import os
from pathlib import Path

def write_file(working_directory, file_path, content):
    # If file_path is not absolute, resolve it relative to working_directory
    if not os.path.isabs(file_path):
        file_path_abs = os.path.abspath(os.path.join(working_directory, file_path))
    else:
        file_path_abs = os.path.abspath(file_path)
    
    # Check if file is outside working directory
    working_dir_abs = os.path.abspath(working_directory)
    if not file_path_abs.startswith(working_dir_abs):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    try:
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(file_path_abs), exist_ok=True)
        
        # Write content to file
        with open(file_path_abs, 'w', encoding='utf-8') as f:
            f.write(content)
            
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        
    except Exception as e:
        return f'Error: {str(e)}'