from openai import OpenAI, api_key
import os
from dotenv import load_dotenv

import json

# Set your API key
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

# Define function to generate response
def generate_response(model="gpt-3.5-turbo", history=[]):
    history.insert(0, {"role":"system", "content":"You are a translator bot to translate text to english. You return json with the format {translation : text}"})
    try:
        response = client.chat.completions.create(
            model=model,
            response_format={ "type": "json_object" },
            messages=history
        )
        response = response.choices[0].message.content
        print(response)
        # convert to json
        response = json.loads(response)
        return response["translation"]
    
    except Exception as e:
        print(e)
        return str(e)

# Define function to run the chatbot
def query(prompt='', history=[]):
    if prompt != '':
        history.append({"role":"user", "content":prompt})
    return generate_response(history=history)

if __name__ == "__main__":
    pass