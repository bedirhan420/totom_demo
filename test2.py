from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Setup driver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# 1. Navigate to the website
url = "https://www.python.org/"
driver.get(url)
print(f"Navigated to {url}")

# --- ASSERTION 1: Check Page Title ---
# We expect the title to be exactly 'Welcome to Python.org'
expected_title = "Welcome to Python.org"
actual_title = driver.title

# If actual_title is NOT equal to expected_title, the code stops and prints the error message.
assert actual_title == expected_title, f"Title Check Failed! Expected: '{expected_title}', Got: '{actual_title}'"

print("Assertion 1 Passed: Page title is correct.")

# --- ASSERTION 2: Check Element Visibility ---
# Verify that the search bar is displayed on the page
search_bar = driver.find_element(By.NAME, "q")

# is_displayed() returns True or False
is_visible = search_bar.is_displayed()

assert is_visible == True, "Assertion 2 Failed: Search bar is not visible!"

print("Assertion 2 Passed: Search bar is visible.")

# --- ASSERTION 3: Check Element Text ---
# Verify the 'Donate' button text
donate_button = driver.find_element(By.CLASS_NAME, "donate-button")
button_text = donate_button.text

# We assert that 'Donate' word exists in the button text
assert "Donate" in button_text, f"Assertion 3 Failed: 'Donate' text not found in {button_text}"

print("Assertion 3 Passed: Donate button text is correct.")

# Teardown
driver.quit()
