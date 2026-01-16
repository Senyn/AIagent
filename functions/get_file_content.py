import os

def get_file_content(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    target_file_path = os.path.normpath(os.path.join(abs_working_directory, file_path))
    valid_target_file = os.path.commonpath([abs_working_directory, target_file_path]) == abs_working_directory
    if not valid_target_file:
        return f"Error: Cannot read \"{file_path}\" as it is outside the permitted working directory"
    if not os.path.isfile(target_file_path):
        return f"Error: \"{target_file_path}\" is not a file"
    
    try:
        with open(target_file_path, 'r') as file:
            content = file.read(10000)
            if file.read(1):
                content += f'[...File "{file_path}" truncated at {10000} characters]'
            return content
    except:
        return f"Error: "
    
