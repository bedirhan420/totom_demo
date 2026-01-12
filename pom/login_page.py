from selenium.webdriver.common.by import By

class LoginPage:
    # 1. Constructor: Driver'ı test dosyasından alır
    def __init__(self, driver):
        self.driver = driver
        
    # 2. Locators: Elementlerin adresleri burada tutulur
    # Sayfa değişirse sadece burayı güncellersiniz.
    username_box = (By.ID, "user-name")
    password_box = (By.ID, "password")
    login_button = (By.NAME, "login-button")
    
    # 3. Actions: Sayfada yapılabilecek aksiyonlar
    def enter_username(self, username):
        self.driver.find_element(*self.username_box).send_keys(username)
        
    def enter_password(self, password):
        self.driver.find_element(*self.password_box).send_keys(password)
        
    def click_login(self):
        self.driver.find_element(*self.login_button).click()
