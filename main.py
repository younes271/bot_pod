import logging
from dotenv import load_dotenv
from generatePrompt import generater_function
from generateImage import generate_image
from save_image import save_and_resize_image

# Load environment variables
load_dotenv()

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def main():
    try:
        prompt = generater_function()
        logger.info(f"Generated Prompt: {prompt}")
        
        image_url = generate_image(prompt)
        logger.info(f"Generated Image URL: {image_url}")
        
        save_and_resize_image(image_url)
        logger.info("Image saved and resized successfully.")

    except Exception as e:
        logger.error(f"Error in main function: {e}")

if __name__ == "__main__":
    main()
