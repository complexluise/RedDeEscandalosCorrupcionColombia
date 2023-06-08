import openai
import os

# Load your API key from an environment variable or secret management service
openai.api_key = os.getenv("OPENAI_API_KEY")


def extract_relationship(my_prompt: str) -> str:
    """Extract the relationship between two entities from a text."""
    chat_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": my_prompt}])
    return chat_completion.choices[0].message.content


if __name__ == '__main__':
    my_response = extract_relationship("Hello world")
    print(my_response)
