from openai import OpenAI

# pip install openai


client = OpenAI(
    api_key="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"
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message.content)