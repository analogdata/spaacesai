import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from langchain_community.document_loaders import BSHTMLLoader

# Set up the Selenium WebDriver
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Run in headless mode for automation
driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()), options=options
)

# Specify the URL of the React-based webpage you want to scrape
url = "https://modernspaaces.com/engrace-vista"

# Open the webpage
driver.get(url)

# Wait for the page to fully render (you might need to adjust the sleep time or use WebDriverWait for specific elements)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, "body"))
)

# Get the page source after JavaScript has rendered the content
page_source = driver.page_source

# Close the WebDriver
driver.quit()

# Parse the HTML content with BeautifulSoup using the lxml parser
soup = BeautifulSoup(page_source, "lxml")

# Extract specific data (example: all paragraphs)
paragraphs = soup.find_all("p")
for paragraph in paragraphs:
    print(paragraph.get_text())

# Save the parsed HTML to a file in a specified directory
output_directory = "web_mspaaces"
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

output_file_path = os.path.join(output_directory, "engrace_vista.html")
with open(output_file_path, "w", encoding="utf-8") as file:
    file.write(soup.prettify())

print(f"HTML content successfully written to {output_file_path}")

# Load the HTML content using BSHTMLLoader
loader = BSHTMLLoader(output_file_path)
data = loader.load()

# Print the loaded data
print(data)
