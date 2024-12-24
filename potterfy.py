from openai import OpenAI
from typing import List
import time
from secrets import OPEN_AI_KEY

# Initialize OpenAI client
client = OpenAI(api_key=OPEN_AI_KEY)

def pick_artist_lyric(artist_name: str):
    """
    Agent to pick a lyric or line from the given artist.
    """
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an agent that retrieves a poetic or iconic lyric from a specified musical artist. Please only return the line and not the name of the artist or any additional context"},
            {"role": "user", "content": f"Provide a famous line or lyric from the artist: {artist_name}"},
        ],
        model="gpt-4o",
    )
    return response.choices[0].message.content.strip()

def make_text_more_magical(text):
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an agent that transforms any given text to sound like it comes from a Harry Potter book. Please be brief"},
            {"role": "user", "content": f"Make the following text sound more magical: {text}"},
        ],
        model="gpt-4o",
    )
    return response.choices[0].message.content.strip()

def is_text_harry_potter(text: str) -> str:
    response = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "You are an agent that determines if a given sentence sounds like it comes from the Harry Potter series."
             " Reply with only 'YES' if it does, and 'NO' if it does not."},
            {"role": "user", "content": f"Does the following sentence sound like it is from Harry Potter?: {text}"},
        ],
        model="gpt-4o",
    )
    return response.choices[0].message.content.strip() == "YES"

def recursive_text_transformation(initial_text):
    """
    Recursively call the magical agent until the Harry Potter agent approves
    """
    print("\nStarting Text: \"{}\"\n".format(initial_text))
    current_text = initial_text
    iteration_count = 0
    iterations = []

    while True:
        iteration_count += 1
        print(f"Iteration {iteration_count}: Enhancing the magic...")

        # Agent 1: Make text more magical
        current_text = make_text_more_magical(current_text)
        print(f"Magical Text: \"{current_text}\"\n")
        iterations.append((iteration_count, current_text))
        
        # Agent 2: Check if text sounds like Harry Potter
        if is_text_harry_potter(current_text):
            print(f"The text has been approved as Harry Potter-like after {iteration_count} iterations!\n")
            break
        else:
            print("Not quite Harry Potter yet. Continuing...\n")
        time.sleep(1)

    print("Final Magical Output: \"{}\"".format(current_text))
    print(f"Total Iterations: {iteration_count}")
    render_marp_presentation(iterations)
    return current_text

def render_marp_presentation(iterations):
    """
    Render a Marp Markdown file with each iteration as a slide.
    """
    with open("magical_iterations.md", "w") as f:
        f.write("---\ntheme: default\nmarp: true\n---\n# Magical Logs")
        for iteration, text in iterations:
            f.write(f"\n---\n# Iteration {iteration}\n{text}\n\n")
        print("Marp presentation saved as 'magical_iterations.md'.")

if __name__ == "__main__":
    artist_name = input("Enter the name of a musical artist: ")
    initial_text = pick_artist_lyric(artist_name)
    print(f"Selected Line from {artist_name}: \"{initial_text}\"\n")
    final_magical_text = recursive_text_transformation(initial_text)