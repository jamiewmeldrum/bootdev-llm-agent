import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.functions_schema import available_functions
from config import system_prompt

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")

def main():

    verbose = "--verbose" in sys.argv

    if not len(sys.argv) >= 2:
        print("AI Code Assistant")
        print('\nUsage: python main.py "your prompt here" [--verbose]')
        print('Example: python main.py "How do I build a calculator app?"')
        sys.exit(1)

    query = sys.argv[1]
    messages = [
        types.Content(role="user", parts=[types.Part(text=query)]),
    ]

    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", 
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions],
            ),
        )
    
    if verbose:
        print(f"User prompt: {query}")

    
    if len(response.function_calls) > 0:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")
    else:
        print(f"Response: {response.text}")

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count }")


if __name__ == "__main__":
    main()
