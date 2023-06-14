from collections import deque
from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.by import By

from helpers import clean_num


class Data:
    def __init__(self, name, element_id, type_) -> None:
        self.name = name
        self.element_id = element_id
        self.type = type_


TO_TRACK = [
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
    """Keeps track of the current state of variables and
    calculates the trend over the last MAX_TREND_LENGTH ticks."""

    MAX_TREND_LENGTH = 2

    def __init__(self, length):
        self.tick_num = 0
        self.length = length
        self.history = {}
        for data in TO_TRACK:
            self.history[data.name] = deque([0])

        self.trend_real = {}  # Average change in variables per tick
        for data in TO_TRACK:
            self.trend_real[data.name] = 0
        self.trend_percent = {}
        for data in TO_TRACK:
            self.trend_percent[data.name] = 0

    def update(self, driver):
        self.tick_num += 1

        for data in TO_TRACK:
            self.history[data.name].append(
                data.type(
                    clean_num(driver.find_element(By.ID, data.element_id).text)
                )
            )

        for data in TO_TRACK:
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
            self.trend_real[data.name] = trend / length
            self.trend_percent[data.name] = self.trend_real[data.name] / (
                self.history[data.name][-length - 1] + 1
            )

    def __getitem__(self, item):
        if type(item) == int:
            state = {}

            for data in TO_TRACK:
                state[data.name] = self.history[data.name][item]

        if type(item) == str:
            state = self.history[item]

        return state

    def __len__(self):
        return len(self.history["clips"])
