from openai import OpenAI
from typing import List, Dict
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from secrets import OPEN_AI_KEY

# Initialize OpenAI client
client = OpenAI(api_key=OPEN_AI_KEY)

# Step 1.5: Filter out any news stories which
#    - contain names of people (cannot be uploaded into Sora)
#    - contain topics which are not suitable for the general audience

# Helper function to process LLM JSON response
def extract_json(text):
    """This function extracts JSON string from the LLM response and formats it."""
    text = text.replace(": None", ": null")
    text = text.replace(": False", ": false")
    text = text.replace(": True", ": true")
    
    # Expected format is "```json\n{<INFO>}```"
    if text.startswith("```json") and text.endswith("```"):
        text = text.strip("```")
        text = text.strip("json")
        try:
            parsed_json = json.loads(text)
            return json.dumps(parsed_json, indent=4)
        except Exception:
            pass
    # If not the expected format, just give it a try
    else:
        try:
            parsed_json = json.loads(text)
            return json.dumps(parsed_json, indent=4)
        except Exception:
            pass
    return ""

# Agent that checks for people's names and inappropriate stories
def filter_title_agent(title: str) -> bool:
    content = f"""
Read the <NEWS_TITLE> and determine if it
1. mentions the name of a person
2. has adult themes which include war, murder, sex, or politics.
Your response must follow the <JSON_RESPONSE_SCHEMA>.

<NEWS_TITLE>
{title}

<JSON_RESPONSE_SCHEMA>
{{
"has_person_name": true/false,
"adult_themed": true/false
}}
"""
    response = client.chat.completions.create(
        messages=[
            {'role': 'system', 'content': 'You are a fact-checking assistant.'},
            {'role': 'user', 'content': content},
        ],
        model='gpt-4o',
    )
    response = response.choices[0].message.content.strip()
    try:
        response = extract_json(response)
        response = json.loads(response)
        return response
    except:
        # Error on the side that it should be filtered out.
        return {"has_person_name": True, "adult_themed": True} 

# Function to process a single news title
def process_title(title: str) -> Dict[str, bool]:
    filter_check = filter_title_agent(title)
    filter_check['title'] = title
    return filter_check

# Function to filter news using parallel processing
def filter_news_parallel(news: List[str]) -> List[str]:
    filtered_news = []
    rejected_news = []
    agent_results = []

    with ThreadPoolExecutor() as executor:
        # Submit tasks for each title
        futures = {executor.submit(process_title, title): title for title in news}

        for future in as_completed(futures):
            result = future.result()
            agent_results.append(result)

            # Add to filtered news if both checks return False
            if not result["has_person_name"] and not result["adult_themed"]:
                filtered_news.append(result["title"])
            else:
                rejected_news.append(result["title"])

    # print("Agent Results:", json.dumps(agent_results, indent=2))
    # print("Filtered News:", '\n'.join(filtered_news))
    # print("Rejected News:", '\n'.join(rejected_news))
    return filtered_news
