import os
import subprocess
import keyword
from openai import OpenAI
api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
completion = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "user", "content": "“Write a Python program that checks if a number is prime."
         "The input should be read as a command-line argument using sys.argv. "
         "Additionaly include unit tests that validate the program's logic with at least 10 different test cases, covering important edge cases."
         "Use assertions to verify the correctness of the program."
         "Only return the raw Python code, without any explanations or formatting syntax."}
    ]
)
# The folowing remove all the chars that will cause syntax error
output_code=completion.choices[0].message.content
print (output_code)
with open("generatedcode.py", "w") as file:
    file.write(output_code)
number_to_check = input("\nEnter a number:")
try:
    result = subprocess.run(
        ["python", "generatedcode.py",number_to_check], 
        text=True,                    
        capture_output=True,
        check=True
    )
    # Print the output from the generated code
    print(result.stdout)
except subprocess.CalledProcessError as e:
    print("\nError while running 'generatedcode.py':")
    print(e.stderr)
