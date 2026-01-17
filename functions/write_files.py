import os

def write_file(working_directory, file_path, content):
    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
    valid_target_file = os.path.commonpath([abs_working_directory, target_file_path]) == abs_working_directory
    if not valid_target_file:
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    if os.path.isdir(target_file_path):
        return f"Error: Cannot write to \"{target_file_path}\" as it is a directory"
    
    try:
        if os.makedirs(os.path.dirname(target_file_path), exist_ok=True):
            pass
        with open(target_file_path, "w") as file:
            file.write(content)
            return f"Successfully wrote to \"{file_path}\" ({len(content)} characters written)"
    except:
        return f"Error: "
