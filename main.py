import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
import argparse
from functions.get_files_info import get_files_info

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true', help='Enable verbose output')
    parser.add_argument('prompt', help='The prompt to send to the model')
    args = parser.parse_args()

    load_dotenv()

    system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
        ]
    )

    messages = [
        types.Content(role="user", parts=[types.Part(text=args.prompt)])
    ]

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions],
            system_instruction=system_prompt
        )
    )

    if args.verbose:
        print("User prompt:", args.prompt)
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)
    
    print("Response:")
    
    # Check for function calls
    if response.candidates and response.candidates[0].content.parts:
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'function_call'):
                print(f"Calling function: {part.function_call.name}({part.function_call.args})")
                # Execute the function call
                if part.function_call.name == "get_files_info":
                    result = get_files_info(".", part.function_call.args.get("directory", "."))
                    print(result)
            else:
                print(part.text)


if __name__ == "__main__":
    main()
