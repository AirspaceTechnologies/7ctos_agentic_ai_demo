from openai import OpenAI
import requests
from typing import List
from secrets import NEWS_API_KEY, OPEN_AI_KEY

# Initialize OpenAI client
client = OpenAI(api_key=OPEN_AI_KEY)

# Step 1: Pull the news from a news API
def fetch_news(api_key: str, query: str = "top headlines") -> List[str]:
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"
    response = requests.get(url)
    news_data = response.json()

    if "articles" in news_data:
        return [article["title"] for article in news_data["articles"]]
    else:
        raise ValueError("Failed to fetch news")

# Step 2: Summarize the news
def summarize_news(news: List[str]) -> str:
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a concise news summarizer."},
            {"role": "user", "content": f"Summarize this news: {news}"},
        ],
        model="gpt-4o",
    )
    return response.choices[0].message.content.strip()

# Step 3: Choose the most entertaining news
def choose_news_topic(news: List[str]) -> str:
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a critic that finds the most entertaining news from a list of topics"},
            {"role": "user", "content": f"Please tell me the topic that is the most entertaining from the list: {news}"},
        ],
        model="gpt-4o",
    )
    return response.choices[0].message.content.strip()

# Step 4: Sensationalize the summary
def sensationalize_summary(summary: str) -> str:
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a conspiracy theorist. Embelish any details to maxmize entertainment. Feel free to make things up. Keep it to a few sentances."},
            {"role": "user", "content": f"Make this summary more shocking: {summary}"},
        ],
        model="gpt-4o",
    )
    return response.choices[0].message.content.strip()

# Step 5: Generate a movie trailer description
def generate_movie_trailer(sensational_summary: str) -> str:
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You make 10 second videos with a cool tool named Sora by OpenAI"},
            {"role": "user", "content": f"Create a sora prompt for a 10 second movie based on the text: {sensational_summary}"},
        ],
        model="gpt-4o",
    )
    return response.choices[0].message.content.strip()

# Step 6: Refine with a movie critic agent
def refine_trailer_with_critic(trailer: str) -> str:
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are a movie critic collaborating with a screenwriter to refine a trailer to maximize its entertainment for 10 second movie trailers."},
            {"role": "user", "content": f"Please provide a 10 second narration that would work over a short video: {trailer}"},
        ],
        model="gpt-4o",
    )
    return response.choices[0].message.content.strip()

# Helper function to ask if a step should be repeated
def ask_to_repeat(prompt: str) -> bool:
    while True:
        user_input = input(f"{prompt} (yes/no): ").strip().lower()
        if user_input in ["yes", "y"]:
            return True
        elif user_input in ["no", "n"]:
            return False
        else:
            print("Please answer 'yes' or 'no'.")

# Main function to run the workflow
def main():
    news_api_key = NEWS_API_KEY

    print("Fetching the latest news...")
    news = fetch_news(news_api_key)
    print(f"Fetched news: {news}\n")

    print("Summarizing the news...")
    summary = summarize_news(news)
    print(f"News Summary: {summary}\n")

    print("Choosing the most entertaining news...")
    top_topic = choose_news_topic(summary)
    print(f"The most entertaining topic is: {top_topic}\n")

    while ask_to_repeat("Do you want to refine the news topic?"):
        print("Refining...")
        summary = summarize_news(top_topic)
        print(f"Updated News Summary: {summary}\n")

    print("Sensationalizing the summary...")
    sensational_summary = sensationalize_summary(top_topic)
    print(f"Sensationalized Summary: {sensational_summary}\n")

    while ask_to_repeat("Do you want to make the summary more sensational?"):
        print("Making the summary more sensational...")
        sensational_summary = sensationalize_summary(sensational_summary)
        print(f"Updated Sensationalized Summary: {sensational_summary}\n")

    print("Generating movie trailer description...")
    trailer = generate_movie_trailer(sensational_summary)
    print(f"Initial Movie Trailer: {trailer}\n")

    while ask_to_repeat("Do you want to refine the trailer with the movie critic?"):
        print("Refining the trailer with the movie critic...")
        trailer = refine_trailer_with_critic(trailer)
        print(f"Updated Movie Trailer: {trailer}\n")

if __name__ == "__main__":
    main()
