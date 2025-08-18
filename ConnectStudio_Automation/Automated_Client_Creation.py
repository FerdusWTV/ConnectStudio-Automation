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
max_page = 15
page_no = 0

while page_no < max_page:
    try:
        targeted_org = quick_wait.until(
            expected_conditions.presence_of_element_located((By.XPATH, "//h6[normalize-space()='Automated Test ORG']")))
        print(f'Found the targeted organization: {targeted_org.text}')
        break
    except:
        page_no += 1
        print(f'Moving to page: {page_no}')
        next_btn = quick_wait.until(
            expected_conditions.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next page']")))
        driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
        time.sleep(1)
        next_btn.click()
else:
    raise Exception("❌ Target organization not found.")

driver.find_element(By.XPATH, "(//div[@class='org-card-arrow'])[8]").click()
current_org_name = driver.find_element(By.CLASS_NAME, "client-org-name").text

# ======================================================================================================================

# Client form fillup
client_btn_text = driver.find_element(By.CLASS_NAME, "save-button").text
print(f'client btn: {client_btn_text}')
driver.find_element(By.CLASS_NAME, "save-button").click() #click the add new client

driver.find_element(By.CSS_SELECTOR, "input[name='name']").send_keys("Automated client 002")

driver.find_element(By.ID, "rc_select_0").click()
driver.find_element(By.XPATH, "//div[@title='English']").click()

driver.find_element(By.ID, "rc_select_1").click()
driver.find_element(By.XPATH, "//div[text()='Modern - popular user experience style comprised of 3D elements']").click()

# Wait for the modal body
modal_body = wait.until(expected_conditions.presence_of_element_located((By.CLASS_NAME, "ant-modal-body")))

# Scroll to bottom of modal
driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal_body)

# Wait for the button to be clickable
save_button = wait.until(expected_conditions.element_to_be_clickable((By.CLASS_NAME, "custom-save-btn")))
# save_button.click()

time.sleep(3)