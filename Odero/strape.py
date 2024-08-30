import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import time

# Set up the Firefox WebDriver
options = Options()
options.headless = False  # Change to True if you don't want the browser to be visible
gecko_path = os.path.join(os.getcwd(), 'geckodriver')  # Path to geckodriver in the same folder
service = Service(executable_path=gecko_path)

driver = webdriver.Firefox(service=service, options=options)

# Load the Excel file
file_path = 'collected_links.xlsx'
df = pd.read_excel(file_path)

# Ensure the URL column exists
if 'URL' not in df.columns:
    raise ValueError("The column 'URL' does not exist in the Excel file.")

# Limit to the first 5 rows
df_subset = df.head(5)

# List to store collected product links
product_links = []

# Function to scroll to the bottom of the page
def scroll_to_bottom(driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(3)  # Wait for new content to load

# Open each link in the URL column
for url in df_subset['URL']:
    try:
        driver.get(url)
        print(f"Opened: {url}")
        
        # Scroll to the bottom of the page to load all elements
        scroll_to_bottom(driver)
        
        # Wait for the specific div and ul to be present and visible
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'product_list_container'))
        )
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'product_list'))
        )
        
        # Find the div containing the product list
        product_list_div = driver.find_element(By.CLASS_NAME, 'product_list_container')
        product_list_ul = product_list_div.find_element(By.CLASS_NAME, 'product_list')

        # Wait for all product elements to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'ajax_block_product'))
        )

        # Find all product links within the li elements
        li_elements = product_list_ul.find_elements(By.CLASS_NAME, 'ajax_block_product')
        for li in li_elements:
            try:
                anchor = li.find_element(By.CLASS_NAME, 'product_link')
                product_links.append(anchor.get_attribute('href'))
            except Exception as e:
                print(f"Failed to extract link from a product item: {e}")

        print(f"Collected {len(product_links)} product links.")
    except Exception as e:
        print(f"Failed to process {url}: {e}")

# Print collected product links
print("Product Links:")
for link in product_links:
    print(link)

# Close the WebDriver
driver.quit()
