from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Set up options for Firefox (optional)
options = Options()
options.add_argument("--start-maximized")  # Start maximized (optional)

# Provide the path to the Firefox WebDriver (geckodriver)
service = Service(executable_path='./geckodriver')  # Assuming geckodriver is in the same folder

# Initialize the WebDriver
driver = webdriver.Firefox(service=service, options=options)

# Open the website
driver.get("https://www.venus.net.pl/")

# Locate the ul element
ul_element = driver.find_element(By.CSS_SELECTOR, "div#navbarSupportedContent ul.navbar-nav.justify-content-between.w-100")

# Locate all li elements within the ul
li_elements = ul_element.find_elements(By.CLASS_NAME, "nav-item.dropdown")

# List to store the data
collected_data = []

# Iterate over each li element
for li in li_elements:
    try:
        # Click the li element
        li.click()
        time.sleep(2)  # Wait for the dropdown content to load (adjust timing if necessary)
        
        # Collect all anchor tags within the clicked li element
        anchors = li.find_elements(By.TAG_NAME, "a")
        for anchor in anchors:
            href = anchor.get_attribute("href")
            text = anchor.text.strip()
            collected_data.append({"Text": text, "URL": href})
    except Exception as e:
        print(f"An error occurred: {e}")
        continue

# Save the collected data to an Excel file
df = pd.DataFrame(collected_data)
df.to_excel('collected_links.xlsx', index=False)

# Print a success message
print("Data collected and saved to 'collected_links.xlsx'.")

# Optionally, close the browser when done
driver.quit()
