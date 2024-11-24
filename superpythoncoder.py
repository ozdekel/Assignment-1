import os
import subprocess
import random
import time
from openai import OpenAI

# Initialize OpenAI API client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Number of retries for fixing errors
MAX_RETRIES = 5


def add_noise_to_code(code):
    """Add random noise to the code to simulate errors."""
    if random.random() > 0.5:  # 50% chance of adding noise
        noise_index = random.randint(0, len(code) - 1)
        return code[:noise_index] + "@" + code[noise_index:]  # Add random "@" in the code
    return code


def time_execution(file_path):
    """Run the generated code and time its execution."""
    start_time = time.perf_counter()
    subprocess.run(["python", file_path], check=True)
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000  # Convert to milliseconds


def super_python_coder():
    # List of program ideas
    program_list = [
        "Write a Python program to find the greatest common divisor (GCD) of two numbers using the Euclidean algorithm, with unit tests to validate the solution. Include at least 10 unit tests to validate the algorithm with various edge cases and scenarios. Only return the raw Python code, without any explanations or formatting syntax.",
        "Write a Python program to implement binary search on a sorted list of numbers, including unit tests for edge cases. Include at least 10 unit tests to validate the algorithm with various edge cases and scenarios. Only return the raw Python code, without any explanations or formatting syntax.",
        "Write a Python program to solve the 'Regular Expression Matching' problem, where you implement a function to determine if a string matches a given pattern containing '.' and '*' as wildcards. Include at least 10 unit tests to validate the algorithm with various edge cases and scenarios. Only return the raw Python code, without any explanations or formatting syntax."
    ]

    print("I’m Super Python Coder. Tell me, which program would you like me to code for you?")
    print("If you don't have an idea, just press enter and I will choose a random program to code.")
    user_input = input("\nEnter your program idea: ").strip()

    if user_input:
        selected_prompt = (
            user_input.strip()
            + " Include at least 10 unit tests to validate the algorithm with various edge cases and scenarios. "
            + "Only return the raw Python code, without any explanations or formatting syntax."
        )
    else:
        selected_prompt = random.choice(program_list)

    print("\nSelected prompt:")
    print(selected_prompt)

    errors = ""
    file_path = "generated_code.py"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            messages = [{"role": "user", "content": selected_prompt}]
            if errors:
                messages.append({"role": "user", "content": f"The previous code had the following errors: {errors}. Please fix them and provide the full corrected code. Only return the raw Python code, without any explanations or formatting syntax."})

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )
            output_code = completion.choices[0].message.content

            # Add noise to simulate errors (if needed)
            if attempt == 1:
                output_code = add_noise_to_code(output_code)

            # Save the generated code to a file
            with open(file_path, "w") as file:
                file.write(output_code)

            print(f"\nGenerated code saved to {os.path.abspath(file_path)}.")

            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File '{file_path}' was not created.")

            # Run and time the code
            print("\nRunning the generated code...")
            before_time = time_execution(file_path)
            print(f"\nCode ran successfully in {before_time:.2f} milliseconds.")

            # Request optimized code
            print("\nRequesting optimized code...")
            optimization_prompt = (
                f"Optimize the following code for performance while keeping the same unit tests:\n\n{output_code}\n\n"
                + "Only return the raw Python code, without any explanations or formatting syntax."
            )
            optimized_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": optimization_prompt}]
            )
            optimized_code = optimized_completion.choices[0].message.content

            # Save the optimized code to the same file
            print("\nRunning the optimized code...")
            with open(file_path, "w") as file:
                file.write(optimized_code)

            after_time = time_execution(file_path)

            # Compare timing results
            if after_time < before_time:
                print(f"\nCode running time optimized! It now runs in {after_time:.2f} milliseconds, while before it was {before_time:.2f} milliseconds.")
                print("The optimized code has replaced the original in 'generated_code.py'.")
            else:
                print(f"\nNo significant optimization. Optimized code runs in {after_time:.2f} milliseconds, while the original code ran in {before_time:.2f} milliseconds.")
                print("The optimized code has replaced the original in 'generated_code.py' for consistency.")

            break

        except subprocess.CalledProcessError as e:
            errors = e.stderr.strip() if e.stderr else str(e)
            print(f"\nError running generated code! Error: {errors}")
            if attempt < MAX_RETRIES:
                print("Trying again...")
            else:
                print("Code generation FAILED.")
                return

        except Exception as e:
            errors = str(e)
            print(f"\nAn unexpected error occurred: {errors}")
            if attempt < MAX_RETRIES:
                print("Trying again...")
            else:
                print("Code generation FAILED.")
                return


# Run the assistant
if __name__ == "__main__":
    super_python_coder()
