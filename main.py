import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():

    query = None
    if len(sys.argv) >= 2:
        query = sys.argv[1]

    verbose = False
    if len(sys.argv) >= 3 and sys.argv[2] == "--verbose":
        verbose = True

    if not query:
        print("Must provide a command line query")
        exit(1)

    query = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=query)]),
    ]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages
        )
    
    print(response.text)


    if verbose:
        print(f"User prompt: {query}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count }")


if __name__ == "__main__":
    main()
