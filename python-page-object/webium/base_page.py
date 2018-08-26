__maintained__ = 'jacob@vsee.com'

import os
import sys
import datetime
import time
from PIL import Image
from io import BytesIO
import logging
import calendar

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException, ElementNotVisibleException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains

from core.robot.pyrobot import Robot, Keyboard
from driver import get_driver
from driver import close_driver
from driver import open_at

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from scenarios.util.support import TARGET
from scenarios.util.support import mkdir
from scenarios.util.logger import setup_logger
from scenarios.util.logger import LogTests

from scenarios.util.setting import _capture_mode
from scenarios.util.setting import _url
from scenarios.util.setting import _wait_timeout
from scenarios.util.setting import _webdriver_driver
from scenarios.util.setting import _project_name
from scenarios.util.setting import _take_screenshot_driver_exception

def get_timestamp():
    return datetime.datetime.now().strftime("%Y-%d-%m  %H:%M:%S")

def get_epoc():
    return str(calendar.timegm(time.gmtime())/60)

def Test( locator=None):
    import inspect
    def loc(func):
        def func_wrapper(*args, **kwargs):
            class_name = args[0].__class__.__name__
            value = None
            if len(args) > 1:
                value = args[1]
            # web driver
            _driver = get_driver()
            
            className = str(inspect.getfile(args[0].__class__)).split("features")[1] \
                            .replace("pyc", "").replace("py", "") \
                            .replace("/", ".").replace("\\", ".").replace("..", "") + class_name

            with LogTests(className, func.__name__, locator, value=value, _driver=_driver):
                return func(*args, **kwargs)
        return func_wrapper
    return loc
class BasePage():

    url = None

    @property
    def _driver(self):
        if self.driver_:
            return self.driver_
        return get_driver()

    def __init__(self, driver=None, url=None):
        if url:
            self.url = url
        self.driver_ = driver
        self.testID = sys.argv[1]  # test case ID
        mkdir(self.testID)
        setup_logger('report', TARGET + 'report_{0}.log'.format(get_epoc()), level=logging.DEBUG)    # report logger
        self.logger = logging.getLogger('report')

    def find_element(self, *args):
        try:
            return self._driver.find_element(*args)
        except(TimeoutException, NoSuchElementException, StaleElementReferenceException,
               ElementNotVisibleException, ElementNotInteractableException) as e:
            self.capture_screenshot("find_element")
            raise Exception(self.logger.debug("[TEST FAILED]: The element located by {0}: '{1}' need to check".format(*args)))

    def capture_screenshot(self,value):
        if not _take_screenshot_driver_exception: return
        if 'FOR_FAILURES' == _capture_mode or 'AFTER_EACH_STEP' == _capture_mode:
            image_name = "FALSE_" + value + str(datetime.datetime.now()).replace("-", "").replace(" ", "").replace(":", "") + ".png"
            path_pic = TARGET + image_name
            # create an instance of the class
            robot = Robot()
            im = robot.take_screenshot()
            # Save the PIL Image to disk
            im.save(path_pic, 'png')

    def find_elements(self, *args):
        return self._driver.find_elements(*args)

    def get_text_values(self, *locator):
        items = [x for x in self.find_elements(*locator)]
        list_value = []
        for item in items:
            list_value.append(item.text)
        return list_value

    def size(self):
        return len(self.find_elements(self._by, self._value))

    def is_present(self):
        if self.size()>0:
            return True
        else:
            return False

    def is_visible(self):
        if self.find_element(self._by, self._value).is_displayed():
            return True
        else:
            return False

    def open(self):
        if self.url:
            self._driver.get(self.url)
        else:
            open_at()
    
    def open_url(self, url):
        self._driver.get(url)
        return self

    def close(self):
        close_driver()

    def element(self, *locator):
        self._by = locator[0]
        self._value = locator[1]
        return self

    def wait_until_clickable(self, timeout = _wait_timeout):
        try:
            wait = WebDriverWait(self._driver, timeout)
            wait.until(EC.element_to_be_clickable((self._by, self._value)))
            if self._driver.capabilities['browserName'] == 'chrome':
                time.sleep(1)
            return self
        except(TimeoutException, NoSuchElementException):
            self.capture_screenshot("waitUntilClickable")
            raise Exception(
                self.logger.debug(
                    "[TEST FAILED]:TimeoutException - Timed out after "
                    + str(timeout)
                    + " seconds waiting for clickable of element located by {0}: '{1}' ".format(self._by,self._value)))

    def wait_until_visible(self, timeout = _wait_timeout):
        try:
            wait = WebDriverWait(self._driver, timeout)
            wait.until(EC.visibility_of_element_located((self._by, self._value)))
            if self._driver.capabilities['browserName'] == 'chrome':
                time.sleep(1)
            return self
        except(TimeoutException, ElementNotVisibleException):
            self.capture_screenshot("waitUntilVisible")
            raise Exception(
                self.logger.debug(
                    "[TEST FAILED]: ElementNotVisibleException - Timed out after "
                    + str(timeout)
                    + " seconds waiting for visibility of element located by {0}: '{1}' ".format(self._by, self._value)))

    def wait_until_invisible(self, timeout = _wait_timeout):
        try:
            wait = WebDriverWait(self._driver, timeout)
            wait.until_not(EC.visibility_of_element_located((self._by, self._value)))
            return self
        except(TimeoutException):
            self.capture_screenshot("waitUntilNotVisible")
            raise Exception(
                self.logger.debug(
                    "[TEST FAILED]: TimeoutException - Timed out after "
                    + str(timeout)
                    + " seconds waiting for invisibility of element located by {0}: '{1}' ".format(self._by, self._value)))

    def wait_until_present(self, timeout = _wait_timeout):
        try:
            wait = WebDriverWait(self._driver, timeout)
            wait.until(EC.presence_of_element_located((self._by, self._value)))
            if self._driver.capabilities['browserName'] == 'chrome':
                time.sleep(1)
            return self
        except(TimeoutException, Exception):
            self.capture_screenshot("waitUntilPresent")
            raise Exception(
                self.logger.debug(
                    "[TEST FAILED]: TimeoutException - Timed out after "
                    + str(timeout)
                    + " seconds waiting for present of element located by {0}: '{1}'".format(self._by, self._value)))

    def wait_until_not_present(self, timeout = _wait_timeout):
        try:
            wait = WebDriverWait(self._driver, timeout)
            wait.until_not(EC.presence_of_element_located((self._by, self._value)))
            return self
        except(TimeoutException, Exception):
            self.capture_screenshot("waitUntilNotPresent")
            raise Exception(
                self.logger.debug(
                    "[TEST FAILED]: TimeoutException - Timed out after "
                    + str(timeout)
                    + " seconds waiting for not present of element located by {0}: '{1}' ".format(self._by, self._value)))

    def wait_for_text_to_appear(self, text, timeout = _wait_timeout):
        try:
            wait = WebDriverWait(self._driver, _wait_timeout)
            wait.until(EC.text_to_be_present_in_element((self._by, self._value), text))
            return self
        except(TimeoutException, Exception):
            self.capture_screenshot("waitForTextToAppear")
            raise Exception(
                self.logger.debug(
                    "[TEST FAILED]: TimeoutException - Timed out after "
                    + str(timeout)
                    + " seconds waiting for Text to appear of element located by {0}: '{1}'".format(self._by, self._value)))

    def click(self):
        self.find_element(self._by, self._value).click()
        return self

    def get_width(self):
        element = self.find_element(self._by, self._value).size
        return element.get("width")

    def get_height(self):
        element = self.find_element(self._by, self._value).size
        return element.get("height")

    def click_and_wait(self, timeout=3):
        self.find_element(self._by, self._value).click()
        self.wait_a_bit(timeout)
        return self

    def type(self, value):
        self.find_element(self._by, self._value).send_keys(value)
        return self

    def type_and_wait(self, value, timeout=3):
        self.find_element(self._by, self._value).send_keys(value)
        self.wait_a_bit(timeout)
        return self

    def implicitly_wait(self, *args):
        return self._driver.implicitly_wait(*args)

    def get_title(self):
        return self._driver.title

    def enter_text_into(self, value, *locator):
        self.find_element(*locator).send_keys(value)
        return self

    def get_text_value(self):
        return self.find_element(self._by, self._value).text

    def get_value(self):
        return self.get_attribute_value("value")

    # Using for td tag
    def get_text_by_innerhtml(self):
        return self.find_element(self._by, self._value).get_attribute("innerHTML")
    
    def get_text_by_value(self):
        return self.find_element(self._by, self._value).get_attribute("value")

    def clear(self):
        self.find_element(self._by, self._value).clear()
        return self

    def click_on_element(self, *locator):
        self.find_element(*locator).click()
        return self

    def get_source_html(self):
        return self._driver.page_source
    
    def get_current_url(self):
        return self._driver.current_url

    def accept_alert(self, alert_text=""):
        if self._driver.capabilities['browserName'] == 'chrome':
                time.sleep(1)
        try:
            WebDriverWait(self._driver, 30)\
                .until(EC.alert_is_present(), 'Timed out waiting for PA creation confirmation popup to appear.')
        except TimeoutException:
            self.capture_screenshot("no_alert")

        popup = self._driver.switch_to.alert
        if alert_text != "":
            msg = "Verify alert text equals: {0}".format(alert_text)
            self.logger.debug('{0} [INFO]  : {1}'.format(get_timestamp(), msg))
            if popup.text != alert_text:
                msg = "Alert text is: {0} - doesn't match".format(popup.text())
                self.logger.debug('{0} [INFO]  : {1}'.format(get_timestamp(), msg))
        popup.accept()
        return self
    
    def dismiss_alert(self, alert_text=""):
        if self._driver.capabilities['browserName'] == 'chrome':
                time.sleep(1)
        try:
            WebDriverWait(self._driver, 30)\
                .until(EC.alert_is_present(), 'Timed out waiting for PA creation confirmation popup to appear.')
        except TimeoutException:
            self.capture_screenshot("dismiss_alert")

        popup = self._driver.switch_to.alert
        if alert_text != "":
            msg = "Verify alert text equals: {0}".format(alert_text)
            self.logger.debug('{0} [INFO]  : {1}'.format(get_timestamp(), msg))
            if popup.text != alert_text:
                msg = "Alert text is: {0} - doesn't match".format(popup.text)
                self.logger.debug('{0} [INFO]  : {1}'.format(get_timestamp(), msg))
        popup.dismiss()
        return self

    def select_option_by_text(self, value):
        Select(self.find_element(self._by, self._value)).select_by_visible_text(value)
        return self

    def select_option_by_value(self, value):
        Select(self.find_element(self._by, self._value)).select_by_value(value)
        return self

    def select_option_by_index(self, value):
        Select(self.find_element(self._by, self._value)).select_by_index(value)
        return self

    def get_selected_visible_text_value(self):
        return Select(self.find_element(self._by, self._value)).first_selected_option.get_attribute("innerText")

    def get_selected_value(self):
        return Select(self.find_element(self._by, self._value)).first_selected_option.get_attribute("value")

    def get_all_options(self):
        all_opts = []
        options = Select(self.find_element(self._by, self._value)).options
        for opt in options:
            all_opts.append(opt.get_attribute("innerText").strip())
        return all_opts

    def type_and_enter(self, value, *locator):
        self.find_element(*locator).send_keys(value + Keys.ENTER)
        return self

    def type_and_tab(self, value, *locator):
        self.find_element(*locator).send_keys(value + Keys.TAB)
        return self

    def get_attribute_value(self, attribute):
        return self.find_element(self._by, self._value).get_attribute(attribute)

    def get_driver(self):
        return self._driver

    def get_url(self):
        if self.url:
            return self.url
        else:
            return _url
    
    def refresh_page(self):
        self._driver.refresh()
        return self

    def is_checked(self):
        """
        Check the radio or checkbox status
        :return:
            None: If the object is unchecked
            true: If the object is checked
        """
        return self.get_attribute_value("checked")

    def check(self):
        if self.is_checked() is None:
            self.click()
        return self

    def un_check(self):
        if self.is_checked() is not None:
           self.click()
        return self

    def evaluate_javascript(self, js, *args):
        self._driver.execute_script(js,*args)

    def get_project_name(self):
        """
        Should be put the title of email that is sent by application:
        Example: Welcome to CEP OnDuty
        """
        return _project_name

    def get_webdriver_driver(self):
        """
        :return: name of browser
        """
        return _webdriver_driver

    def highlight_element(self):
        element = self.find_element(self._by, self._value)
        def apply_style(s):
            self.evaluate_javascript("arguments[0].setAttribute('style', arguments[1]);", element, s)
        original_style = self.get_attribute_value('style')
        apply_style("background: yellow; border: 2px solid red;")
        time.sleep(.3)
        apply_style(original_style)
        return self

    def scroll_element_into_view(self):
        element = self.find_element(self._by, self._value)
        self.evaluate_javascript("return arguments[0].scrollIntoView();", element)
        time.sleep(.3)
        return self
    
    def scroll_to_end_page(self):
        self.evaluate_javascript("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        return self

    def upload_file(self,pathfile):
        self.wait_a_bit(5)
        robot = Robot()
        robot.clear_clipboard()
        robot.add_to_clipboard(pathfile)
        robot.paste()
        robot.sleep(1)
        self.press_enter()
        self.wait_a_bit(5)
        return self

    def press_enter(self):
        robot = Robot()
        robot.sleep(1)
        robot.key_press(Keyboard.enter)
        return self

    def press_tab(self):
        robot = Robot()
        robot.sleep(1)
        robot.key_press(Keyboard.tab)
        return self

    def then(self, desc):
        """ Make scripts more readable"""
        return self

    def then_answers_are(self):
        """ Make scripts more readable"""
        return self

    def give_question_that(self, desc):
        """ Make scripts more readable"""
        return self

    def wait_a_bit(self, seconds):
        time.sleep(seconds)
        return self

    def switch_to_new_window(self):
        self.default_window = self._driver.window_handles[0]
        window_after = self._driver.window_handles[1]

        # switch on to new child window
        self._driver.switch_to_window(window_after)
        return self

    def switch_default_window(self):
        self._driver.switch_to_window(self.default_window)
        return self

    def close_active_window(self):
        self._driver.close()
        return self

    def capture_element(self,image_name):

        png = self._driver.get_screenshot_as_png()  # saves screenshot of entire page

        location = self.find_element(self._by, self._value).location
        size = self.find_element(self._by, self._value).size

        im = Image.open(BytesIO(png))  # uses PIL library to open image in memory

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        im = im.crop((left, top, right, bottom))  # defines crop points
        im.save(TARGET+image_name+'.png')  # saves new cropped image
        return self

    def go_back_and_wait(self, steps):
        step = str(steps)
        self.evaluate_javascript("window.history.go({0})".format(step))
        self.wait_a_bit(3)
        return self

    def move_to_and_click(self):
        element = self._driver.find_element(self._by, self._value)
        actions = ActionChains(self._driver)
        actions.click(element)
        actions.perform()
        return self

    def click_on(self):
        element = self.find_element(self._by, self._value)
        self.evaluate_javascript("arguments[0].click();", element)
        return self
