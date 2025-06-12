# AI-Agent

A Python-based AI agent that uses Google's Gemini API to perform file system operations and code execution in a safe, controlled environment.

## Project Description

This project demonstrates how to build an AI agent that can:
- List files and directories
- Read file contents
- Execute Python files
- Write or overwrite files

The agent uses the Gemini API as a decision-making engine, but all actual code execution is performed by our own functions. This ensures that the LLM can only perform operations that we explicitly allow.

## Scope

The agent operates within a controlled environment where:
- All file operations are constrained to a specific working directory
- The LLM can only call predefined functions with specific parameters
- File paths must be relative to the working directory
- The working directory parameter is hardcoded for security

## Learning Objectives

This project demonstrates several important concepts in AI agent development:

1. **Function Calling**: How to define and expose functions to an LLM
   - Using `types.FunctionDeclaration` to define function schemas
   - Using `types.Tool` to make functions available to the LLM
   - Implementing proper parameter validation and security checks

2. **Conversation Management**: How to maintain context in a multi-turn conversation
   - Keeping track of the conversation history
   - Handling function calls and their results
   - Implementing a maximum iteration limit to prevent infinite loops

3. **Security Considerations**: How to safely execute code in an AI agent
   - Constraining file operations to a specific directory
   - Hardcoding sensitive parameters
   - Implementing proper error handling and validation

4. **System Design**: How to structure an AI agent application
   - Separating concerns between LLM interaction and code execution
   - Implementing a modular function system
   - Creating a maintainable and extensible codebase

## Important Limitations

1. **Decision Making vs. Execution**
   - We're using the LLM as a decision-making engine, but we're still the ones running the code
   - All actual file operations and code execution are performed by our own functions
   - The LLM can only suggest operations, not perform them directly

2. **Security Constraints**
   - We won't allow the LLM to specify the working_directory parameter. We're going to hard code that
   - All file paths must be relative to the working directory
   - File operations are constrained to prevent access to sensitive areas

3. **Function Availability**
   - The LLM can only use functions that we explicitly define and make available
   - Each function has a strict schema that defines its parameters and behavior
   - Function calls are validated before execution

## Getting Started

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment:
   - Create a `.env` file with your Gemini API key:
     ```
     GEMINI_API_KEY=your_api_key_here
     ```

3. Run the agent:
   ```bash
   python main.py "your prompt here"
   ```

   For verbose output:
   ```bash
   python main.py --verbose "your prompt here"
   ```

## Example Usage

```bash
# List files in a directory
python main.py "list the contents of the pkg directory"

# Read a file
python main.py "read the contents of main.py"

# Execute a Python file
python main.py "run tests.py"

# Write to a file
python main.py "write 'hello world' to test.txt"
```