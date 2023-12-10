import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By

# options to keep the browser open
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)

# logging
service = webdriver.ChromeService(log_output=subprocess.STDOUT)

# Set up the Chrome web driver
driver = webdriver.Chrome(options=options, service=service)

# Navigate to the LinkedIn login page
driver.get('https://www.linkedin.com/login')

# wait for the page to load
time.sleep(2)

username = driver.find_element(By.ID, 'username')
username.send_keys('musicmusiq@live.com')

password = driver.find_element(By.ID, 'password')
password.send_keys('Th3wayto12!')
password.submit()

