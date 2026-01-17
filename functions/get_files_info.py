import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    abs_working_directory = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_directory, directory))
    # Will be True or False
    valid_target_dir = os.path.commonpath([abs_working_directory, target_dir]) == abs_working_directory
    if not valid_target_dir:
        return f"Error: Cannot list \"{directory}\" as it is outside the permitted working directory"
    if not os.path.isdir(target_dir):
        return f"Error: \"{target_dir}\" is not a directory"
    result = []
    try:
        for files in os.listdir(target_dir):
            file_path = os.path.join(target_dir, files)
            file_size = os.path.getsize(file_path)
            is_dir = os.path.isdir(file_path)
            result.append(f"  -{files}: file_size={file_size} bytes, is_dir={is_dir}")
        return "\n".join(result)

    except:
        return f"Error: Cannot access directory \"{target_dir}\""

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself. Also, Current directory should be represented as '.')",
            ),
        },
     required=["directory"]),
)