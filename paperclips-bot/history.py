from collections import deque
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.by import By

from helpers import clean_num


@dataclass
class State:
    paperclips: int
    funds: int
    unsold: int
    wire: int


class History:
    def __init__(self, n):
        self.n = n
        self.history = deque(maxlen=n)

    def update(self, driver):
        state = State(
            paperclips=int(
                clean_num(driver.find_element(By.ID, "clips").text)
            ),
            funds=float(clean_num(driver.find_element(By.ID, "funds").text)),
            unsold=int(
                clean_num(driver.find_element(By.ID, "unsoldClips").text)
            ),
            wire=int(clean_num(driver.find_element(By.ID, "wire").text)),
        )
        self.history.append(state)

    def __getitem__(self, item):
        return self.history[item]
