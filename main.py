import os
import sys
import time

from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.functions_schema import available_functions
from config import system_prompt
from functions.function_caller import call_function

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
    for i in range(20):
        try:
            response = generate_content(verbose, query, messages, client)
            if response:
                print(f"Response: {response}")
                break
        except Exception as e:
            if verbose:
                print("ERROR - something went wrong. Will try again after a small delay")
                print(e)
                time.sleep(0.5)


def generate_content(verbose, query, messages, client):
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

    # Add candidates to messages to persist context
    map(lambda x: messages.append(x.content), response.candidates)
    
    if response.function_calls and len(response.function_calls) > 0:
        for function_call in response.function_calls:
            function_call_response = call_function(function_call, verbose).parts[0].function_response.response

            if not function_call_response:
                raise Exception("Response from running function went badly wrong")
            elif verbose:
                print(f"-> {function_call_response}")

            #Add function calls to messages to persist context
            messages.append(
                types.Content(
                    role="user",
                    parts=[
                        types.Part.from_text(
                            text=f"{function_call_response}",
                        )
                    ],
                )
            )

    else:
        return response.text

    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count }")


if __name__ == "__main__":
    main()
