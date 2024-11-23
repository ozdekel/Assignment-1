import os
from openai import OpenAI
api_key=os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
completion = client.chat.completions.create(
    model = "gpt-4o-mini",
    messages=[
        {"role": "user", "content": "“Create a python program that checks if a number is prime. Do not write any explanations, just show me the code itself"}
    ]
)
print(completion.choices[0].message.content)