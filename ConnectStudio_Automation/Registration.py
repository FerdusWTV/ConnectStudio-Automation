import time
import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from dotenv import load_dotenv

service_obj = Service("C:/Users/Tulip/Downloads/chromedriver-win64/chromedriver.exe")
driver = webdriver.Chrome(service = service_obj)
driver.maximize_window()
driver.implicitly_wait(5)

load_dotenv()

url = os.getenv("URL")
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

wait = WebDriverWait(driver, 10)
quick_wait = WebDriverWait(driver, 3)

# ======================================================================================================================

# login form
driver.get(url)
driver.find_element(By.ID, 'email').send_keys(email)
driver.find_element(By.ID, 'password').send_keys(password)
driver.find_element(By.CLASS_NAME, 'login-button').click()
time.sleep(5)

#login validation wait
wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, 'swal2-container')))

#dashboard page validation
welcome = driver.find_element(By.CLASS_NAME, 'header-title').text
print(f'welcome: {welcome}')

# ======================================================================================================================

# assert
assert 'Welcome' in welcome, "Test Failed: LOgin Unsuccessful"
print("Test Passed: Login Successful")


time.sleep(5)