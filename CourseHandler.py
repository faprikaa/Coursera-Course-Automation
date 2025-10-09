import random
import time

from selenium.common import ElementNotInteractableException, ElementClickInterceptedException, \
    StaleElementReferenceException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import lesson_type_handler


class CourseHandler:
    def __init__(self, driver, course_url, quiz_solver, user_id, session):
        self.driver = driver
        self.course_url = course_url
        self.quiz_solver = quiz_solver
        self.user_id = user_id
        self.session = session
        self.handle_course()


    def handle_course(self):
        wait = WebDriverWait(self.driver, 30)

        self.driver.get(self.course_url)

        course_title = self.go_to_course()
        print("Processing course: ", course_title)

        # Masuk ke halaman /lecture/
        # buka accordion pertama
        first_lesson_accordion = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "rc-ItemGroupLesson")))
        is_expanded = first_lesson_accordion.find_element(By.CLASS_NAME, "cds-AccordionHeader-button").get_attribute("aria-expanded")
        if is_expanded == "false":
            first_lesson_accordion.click()
        time.sleep(random.randint(1, 5))
        first_lesson = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'div[data-test="WeekSingleItemDisplay-lecture"] a')))
        first_lesson.click()

        modules = self.get_modules()
        all_lessons = []
        for module in modules:
            # expand semua module
            is_expanded = module.find_element(By.CLASS_NAME, "cds-AccordionHeader-button").get_attribute("aria-expanded")
            if is_expanded == "false":
                try:
                    module.click()
                except ElementClickInterceptedException as e:
                    ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
                    time.sleep(1)
                    module.click()

        for module in modules:
            self.try_close_dialog()
            # ambil semua li
            lessons = module.find_elements(By.TAG_NAME, "li")
            time.sleep(1)
            lesson_list = self.get_lessons_list(lessons)
            all_lessons.extend(lesson_list)
            time.sleep(1)

            print("===============")

        input("Press enter to continue...")
        input("Press enter to continue...")

    def go_to_course(self):
        enroll_button = self.driver.find_elements(By.CSS_SELECTOR, 'button[data-track-component="enroll_button"]')
        if enroll_button:
            print(f"Enrollment button: {enroll_button[0].text}")
            enroll_button[0].click()
        course_navigation = WebDriverWait(self.driver, 30).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[data-e2e="courseNavigation"]'))
        )
        title = course_navigation.find_element(By.TAG_NAME, 'h2')
        company = course_navigation.find_element(By.TAG_NAME, 'p')
        return title.text + company.text

    def get_modules(self):
        modules = WebDriverWait(self.driver, 30).until(
            EC.presence_of_all_elements_located((    By.XPATH,    '//*[@id="rendered-content"]/div/div/div/div/div[2]/div[1]/div/div[2]/div/div')        )
        )
        return modules

    def get_lessons_list(self, lessons):
        lesson_list = []
        for index, lesson in enumerate(lessons):
            lesson_dict = {}
            button = lesson.find_element(By.TAG_NAME, "a")
            href = button.get_attribute("href")
            parts = href.split("/")  # pecah berdasarkan '/'
            lesson_id = parts[6]  # indeks ke-5
            course_slug = parts[4]
            type_raw = lesson.find_element(By.XPATH, ".//div/a/div/div[2]/div[2]").text
            lesson_type = type_raw.split(".")[0].strip().lower()
            title = lesson.find_element(By.XPATH, ".//div/a/div/div[2]/div[1]").text
            is_done = lesson.find_elements(By.TAG_NAME, "circle")

            lesson_dict["element"] = lesson
            lesson_dict["button"] = button
            lesson_dict["title"] = title
            lesson_dict["type"] = lesson_type
            lesson_dict["is_done"] = True if is_done else False
            lesson_dict["lesson_id"] = None

            print(f"title: {lesson_dict['title']}. type: {lesson_dict['type']}. is_done: {lesson_dict['is_done']}")
            lesson_list.append(lesson_dict)

            if lesson_type == "video" and not is_done:
                print(f"Processing {lesson_id} video: {title}")
                lesson_type_handler.handle_video(lesson_id, course_slug, self.user_id, self.session)
                lesson_dict["is_done"] = True
                time.sleep(random.randint(1, 5))
            elif "assignment" in lesson_type and not is_done:
                print(f"Solving {lesson_id} assignment: {title}")
                self.quiz_solver.solve_quiz(href)
                lesson_dict["is_done"] = True
                self.driver.get(href)

                for attempt in range(3):
                    try:
                        profile_btn = WebDriverWait(self.driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="authenticated-info-menu"]/div/button')))
                        profile_btn.click()
                    except StaleElementReferenceException as e:
                        profile_btn = WebDriverWait(self.driver, 30).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="authenticated-info-menu"]/div/button')))
                        profile_btn.click()
                        time.sleep(2)

                time.sleep(random.randint(1, 5))

        return lesson_list

    def try_close_dialog(self):
        close_buttons = self.driver.find_elements(By.XPATH, '//*[@id="cds-react-aria2500801235-:r64:"]/div[3]/div/div/div[1]/button')
        if close_buttons:
            try:
                close_buttons[0].click()
            except ElementNotInteractableException as e:
                print("Dialog close button not interactable")


