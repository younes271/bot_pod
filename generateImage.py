import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def generate_image(prompt):
    api_key = os.getenv('OPENAI_API_KEY')
    size = "1024x1024"
    response_format = "url"  # Choose from "url" or "b64_json"
    style = "vivid"  # Choose from "vivid" or "natural"
    quality = "standard"  # Choose from "standard" or "hd"

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    data = {
        'prompt': prompt,
        'n': 1,  # DALL-E 3 currently only supports n=1
        'size': size,
        'response_format': response_format,
        'model': "dall-e-3",  # Specify DALL-E 3 model
        'style': style,
        'quality': quality
    }

    try:
        response = requests.post('https://api.openai.com/v1/images/generations', json=data, headers=headers)
        response.raise_for_status()
        image_url = response.json()['data'][0]['url']
        logger.info(f"Image URL: {image_url}")
        return image_url
    except requests.exceptions.HTTPError as err:
        logger.error(f"HTTP Error: {err}")
    except Exception as e:
        logger.error(f"Error: {e}")
