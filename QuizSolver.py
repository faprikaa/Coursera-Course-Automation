import json
import random
import time

from selenium.common import ElementClickInterceptedException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def print_qas(qas):
    for index,qa in enumerate(qas, 1):
        answers_string = ", ".join(a["text"] for a in qa["answers"])
        print(f"Question {index} : {qa['question']}")
        print(f"Answers: {answers_string}")


def create_prompt(qas):
    prompt = "You are an expert in .NET Core. For each question, choose the most correct answer and explain why briefly."
    prompt += " Dont give any explanation. Only give like formatted answer\n\n"
    for i, qa in enumerate(qas, 1):
        prompt += f"Question {i}: {qa['question']}\n"
        for j, ans in enumerate(qa['answers'], 1):
            answer = ans["text"]
            prompt += f"{j}. {answer}\n"
        prompt += "\n"
    prompt += "Return the answers in exactly like this format:\n"
    prompt += '[{"question": 1, "selected_option": 2}, ...]'
    return prompt


class QuizSolver:

    def __init__(self, driver, client, model):
        self.driver = driver
        self.client = client
        self.model = model

    def solve_quiz(self, quiz_link):
        self.driver.get(quiz_link)
        start_button = WebDriverWait(self.driver, 30).until(
            EC.visibility_of_element_located((By.XPATH,
                                              '//*[@id="main-container"]/div[1]/div/div/div/div/div/div/div/div[2]/div[2]/div[2]/div[2]/div/div/div/button'))
        )
        try:
            start_button.click()
        except ElementClickInterceptedException as  e:
            self.try_close_dialog()
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            start_button.click()


        confirm_new_attempt_button = self.driver.find_elements(By.CSS_SELECTOR, 'button[data-testid="StartAttemptModal__primary-button"]')
        if confirm_new_attempt_button:
            confirm_new_attempt_button[0].click()

        questions = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-testid="part-Submission_MultipleChoiceQuestion"]'))
        )
        qas = []
        for question in questions:
            question_text = question.find_element(By.CSS_SELECTOR, 'div[data-testid="cml-viewer"]').text

            answers = question.find_elements(By.CLASS_NAME, "rc-Option")
            answer_texts = []
            for answer in answers:
                checkbox = answer.find_element(By.CSS_SELECTOR, "label")
                answer_texts.append({"checkbox": checkbox, "text": answer.text})

            qas.append({"question": question_text, "answers": answer_texts})

        prompt = create_prompt(qas)
        response = self.ask_ai(prompt)
        for index, rsp in enumerate(response, 0):
            selected_option = rsp["selected_option"] - 1
            checkbox = qas[index]["answers"][selected_option]["checkbox"]
            try:
                checkbox.click()
            except Exception as e:
                print(e)
                input("Press Enter to continue...")
            time.sleep(random.randint(1, 5))

        agreement_checkbox = self.driver.find_element(By.ID, 'agreement-checkbox-base')
        if not agreement_checkbox.is_selected(): # Check if not already selected
            agreement_checkbox.click()

        name_input = WebDriverWait(self.driver, 15).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, 'input[aria-label="Enter your legal name"]')
        ))
        name_input.clear()
        name_input.send_keys("Muammar Mufid")

        submit_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="submit-button"]'))
        )
        submit_button.click()

        dialog_submit_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[data-testid="dialog-submit-button"]'))
        )
        dialog_submit_button.click()

        grade_parent = WebDriverWait(self.driver, 60).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-testid="AssignmentViewTopBanner"]'))
        )
        grade = grade_parent.find_element(By.TAG_NAME, "span").text
        print(f"Quiz completed with grade: {grade}")

        next_item_button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[data-testid="TopBannerCTAButton"]'))
        )
        try:
            next_item_button.click()
        except ElementClickInterceptedException:
            close_dialog_btn = self.driver.find_elements(By.XPATH, '//*[@id="cds-react-aria4856666153-:rh:"]/div[3]/div/div/div[1]/button')
            if close_dialog_btn:
                close_dialog_btn[0].click()
                time.sleep(1)
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
            next_item_button.click()





    def ask_ai(self, prompt, max_retries=3):
        """Ask the AI model with retry logic."""
        for attempt in range(1, max_retries + 1):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system",
                         "content": "You are a .NET expert who answers multiple-choice questions accurately."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )
                return json.loads(response.choices[0].message.content)

            except Exception as e:
                print(f"[Attempt {attempt}] Error: {e} Line {e.__traceback__.tb_lineno}")
                if attempt == max_retries:
                    raise  # re-raise after final failure
                time.sleep(2)  # wait a bit before retrying

    def try_close_dialog(self):
        time.sleep(random.randint(2, 5))
        honor_code_dialog = self.driver.find_elements(By.XPATH, '//*[@id="cds-react-aria7791273047-:r19:"]/div[3]/div/div/div[2]/div[3]/div/button')
        if honor_code_dialog:
            honor_code_dialog[0].click()
            time.sleep(1)

