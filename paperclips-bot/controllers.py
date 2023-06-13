from dataclasses import dataclass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from history import State, History
from helpers import is_valid_btn


class ClipController:
    def __init__(self, driver):
        self.driver = driver
        self.btnMakePaperclip = driver.find_element(By.ID, "btnMakePaperclip")
        self.btnMakeClipper = driver.find_element(By.ID, "btnMakeClipper")

    def next(self, history: History, can_spend: bool):
        state = history[-1]

        if is_valid_btn(self.btnMakePaperclip):
            self.btnMakePaperclip.click()
        if can_spend and is_valid_btn(self.btnMakeClipper):
            self.btnMakeClipper.click()


class PriceController:
    def __init__(self, driver):
        self.btnLowerPrice = driver.find_element(By.ID, "btnLowerPrice")
        self.btnRaisePrice = driver.find_element(By.ID, "btnRaisePrice")

    def next(self, history: History):
        if history.tick_num % 3 != 0:
            return

        if not is_valid_btn(self.btnLowerPrice) or not is_valid_btn(
            self.btnRaisePrice
        ):
            return

        state = history[-1]

        if history.trend["clips"] > state["unsold"]:
            self.btnRaisePrice.click()
        elif state["unsold"] > abs(20 * history.trend["unsold"]):
            self.btnLowerPrice.click()
        elif history.trend["unsold"] < -0.2:
            self.btnRaisePrice.click()
        elif history.trend["unsold"] > 0.2:
            self.btnLowerPrice.click()


class WireController:
    def __init__(self, driver):
        self.btnBuyWire = driver.find_element(By.ID, "btnBuyWire")

    def next(self, history: History) -> bool:
        if not is_valid_btn(self.btnBuyWire):
            return True

        state = history[-1]

        # If we'll run out of wire in less than 100 ticks
        if state["wire"] + history.trend["wire"] * 100 <= 0:
            self.btnBuyWire.click()
            return False
        else:
            return True


@dataclass
class Project:
    def __init__(self, driver, element_id, title):
        self.id = element_id
        self.title = title
        self.button = driver.find_element(By.ID, element_id)

    def __repr__(self) -> str:
        return f"<Project {self.id}, {self.title}>"


class CompResController:

    PROC_MEM_RATIO = 1 / 4

    def __init__(self, driver):
        self.btnAddProc = driver.find_element(By.ID, "btnAddProc")
        self.btnAddMem = driver.find_element(By.ID, "btnAddMem")

        self.update_projects(driver)

    def update_projects(self, driver):
        try:
            js_projects = driver.find_elements(By.CLASS_NAME, "projectButton")
        except NoSuchElementException:
            js_projects = []

        self.projects = [
            Project(
                driver,
                project.get_attribute("id"),
                project.text,
            )
            for project in js_projects
        ]

    def next(self, driver, history: History):
        if history.tick_num % 30 == 0:
            self.update_projects(driver)

        state = history[-1]

        if state["trust"] > 0:
            if (
                is_valid_btn(self.btnAddProc)
                and state["processors"] < state["memory"] * self.PROC_MEM_RATIO
            ):
                self.btnAddProc.click()
            elif is_valid_btn(self.btnAddMem):
                self.btnAddMem.click()

        for project in self.projects:
            if is_valid_btn(project.button):
                disabled = project.button.get_attribute("disabled")
                if disabled is None:
                    project.button.click()
                    self.update_projects(driver)


class MainController:
    def __init__(self, driver):
        self.driver = driver

        self.can_spend = True

        self.clips_controller = ClipController(driver)
        self.price_controller = PriceController(driver)
        self.wire_controller = WireController(driver)
        self.comp_res_controller = CompResController(driver)

    def next(self, driver, history: History):
        self.can_spend = self.wire_controller.next(history)
        self.price_controller.next(history)
        self.clips_controller.next(history, self.can_spend)
        self.comp_res_controller.next(driver, history)
