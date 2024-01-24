import logging
import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Constants
IMAGE_PATH = 'images/default.jpg'
LOGIN_URL = 'https://www.redbubble.com/fr/auth/login'
ADD_PRODUCT_URL = 'https://www.redbubble.com/fr/portfolio/images/new?ref=dashboard'

# Configure logging
logging.basicConfig(filename='myapp.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def login(driver, email, password):
    try:
        # Navigate to the login page
        driver.get(LOGIN_URL)

        # Check if already logged in (redirected to dashboard)
        if "/explore/for-you" in driver.current_url:
            logging.info("Already logged in, redirected to dashboard.")
            return True

        # Find email and password fields
        email_field = driver.find_element(By.NAME, 'cognitoUsername')
        password_field = driver.find_element(By.NAME, 'password')

        # Input email and password
        email_field.send_keys(email)
        password_field.send_keys(password)

        # Wait for the overlay to disappear
        wait = WebDriverWait(driver, 10)
        wait.until(EC.invisibility_of_element_located((By.ID, 'sidebar-overlay-lightbox-6d96416b-2d7a-43f0-adc8-433485ead063-1706080690578')))

        # Find and click the "Connectez-vous" button
        connect_button = driver.find_element(By.XPATH, '//*[@id="login-form-container"]/div/form/span/button')
        connect_button.click()

        # Additional wait or checks can be added here to confirm login success

        logging.info("Login successful.")
        return True
    except Exception as e:
        logging.error(f"Login failed: {e}")
        return False

def active_all_product(driver):
    try:
        # Wait for all elements with the class 'rb-button enable-all' to be clickable
        wait = WebDriverWait(driver, 10)
        buttons = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'enable-all')))

        # Iterate through the found elements and click each one
        for button in buttons:
            try:
                # If the element is visible and clickable
                if button.is_enabled():
                    button.click()
                    # Wait a bit between clicks if necessary
                    logging.info("Activated a product.")
                    time.sleep(1)
            except Exception as e:
                logging.error(f"Error clicking button: {e}")
    except Exception as e:
        logging.error(f"Error finding elements: {e}")

# Function to click a checkbox if it's not already selected
def click_checkbox(driver, checkbox_id):
    checkbox = driver.find_element(By.ID, checkbox_id)
    if not checkbox.is_selected():
        checkbox.click()

def insert_into_input(driver, input_id, input_value):
    # Find the input element and insert text
    input_element = driver.find_element(By.ID, input_id)
    input_element.clear()  # Clear any pre-filled text in the input box
    input_element.send_keys(input_value)

def add_ouevre(driver):
    try:
        # Prepare the file path for the image to be uploaded
        current_dir = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_dir, IMAGE_PATH)

        # Navigate to the page for adding a new image
        driver.get(ADD_PRODUCT_URL)
        time.sleep(3)

        # Find the file input element by its ID
        file_input = driver.find_element(By.ID, 'select-image-single')

        # Send the file path to the input element
        file_input.send_keys(image_path)
        time.sleep(5)
        logging.info("Image added successfully.")

        # Activate all products in this œuvre
        active_all_product(driver)
        time.sleep(3)

        # Write the necessary information
        insert_into_input(driver, "work_title_fr", "design title")
        insert_into_input(driver, "work_tag_field_fr", "tag1, tag2, tag3")
        insert_into_input(driver, "work_description_fr", "Your Description Here")

        # Click the 'media_design' checkbox
        click_checkbox(driver, 'media_design')

        # Click the 'media_digital' checkbox
        click_checkbox(driver, 'media_digital')

        # Click the 'rightsDeclaration' checkbox
        click_checkbox(driver, 'rightsDeclaration')

        # Click the 'work_safe_for_work_true' checkbox
        click_checkbox(driver, 'work_safe_for_work_true')

        # Call the function to activate all products
        active_all_product(driver)

        # Wait for the submit button to be clickable
        wait = WebDriverWait(driver, 10)
        submit_button = wait.until(EC.element_to_be_clickable((By.ID, 'submit-work')))

        # Click the submit button
        submit_button.click()
        logging.info("The product is added successfully.")
    except Exception as e:
        logging.error(f"Error adding œuvre: {e}")

def main_selenium_script():
    try:
        # Initialize the WebDriver
        options = uc.ChromeOptions()
        options.add_argument(r'--user-data-dir=/home/katakuri/.config/google-chrome')
        options.add_argument(r'--profile-directory=Default')
        driver = uc.Chrome(options=options)

        # Read email and password from environment variables
        email = os.getenv("EMAIL")
        password = os.getenv("PASSWORD")

        # Call the login function
        if login(driver, email, password):
            # Call the function to add a new œuvre
            add_ouevre(driver)

            
    except Exception as e:
        logging.error(f"Script execution error: {e}")


