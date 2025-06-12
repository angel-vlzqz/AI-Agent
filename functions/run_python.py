import os
import subprocess
from pathlib import Path

def run_python_file(working_directory, file_path):
    # Convert paths to absolute paths
    working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_dir, file_path))
    
    # Check if file is outside working directory
    if not abs_file_path.startswith(working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    # Check if file exists
    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    
    # Check if file is a Python file
    if not file_path.endswith('.py'):
        return f'Error: "{file_path}" is not a Python file.'
    
    try:
        # Run the Python file with timeout
        result = subprocess.run(
            ['python', file_path],
            cwd=working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # Build output string
        output_parts = []
        
        if result.stdout:
            output_parts.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output_parts.append(f"STDERR:\n{result.stderr}")
        if result.returncode != 0:
            output_parts.append(f"Process exited with code {result.returncode}")
            
        if not output_parts:
            return "No output produced."
            
        return "\n".join(output_parts)
        
    except subprocess.TimeoutExpired:
        return "Error: Process timed out after 30 seconds"
    except Exception as e:
        return f"Error: executing Python file: {e}" 