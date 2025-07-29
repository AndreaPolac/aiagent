import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_function import available_functions, call_function

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")


def main(input_prompt, verbosity):
    client = genai.Client(api_key=api_key)
    messages = [
        types.Content(role="user", parts=[types.Part(text=input_prompt)]),
    ]
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
            ),
    )
    for function_call_part in response.function_calls:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
        call_result = call_function(function_call_part, verbose=verbosity)

        if not call_result.parts[0].function_response.response:
            raise Exception(f"Function call failed")

        if verbosity:
            print(f"User prompt: {input_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            print(f"-> {call_result.parts[0].function_response.response}")
    print(response.text)
    

if __name__ == "__main__":
    input_prompt = sys.argv[1] 
    verbosity = sys.argv[2] if len(sys.argv) >= 3 else None
    main(input_prompt, verbosity)
