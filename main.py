import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
import sys
import argparse
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python import run_python_file
from functions.write_file import write_file

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
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files

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

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Reads and returns the contents of a file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to read, relative to the working directory.",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes a Python file with optional arguments, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the Python file to execute, relative to the working directory.",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes or overwrites content to a file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The path to the file to write to, relative to the working directory.",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content to write to the file.",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file,
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
                elif part.function_call.name == "get_file_content":
                    result = get_file_content(".", part.function_call.args.get("file_path"))
                    print(result)
                elif part.function_call.name == "run_python_file":
                    result = run_python_file(".", part.function_call.args.get("file_path"))
                    print(result)
                elif part.function_call.name == "write_file":
                    result = write_file(".", part.function_call.args.get("file_path"), part.function_call.args.get("content"))
                    print(result)
            else:
                print(part.text)


if __name__ == "__main__":
    main()
