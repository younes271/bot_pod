import requests
import json
import random
import logging
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# This is the default and can be omitted
api_key=os.environ.get("OPENAI_API_KEY")



# Set up logging
log_filename = "bot_pod.log"
logging.basicConfig(filename=log_filename, filemode='a', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def generate_descriptions():
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Generate a list of creative descriptions for print-on-demand designs, focusing on various themes like nature, urban, abstract, and fantasy."
            }
        ]
    })
   
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=data)
        response.raise_for_status()
        descriptions = response.json()['choices'][0]['message']['content'].strip().split('\n')
        return [desc for desc in descriptions if desc]
    except Exception as e:
        logger.error(f"Error in generate_descriptions: {e}")
        return []

def get_description(descriptions):
    if not descriptions:
        descriptions = generate_descriptions()

    if descriptions:
        description = random.choice(descriptions)
        descriptions.remove(description)
        return description
    else:
        logger.warning("No descriptions available.")
        return None

def generate_design_prompt(description):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    data = json.dumps({
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": f"Generate a creative prompt for a design based on: {description}"
            }
        ]
    })

    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, data=data)
        response.raise_for_status()
        prompt = response.json()['choices'][0]['message']['content'].strip()
        return prompt
    except Exception as e:
        logger.error(f"Error in generate_design_prompt: {e}")
        return "Error in generating prompt."

# initial value
descriptions = generate_descriptions()

def generater_function():
    description = get_description(descriptions)
    if description:
        design_prompt = generate_design_prompt(description)
        logger.info(f"Description: {description}")
        logger.info(f"Design Prompt: {design_prompt}")
        return design_prompt
