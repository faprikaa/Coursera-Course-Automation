import json

from openai.lib.azure import API_KEY_SENTINEL
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openai import OpenAI
from dotenv import load_dotenv
import os

from QuizSolver import QuizSolver
load_dotenv()

COOKIES = os.getenv("COOKIES")
QUIZ_URL = "https://www.coursera.org/learn/dot-net-full-stack-foundation/assignment-submission/4pAaF/architecture-cli-practice-quiz"
API_KEY=os.getenv("API_KEY")
MODEL=os.getenv('API_MODEL')
BASE_URL=os.getenv("API_BASE_URL", "https://api.openai.com/v1")

driver = webdriver.Chrome()
driver.get("https://www.coursera.org/")
driver.maximize_window()
WebDriverWait(driver, 30).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="rendered-content"]'))
)

cookies = json.loads(COOKIES)

for cookie in cookies:
    cookie.pop("sameSite", None)
    driver.add_cookie(cookie)

driver.refresh()
auth_info_menu_button = driver.find_element(By.XPATH, '//*[@id="authenticated-info-menu"]/div/button')
nama = auth_info_menu_button.get_attribute("aria-label").replace("User dropdown menu for ", "")
print(f"Logged in as {nama}")

client = OpenAI(
    api_key=API_KEY if API_KEY != API_KEY_SENTINEL else None,
    base_url=BASE_URL
)

quiz_solver = QuizSolver(driver, client, model=MODEL)
quiz_solver.solve_quiz(QUIZ_URL)

input = input("Done")
