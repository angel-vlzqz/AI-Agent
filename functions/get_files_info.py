def get_files_info(working_directory, directory=None):
    import os
    from pathlib import Path

    # If no directory specified, use working directory
    if directory is None:
        directory = working_directory

    # If directory is not absolute, resolve it relative to working_directory
    if not os.path.isabs(directory):
        target_dir_abs = os.path.abspath(os.path.join(working_directory, directory))
    else:
        target_dir_abs = os.path.abspath(directory)
    working_dir_abs = os.path.abspath(working_directory)

    # Check if target directory is outside working directory
    if not target_dir_abs.startswith(working_dir_abs):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

    # Check if path exists and is a directory
    if not os.path.exists(target_dir_abs):
        return f'Error: "{directory}" does not exist'
    if not os.path.isdir(target_dir_abs):
        return f'Error: "{directory}" is not a directory'

    try:
        # Get directory contents and build result string
        result = []
        for item in os.listdir(target_dir_abs):
            item_path = os.path.join(target_dir_abs, item)
            size = os.path.getsize(item_path)
            is_dir = os.path.isdir(item_path)
            result.append(f'- {item}: file_size={size} bytes, is_dir={is_dir}')
        
        return '\n'.join(result)
    except Exception as e:
        return f'Error: {str(e)}'
