import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from selenium.webdriver.remote.webelement import WebElement
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from jquery import JQuery


class Clickable(WebElement):

    def click(self, jquery=False):
        # type: (object) -> object
        """
        Click by WebElement, if not, JQuery click
        """
        if jquery:
            e = JQuery(self)
            e.click()
        else:
            super(Clickable, self).click()
