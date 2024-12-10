import os
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import time

class ClassInfo:
    def __init__(self):
        self.class_name = ""
        self.average_score = 0
        self.quest_list = [] #each_quest = {"title":"", "category":"", "due":"", "score":""}



load_dotenv()

is_test = False

with open('grade.csv', 'w') as file:
    file.write("title,average,quest\n")


if not is_test:

    user = os.environ.get("USER_NAME")
    pw = os.environ.get("PASSWORD")

    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get("https://accesscenter.roundrockisd.org/HomeAccess/Account/LogOn?ReturnUrl=%2fhomeaccess%2f")

    time.sleep(1)

    # Logon
    user_name = driver.find_element(By.ID, value="LogOnDetails_UserName")
    user_name.send_keys(user)

    time.sleep(1)

    password = driver.find_element(By.ID, value="LogOnDetails_Password")
    password.send_keys(pw, Keys.ENTER)

else:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(options=options)
    driver.get("http://127.0.0.1:5000/")

time.sleep(2)

table_rows = driver.find_elements(By.CSS_SELECTOR, value="table.sg-homeview-table tbody tr")

for row in table_rows:
    new_score = ClassInfo()
    class_info = row.text.split('\n')
    if class_info[0].find('Lunch') >= 0 or class_info[0].find('Advisory') >= 0:
        continue

    new_score.class_name = class_info[0]
    new_score.average_score = class_info[3]

    assignment_list = row.find_elements(By.CSS_SELECTOR, value="td div div span.sg-assignment-description")
    if len(assignment_list) > 0:
        for item in assignment_list:
            each_quest = {}
            quest = item.get_attribute("title")
            try:
                score = item.find_element(By.CSS_SELECTOR, value="span").text
            except NoSuchElementException:
                score = "-/-" #not scored yet

            # need to get Title, Category and Due date from quest
            split_temp = quest.split('\n')
            data = []
            for content in split_temp:
                data.append(content.split(':')[1].strip())

            each_quest["title"] = data[1]
            each_quest["category"] = data[2]
            each_quest["due"] = data[3]
            each_quest["score"] = score

            new_score.quest_list.append(str(each_quest))


    with open("grade.csv",'a') as file:
        file.write(f"{new_score.class_name},{new_score.average_score}"
                   f",{','.join(new_score.quest_list)}\n")
        print(f"{new_score.class_name},{new_score.average_score}"
                   f",{','.join(new_score.quest_list)}")
