import os
import requests
from PIL import Image
from io import BytesIO
import glob

def save_and_resize_image(url):
    # Create the images directory if it doesn't exist
    os.makedirs('./images', exist_ok=True)
    
    # Download the image
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to download image")
    
    # Load the image into PIL
    image = Image.open(BytesIO(response.content))

    # Check if "default" image already exists
    default_image_path = './images/default.png'
    if os.path.exists(default_image_path):
        # Count the number of images in the folder
        image_count = len(glob.glob('./images/*'))
        # Rename the existing default image
        os.rename(default_image_path, f'./images/{image_count}.png')
    
    # Resize and save the new image as "default"
    image = image.resize((2000, 2000))
    image.save(default_image_path)
