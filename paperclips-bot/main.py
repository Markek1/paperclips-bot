from selenium import webdriver
from selenium.webdriver.common.by import By

from history import History
from controllers import MainController
from visualizer import Visualizer, VisualizerState

driver = webdriver.Chrome()
driver.get("https://www.decisionproblem.com/paperclips/index2.html")

history = History(10)
controller = MainController(driver)
visualizer = Visualizer()

driver.execute_script("clips=10000;unsoldClips=10000;")
driver.implicitly_wait(0.1)

while True:
    history.update(driver)
    controller.next(driver, history)
    if visualizer.draw(history) == VisualizerState.QUIT:
        del visualizer
        break


driver.close()
