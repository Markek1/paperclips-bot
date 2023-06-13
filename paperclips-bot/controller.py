from selenium import webdriver
from selenium.webdriver.common.by import By

from history import State, History


class Controller:
    MIN_FUNDS = 30.0

    def __init__(self, driver):
        self.driver = driver
        self.btnMakePaperclip = driver.find_element(By.ID, "btnMakePaperclip")
        self.btnLowerPrice = driver.find_element(By.ID, "btnLowerPrice")
        self.btnRaisePrice = driver.find_element(By.ID, "btnRaisePrice")

        self.btnBuyWire = driver.find_element(By.ID, "btnBuyWire")

        self.btnMakeClipper = driver.find_element(By.ID, "btnMakeClipper")

    def next(self, history: History):
        self.btnMakePaperclip.click()

        state: State = history[-1]

        if state.wire == 0:
            self.btnBuyWire.click()

        # Spend money
        if state.funds > self.MIN_FUNDS:
            self.btnMakeClipper.click()
