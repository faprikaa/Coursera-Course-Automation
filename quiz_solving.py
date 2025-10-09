import json
import time
import traceback

import requests
from openai.lib.azure import API_KEY_SENTINEL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
from dotenv import load_dotenv
import os

from CourseHandler import CourseHandler
from QuizSolver import QuizSolver
from helpers import check_course_url_type, get_sylabbus_link, get_user_id

load_dotenv()

COOKIES = os.getenv("COOKIES")
QUIZ_URL = "https://www.coursera.org/learn/dot-net-full-stack-foundation/assignment-submission/4pAaF/architecture-cli-practice-quiz"
API_KEY=os.getenv("API_KEY")
MODEL=os.getenv('API_MODEL')
BASE_URL=os.getenv("API_BASE_URL", "https://api.openai.com/v1")
COURSE_URLS = os.getenv("COURSE_URLS")
USER_ID = None


driver = webdriver.Chrome()
driver.get("https://www.coursera.org/")
driver.maximize_window()
WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="rendered-content"]'))
)

cookies = json.loads(COOKIES)
session = requests.Session()

for cookie in cookies:
    cookie.pop("sameSite", None)
    session.cookies.set(cookie["name"], cookie["value"])
    driver.add_cookie(cookie)

driver.refresh()

USER_ID = get_user_id(driver)

auth_info_menu_button = driver.find_element(By.XPATH, '//*[@id="authenticated-info-menu"]/div/button')
nama = auth_info_menu_button.get_attribute("aria-label").replace("User dropdown menu for ", "")
print(f"Logged in as {nama} with user id {USER_ID}")

client = OpenAI(
    api_key=API_KEY if API_KEY != API_KEY_SENTINEL else None,
    base_url=BASE_URL
)

quiz_solver = QuizSolver(driver, client, model=MODEL)

course_urls = COURSE_URLS.split(",")
try:
    for course_url in course_urls:
        if check_course_url_type(course_url) == "professional_certificate":
            print(f"Processing professional certificate: {course_url.strip()}\n")
            driver.get(course_url.strip())
            time.sleep(1)
            syllabus_links = get_sylabbus_link(driver)
            for syllabus_link in syllabus_links:
                course_url = syllabus_link
                print(f"Processing syllabus: {course_url.strip()}\n")
                course_handler = CourseHandler(driver, course_url, quiz_solver, USER_ID, session)
        else:
            course_handler = CourseHandler(driver, course_url.strip(), quiz_solver, USER_ID, session )
except Exception as e:
    tb_str = traceback.format_exc()
    print(tb_str)
    input("Press Enter to continue...")


quiz_solver.solve_quiz(QUIZ_URL)


input = input("Done")
