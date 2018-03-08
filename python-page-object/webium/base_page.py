import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from types import MethodType
from waiting import TimeoutExpired
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

import settings
from driver import get_driver
from wait import wait
from errors import WebiumException


def is_element_present(self, element_name, just_in_dom=False, timeout=0):
    def _get_driver():
        try:
            driver = getattr(self, '_driver')
        except AttributeError:
            driver = getattr(self, 'parent', None)
        if driver:
            return driver
        return get_driver()

    _get_driver().implicitly_wait(timeout)
    try:
        def is_displayed():
            try:
                element = getattr(self, element_name)
            except AttributeError:
                raise WebiumException('No element "{0}" within container {1}'.format(element_name, self))
            if isinstance(element, list):
                if element:
                    return all(ele.is_displayed() for ele in element)
                else:
                    return False
            return element.is_displayed()

        is_displayed() if just_in_dom else wait(lambda: is_displayed(), timeout_seconds=timeout)
        return True
    except WebDriverException:
        return False
    except TimeoutExpired:
        return False
    finally:
        _get_driver().implicitly_wait(settings.implicit_timeout)

import ConfigParser

class EnvironmentVariables():

    global _config

    def __init__(self, properties="D:\\vsee-space\\eVisitRegression\\selenium\\scenarios\\oneclick\\vsee.properties"):
        self. _config = ConfigParser.RawConfigParser()
        self. _config.read(properties)

    def _property(self, session, option):
        return self._config.get(session, option)


    # Webdriver properties
    def base_url(self):
        return self._property('webdriver', 'webdriver.base.url')


    def webdriver_driver(self):
        return self._property('webdriver', 'webdriver.driver')


    def firefox_driver(self):
        return self._property('webdriver', 'webdriver.firefox.driver')


    def chrome_driver(self):
        return self._property('webdriver', 'webdriver.chrome.driver')


class BasePage():
    set_env = EnvironmentVariables()
    url = set_env.base_url()
    webdriver_driver = set_env.webdriver_driver()


    @property
    def _driver(self):
        if self.__driver:
            return self.__driver
        return get_driver()

    def __init__(self, driver=None, url=None):
        if url:
            self.url = url
        self.__driver = driver
        self.is_element_present = MethodType(is_element_present, self)

    def open(self):
        if not self.url:
            raise WebiumException('Can\'t open page without url')
        self._driver.get(self.url)

    def find_element(self, *args):
        return self._driver.find_element(*args)

    def find_elements(self, *args):
        return self._driver.find_elements(*args)

    def implicitly_wait(self, *args):
        return self._driver.implicitly_wait(*args)


    def get_title(self):
        print "[INFO]: Title page : " + self._driver.title
        return self._driver.title


    def element(self, *locator):
        return self._driver.find_element(*locator)


    def enterTextInto(self, value, *locator):
        print "[INFO]: Fill  [" + value + "] " + " into (" + locator[0] + ", " + locator[1] + ")"
        self.element(*locator).send_keys(value)


    def clickOnElement(self, *locator):
        print "[INFO]: click on (" + locator[0] + ", " + locator[1] + ")"
        self.element(*locator).click()

    def getSourceHTML(self):
        return  self._driver.page_source

    def acceptAlert(self):
        try:
            WebDriverWait(self._driver, 30).until(EC.alert_is_present(),
                                            'Timed out waiting for PA creation ' +
                                            'confirmation popup to appear.')
        except TimeoutException:
            print("no alert")

        #Provider will be deleted. Are you sure?
        popup = self._driver.switch_to.alert
        print "[INFO]: Alert message: " + popup.text
        popup.accept()
