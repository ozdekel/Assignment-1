import os
import subprocess
import random
import time
from openai import OpenAI
from colorama import Fore, Style, init
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)

# Initialize OpenAI API client
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Number of retries for fixing errors
MAX_RETRIES = 5
LINT_RETRIES = 3


def add_noise_to_code(code):
    """Add random noise to the code to simulate errors."""
    if random.random() > 0.5:  # 50% chance of adding noise
        noise_index = random.randint(0, len(code) - 1)
        return code[:noise_index] + "@" + code[noise_index:]  # Add random "@" in the code
    return code


def time_execution(file_path):
    """Run the generated code and time its execution."""
    start_time = time.perf_counter()
    subprocess.run(["python", os.path.abspath(file_path)], check=True)
    end_time = time.perf_counter()
    return (end_time - start_time) * 1000  # Convert to milliseconds


def run_lint_check(file_path):
    """Run pylint on the file and return its output."""
    try:
        result = subprocess.run(
            ["pylint", os.path.abspath(file_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        return result.stdout, result.returncode
    except FileNotFoundError:
        print(Fore.RED + "Error: pylint is not installed or not found in PATH.")
        return "", 1


def save_lint_errors(lint_output, attempt):
    """Save lint errors to a log file."""
    with open("lint_errors.log", "a") as log_file:
        log_file.write(f"\n--- Lint Attempt {attempt} ---\n")
        log_file.write(lint_output)


def super_python_coder():
    # List of program ideas
    program_list = [
        "Write a Python program to find the greatest common divisor (GCD) of two numbers using the Euclidean algorithm, with unit tests to validate the solution. Include at least 10 unit tests to validate the algorithm with various edge cases and scenarios. Only return the raw Python code, without any explanations or formatting syntax.",
        "Write a Python program to solve the 'Regular Expression Matching' problem, where you implement a function to determine if a string matches a given pattern containing '.' and '*' as wildcards. Include at least 10 unit tests to validate the algorithm with various edge cases and scenarios. Only return the raw Python code, without any explanations or formatting syntax."
    ]

    print(Fore.CYAN + "I’m Super Python Coder. Tell me, which program would you like me to code for you?")
    print(Fore.CYAN + "If you don't have an idea, just press enter and I will choose a random program to code.")
    user_input = input(Fore.GREEN + "\nEnter your program idea: ").strip()

    if user_input:
        selected_prompt = (
            user_input.strip()
            + " Include at least 10 unit tests to validate the algorithm with various edge cases and scenarios. "
            + "Only return the raw Python code, without any explanations or formatting syntax."
        )
    else:
        selected_prompt = random.choice(program_list)

    print(Fore.MAGENTA + "\nSelected prompt:")
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

            if not os.path.exists(file_path):
                raise FileNotFoundError(f"File '{file_path}' was not created.")
            print(Fore.GREEN + f"\nGenerated code saved to: {os.path.abspath(file_path)}")

            # Measure and optimize the code for runtime
            print(Fore.MAGENTA + "\nOptimizing the code for runtime efficiency...")

            # Measure original runtime
            before_optimization_time = time_execution(file_path)
            print(Fore.CYAN + f"\nOriginal runtime: {before_optimization_time:.2f} milliseconds.")

            # Prompt for optimization
            optimize_prompt = (f"The following Python code works correctly, but I want it to be optimized for runtime efficiency. "
                               f"Please make it faster while keeping it functionally correct and adhering to Python best practices.\n\n"
                               f"{output_code}\n\n"
                               "Only return the raw Python code, without any explanations or formatting syntax.")

            optimization_completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": optimize_prompt}]
            )
            optimized_code = optimization_completion.choices[0].message.content

            # Save the optimized code
            optimized_code_cleaned = "\n".join([line.rstrip() for line in optimized_code.splitlines()])  # Clean trailing whitespace
            with open(file_path, "w") as file:
                file.write(optimized_code_cleaned + "\n")  # Add exactly one newline at the end

            # Measure optimized runtime
            after_optimization_time = time_execution(file_path)
            print(Fore.CYAN + f"\nOptimized runtime: {after_optimization_time:.2f} milliseconds.")

            # Compare runtimes
            if after_optimization_time < before_optimization_time:
                print(Fore.GREEN + f"\nCode optimization successful! Runtime improved from {before_optimization_time:.2f} to {after_optimization_time:.2f} milliseconds.")
            else:
                print(Fore.RED + f"\nCode optimization failed to improve runtime. Proceeding with lint fixes.")

            # Perform lint checks and fix warnings/errors
            for lint_attempt in tqdm(range(1, LINT_RETRIES + 1), desc="Lint Check Progress", ncols=75):
                lint_output, lint_status = run_lint_check(file_path)
                save_lint_errors(lint_output, lint_attempt)  # Save lint output to log

                if lint_status == 0:
                    print(Fore.GREEN + "\nAmazing. No lint errors/warnings.")
                    break
                else:
                    print(Fore.RED + f"\nLint attempt {lint_attempt}: Lint issues detected. Fixing...")
                    print(Fore.RED + lint_output)
                    lint_fix_prompt = (f"The following Python code has lint warnings/errors. Fix all issues to improve its pylint score to 10/10. "
                    f"Specifically, ensure the following:\n"
                    f"- Add a module-level docstring at the top of the file describing its purpose.\n"
                    f"- Add a docstring for every function, describing its purpose, parameters, and return values.\n"
                    f"- Add a docstring for every class, describing its purpose and role in the code.\n"
                    f"- Ensure all imports are at the top of the file, and remove any unused imports.\n"
                    f"- Remove any trailing blank lines or add a single newline at the end of the file.\n"
                    f"- Ensure no line exceeds 100 characters in length. Split long lines appropriately.\n"
                    f"- Add exactly one newline at the end of the file.\n"
                    f"- Remove all trailing whitespace from the code, ensuring no line ends with unnecessary spaces or tabs.\n\n"
                    f"{output_code}\n\n"
                    "Only return the raw Python code, without any explanations or formatting syntax."
)
                    lint_completion = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": lint_fix_prompt}]
                    )
                    output_code = lint_completion.choices[0].message.content
                    cleaned_lines = [line.rstrip() for line in output_code.splitlines()]  # Strip trailing whitespace from each line
                    cleaned_code = "\n".join(cleaned_lines)
                    with open(file_path, "w") as file:
                        file.write(cleaned_code + "\n")

            if lint_status != 0:
                print(Fore.RED + "\nThere are still lint errors/warnings after 3 attempts.")
                print(Fore.LIGHTBLUE_EX + "Please review 'lint_errors.log' for details.")
                return

            print(Fore.GREEN + "Lint fixing process completed successfully!")
            break

        except subprocess.CalledProcessError as e:
            errors = e.stderr.strip() if e.stderr else str(e)
            print(Fore.RED + f"\nError running generated code! Error: {errors}")
            if attempt < MAX_RETRIES:
                print(Fore.CYAN + "Trying again...")
            else:
                print(Fore.RED + "Code generation FAILED.")
                return

        except Exception as e:
            errors = str(e)
            print(Fore.RED + f"\nAn unexpected error occurred: {errors}")
            if attempt < MAX_RETRIES:
                print(Fore.CYAN + "Trying again...")
            else:
                print(Fore.RED + "Code generation FAILED.")
                return


# Run the assistant
if __name__ == "__main__":
    super_python_coder()
