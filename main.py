import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv

load_dotenv()

user = os.environ.get("USER_NAME")
pw = os.environ.get("PASSWORD")

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=options)
driver.get("https://accesscenter.roundrockisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f")

#Logon
user_name = driver.find_element(By.ID, value="LogOnDetails_UserName")
user_name.send_keys(user)

password = driver.find_element(By.ID, value="LogOnDetails_Password")
password.send_keys(pw, Keys.ENTER)




