from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as webdriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.get("https://the-internet.herokuapp.com/")

#Find Element
element = driver.find_element(By.ID, "content")
print(element.text) 

#wait
wait = webdriverWait(driver, 10)
element = wait.until(EC.presence_of_element_located((By.ID, "content")))

#Interact with Element
element.click()
element.send_keys("Selenium Test")
element.clear()

#Screenshot
driver.save_screenshot("screenshot.png")