import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def random_username():
    return "user" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))

def log(msg):
    print(f"[INFO] {msg}")

def passlog(msg):
    print(f"[PASS] {msg}")

def run_tests():
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 15)

    try:
        # ---------------------------------------------------
        # 1. Homepage
        # ---------------------------------------------------
        driver.get("http://parabank.parasoft.com/")
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "logo")))
        passlog("Homepage loaded successfully")

        # ---------------------------------------------------
        # 2. Registration
        # ---------------------------------------------------
        log("Opening Register page...")
        driver.find_element(By.LINK_TEXT, "Register").click()

        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h1[contains(text(),'Signing up')]")
        ))
        passlog("Register page opened")

        uname = random_username()
        log(f"Registering with username: {uname}")

        driver.find_element(By.ID, "customer.firstName").send_keys("Test")
        driver.find_element(By.ID, "customer.lastName").send_keys("User")
        driver.find_element(By.ID, "customer.address.street").send_keys("123 Test Street")
        driver.find_element(By.ID, "customer.address.city").send_keys("Dubai")
        driver.find_element(By.ID, "customer.address.state").send_keys("DXB")
        driver.find_element(By.ID, "customer.address.zipCode").send_keys("00000")
        driver.find_element(By.ID, "customer.phoneNumber").send_keys("123456789")
        driver.find_element(By.ID, "customer.ssn").send_keys("9999")

        driver.find_element(By.ID, "customer.username").send_keys(uname)
        driver.find_element(By.ID, "customer.password").send_keys("password")
        driver.find_element(By.ID, "repeatedPassword").send_keys("password")

        log("Submitting registration...")
        driver.find_element(By.XPATH, "//input[@value='Register']").click()

        # Correct success message locator
        wait.until(EC.presence_of_element_located(
            (By.XPATH, "//h1[text()='Welcome'] | //p/b[contains(text(),'Welcome')]")
        ))
        passlog("Registration successful")

        print("\n🎉 ALL TESTS PASSED SUCCESSFULLY 🎉")

    except Exception as e:
        print("\n============ DEBUG OUTPUT ============")
        print(driver.page_source[:2000])
        print("======================================")
        raise e

    finally:
        driver.quit()


if __name__ == "__main__":
    run_tests()
