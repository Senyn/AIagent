import os
from google.genai import types


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


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a specified file relative to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path to write to, relative to the working directory (default is the working directory itself. Also, Current directory should be represented as '.')",
            ), "content": types.Schema(
                type=types.Type.STRING,
                description="Content to write to the specified file",
            ),
        },
     ),
)