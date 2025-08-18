import time
import os

from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

service_obj = Service("C:/Users/Tulip/Downloads/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service = service_obj)
driver.maximize_window()
driver.implicitly_wait(5)

# Load env variable
load_dotenv()

url = os.getenv("URL")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

wait = WebDriverWait(driver, 10)
quick_wait = WebDriverWait(driver, 1)

# ======================================================================================================================

# login form
driver.get(url)
driver.find_element(By.ID, 'email').send_keys(email)
driver.find_element(By.ID, 'password').send_keys(password)
driver.find_element(By.CLASS_NAME, 'login-button').click()
time.sleep(5)

#login validation wait
wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'swal2-container')))

# ======================================================================================================================

#dashboard page validation
welcome = driver.find_element(By.CLASS_NAME, 'header-title').text
print(f'Login successful: {welcome}')
assert 'Welcome' in welcome

# ======================================================================================================================

#org page access validation
driver.find_element(By.XPATH, "//li[3]").click()
org_page = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "page-header-title")))
org_page_text = org_page.text
print(f'Accessed Organization Page successfully: {org_page_text}')
assert 'All Organizations' in org_page_text

# ======================================================================================================================

# navigate to the targeted organization
# search for the org
driver.find_element(By.CLASS_NAME, "connect-studio-search-input-small").send_keys("Automated")

# click the org
try:
    wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//h6[normalize-space()='Automated Test ORG']")))
    driver.find_element(By.CLASS_NAME, "org-card-arrow-icon").click()
except:
    print('Org not found')
    
org_name = driver.find_element(By.CLASS_NAME, "client-org-name").text
print(f'Organization Name: {org_name}')

# ======================================================================================================================

# click the create portal btn
driver.find_element(By.XPATH, "//li[@class='show']").click()

time.sleep(3)