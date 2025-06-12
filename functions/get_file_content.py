import os
from pathlib import Path

def get_file_content(working_directory, file_path):
    
    # If file_path is not absolute, resolve it relative to working_directory
    if not os.path.isabs(file_path):
        file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))
    else:
        file_path_abs = os.path.abspath(file_path)
    
    # Check if file is outside working directory
    working_dir_abs = os.path.abspath(working_directory)
    if not file_path_abs.startswith(working_dir_abs):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    
    try:
        # Check if path exists and is a file
        if not os.path.isfile(file_path_abs):
            return f'Error: File not found or is not a regular file: "{file_path}"'
        
        # Read file content
        with open(file_path_abs, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Truncate if longer than 10000 characters
        if len(content) > 10000:
            content = content[:10000] + f'\n[...File "{file_path}" truncated at 10000 characters]'
            
        return content
        
    except Exception as e:
        return f'Error: {str(e)}'
        
        