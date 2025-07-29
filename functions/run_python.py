import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_dir = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)
        if not abs_full_path.startswith(abs_working_dir):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.exists(abs_full_path):
            return f'Error: File "{file_path}" not found.'
        if not abs_full_path.endswith(".py"):
            return f'Error: File "{file_path}" is not a Python (.py) file.'

        
        command = ["python", abs_full_path] + args
        completed_process = subprocess.run(
            command,
            cwd=abs_working_dir,
            capture_output=True,
            text=True,
            timeout=30
        )

        output = ""
        if completed_process.stdout:
            output += f'STDOUT:\n{completed_process.stdout}'
        if completed_process.stderr:
            output += f'STDERR:\n{completed_process.stderr}'
        if completed_process.returncode != 0:
            output += f'Process exited with code {completed_process.returncode}\n'
        if not output:
            output = "No output produced."

        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Executes a Python file in the specified working directory with optional arguments.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path to the Python file to execute, relative to the working directory.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING
                ),
                description="Optional arguments to pass to the Python script.",
            ),
        },
    ),
)
