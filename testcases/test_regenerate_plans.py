from selenium import webdriver
from selenium.webdriver.common.by import By
import time

try:
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("http://127.0.0.1:8000/users/login/")
    driver.find_element(By.NAME, "username").send_keys("Guru12")
    driver.find_element(By.NAME, "password").send_keys("Prajwal@143")
    driver.find_element(By.TAG_NAME, "form").submit()
    time.sleep(2)
    driver.get("http://127.0.0.1:8000/profile/workout-plan/2/")
    workout_regen = driver.find_element(By.LINK_TEXT, "Regenerate Plan")
    driver.execute_script("arguments[0].scrollIntoView(true);", workout_regen)
    time.sleep(0.5)
    workout_regen.click()
    time.sleep(2)
    driver.get("http://127.0.0.1:8000/profile/diet-plan/2/")
    diet_regen = driver.find_element(By.LINK_TEXT, "Regenerate Plan")
    driver.execute_script("arguments[0].scrollIntoView(true);", diet_regen)
    time.sleep(0.5)
    diet_regen.click()
    time.sleep(2)
    driver.get("http://127.0.0.1:8000/logout/")
    time.sleep(1)

    print("Test passed!")

except Exception as e:
    print("Error during test:", str(e))

finally:
    driver.quit()
