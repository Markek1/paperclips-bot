from collections import deque
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.by import By

from helpers import clean_num


@dataclass
class State:
    clips: int
    funds: float
    unsold: int
    wire: int


class Data:
    def __init__(self, name, element_id, type_) -> None:
        self.name = name
        self.element_id = element_id
        self.type = type_


to_track = [
    Data("clips", "clips", int),
    Data("funds", "funds", float),
    Data("unsold", "unsoldClips", int),
    Data("wire", "wire", int),
    Data("trust", "trust", int),
    Data("processors", "processors", int),
    Data("memory", "memory", int),
    Data("creativity", "creativity", int),
]


class History:
    MAX_TREND_LENGTH = 15

    def __init__(self, length):
        self.tick_num = 0
        self.length = length
        self.history = {}
        for data in to_track:
            self.history[data.name] = deque([0])
        self.trend = {}  # Average change in variables per tick
        for data in to_track:
            self.trend[data.name] = 0

    def update(self, driver):
        self.tick_num += 1

        for data in to_track:
            self.history[data.name].append(
                data.type(
                    clean_num(driver.find_element(By.ID, data.element_id).text)
                )
            )

        for data in to_track:
            trend = 0
            length = min(
                self.MAX_TREND_LENGTH, len(self.history[data.name]) - 1
            )
            if length == 0:
                break

            for i in range(1, length + 1):
                trend += (
                    self.history[data.name][-i]
                    - self.history[data.name][-i - 1]
                )
            self.trend[data.name] = trend / length

    def __getitem__(self, item):
        state = {}

        for data in to_track:
            state[data.name] = self.history[data.name][item]

        return state
