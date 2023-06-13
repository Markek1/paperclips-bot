import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from history import History
from controllers import MainController

driver = webdriver.Chrome()
driver.get("https://www.decisionproblem.com/paperclips/index2.html")

btnMakePaperclip = driver.find_element(By.ID, "btnMakePaperclip")

history = History(10)
controller = MainController(driver)

driver.execute_script("clips=100000;unsoldClips=100000;")
driver.implicitly_wait(0.1)

while True:
    btnMakePaperclip.click()

    history.update(driver)
    controller.next(driver, history)

    time.sleep(0.1)


driver.close()
