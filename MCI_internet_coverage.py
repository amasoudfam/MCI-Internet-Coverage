import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

# URL of the MCI internet coverage map
urlpage = 'https://mci.ir/notrino-coverage-map'

# Set up the WebDriver for Chrome (adjust the executable path as needed)
service = Service(executable_path="./chromedriver")
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

# Initialize a list to store the scraped data
data = []

# Start loading the page
driver.get(urlpage)

# Wait for 2 seconds to ensure the page loads
time.sleep(2)

# Loop through page numbers (assuming a range of 1 to 294)
for i in range(1, 295):
    # Find the link element with the current page number
    element = driver.find_element(By.LINK_TEXT, str(i))
    element.click()
    # Wait for 1 second to allow the data to load
    time.sleep(1)
    # Get the HTML source of the page
    htmlSource = driver.page_source
    # Use regular expressions to extract the data from HTML
    k = re.findall("<td>(.+?)</td><td>(.+?)</td><td class=\" en-text\">(.+?)</td>", htmlSource)
    for item in k:
        temp = {}
        item = list(item)
        # Assign data to appropriate columns
        temp['Province'] = item[0]
        temp['Region'] = item[1]
        temp['Status'] = item[2]
        temp['3G'] = 1 if '3G' in item[2] else 0
        temp['4G'] = 1 if '4G' in item[2] else 0
        temp['4.5G'] = 1 if '4.5G' in item[2] else 0
        # Append the data to the list
        data.append(temp)

# Close the WebDriver
driver.quit()

# Create a DataFrame from the collected data and save it as an Excel file
pd.DataFrame(data).to_excel('MCI_internet_coverage.xlsx', index=None)
