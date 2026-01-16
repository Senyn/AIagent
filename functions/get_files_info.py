import os

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
