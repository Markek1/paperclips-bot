import time

from selenium import webdriver
from selenium.webdriver.common.by import By

from history import State, History
from controller import Controller

driver = webdriver.Chrome()
driver.get("https://www.decisionproblem.com/paperclips/index2.html")

btnMakePaperclip = driver.find_element(By.ID, "btnMakePaperclip")

history = History(10)
controller = Controller(driver)

while True:
    btnMakePaperclip.click()

    history.update(driver)
    controller.next(history)

    time.sleep(0.1)

driver.close()
