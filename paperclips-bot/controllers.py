from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from history import History
from helpers import is_valid_btn


class ClipController:
    """Builds clips and buys auto-clippers."""

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
    """Tries to keep the price of clips at the most profitable level."""

    # Used to limit the frequency of price changes
    PERIOD = 2

    def __init__(self, driver):
        self.btnLowerPrice = driver.find_element(By.ID, "btnLowerPrice")
        self.btnRaisePrice = driver.find_element(By.ID, "btnRaisePrice")

    def next(self, history: History):
        state = history[-1]

        if state["unsold"] < 2 * history.trend_real["clips"]:
            if is_valid_btn(self.btnRaisePrice):
                self.btnRaisePrice.click()
        elif (
            state["unsold"] > 30 * history.trend_real["clips"]
            and history.trend_percent["unsold"] > -0.02
        ):
            if is_valid_btn(self.btnLowerPrice):
                self.btnLowerPrice.click()
        elif history.tick_num % self.PERIOD != 0:
            return
        elif is_valid_btn(self.btnRaisePrice) and (
            history.trend_real["unsold"] + history.trend_real["clips"]
            < history.trend_real["clips"]
        ):
            self.btnRaisePrice.click()
        elif is_valid_btn(self.btnLowerPrice) and (
            history.trend_real["unsold"] + history.trend_real["clips"]
            > history.trend_real["clips"] * 0.5
        ):
            self.btnLowerPrice.click()


class WireController:
    """Buys wire and gives a signal to stop spending when we're running out"""

    def __init__(self, driver):
        self.btnBuyWire = driver.find_element(By.ID, "btnBuyWire")

    def next(self, history: History) -> bool:
        state = history[-1]

        if state["wire"] + history.trend_real["wire"] * 100 <= 0:
            if is_valid_btn(self.btnBuyWire):
                self.btnBuyWire.click()
            return False
        else:
            return True


class Project:
    def __init__(self, driver, element_id, title):
        self.id = element_id
        self.title = title
        self.button = driver.find_element(By.ID, element_id)

    def __repr__(self) -> str:
        return f"<Project {self.id}, {self.title}>"


class CompResController:
    """Builds processors and memory when trust is available and buys every project it can."""

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
            return

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
