from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_course_url_type(url):
    if "coursera.org/learn/" in url:
        return "course"
    elif "coursera.org/professional-certificates/" in url:
        return "professional_certificate"
    else:
        return "unknown"

def get_sylabbus_link(driver):
    sylabbus_links = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-e2e="sdp-course-list-link"]'))
    )
    return [sylabbus_link.get_attribute("href") for sylabbus_link in sylabbus_links]

def get_user_id(driver):
    keys = driver.execute_script("""
    const keys = [];
    for (let i = 0; i < localStorage.length; i++) {
      keys.push(localStorage.key(i));
    }
    return keys;
    """)

    target_key = None
    for k in keys:
        if k.endswith(".userPreferences") or k.endswith("~LearnerGoals_DailyGoalUnlockPersonalizedTrackerToastSeen"):
            target_key = k
            break

    return target_key.replace(".userPreferences", "").replace("~LearnerGoals_DailyGoalUnlockPersonalizedTrackerToastSeen", "")
