import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('prompt', help='The prompt to send to the model')
    args = parser.parse_args()

    load_dotenv()

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)])
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages
    )

    if args.verbose:
        print("User prompt:", args.prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    print("Response:")
    print(response.text)


if __name__ == "__main__":
    main()
