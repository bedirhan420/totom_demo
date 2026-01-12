from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 1. Open a website showing dynamic loading (Example)
driver.get("https://the-internet.herokuapp.com/dynamic_loading/1")

# 2. Click the 'Start' button
# Using regular find_element because the button is already there
driver.find_element(By.CSS_SELECTOR, "#start button").click()

# 3. EXPLICIT WAIT DEFINITION
# We define a wait object with a 10-second timeout limit
wait = WebDriverWait(driver, 10)

try:
    # 4. Wait for the loading bar to disappear AND the text to be visible
    # condition: visibility_of_element_located
    finish_text_element = wait.until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )

    print("Success! The element appeared.")
    print(f"Text found: {finish_text_element.text}")

except:
    print("Error! The element did not appear within 10 seconds.")

finally:
    driver.quit()
