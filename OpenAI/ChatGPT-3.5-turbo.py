import openai

# Set the OpenAPI key, replace KEY with your actual key
openai.api_key = key = "KEY" 

# Set the model to be used
engine = "gpt-3.5-turbo"

# Prompt for a question
question = input("What's your question?: ")

# Submit the question, using the default values for everything - https://platform.openai.com/docs/api-reference/completions
response = openai.ChatCompletion.create(
    model= engine,
    messages=[
        {"role": "user", "content": question},
    ],
)

print(response['choices'][0]['message']['content'])
