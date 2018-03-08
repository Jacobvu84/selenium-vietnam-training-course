__author__ = 'jacob@vsee.com'

import os,sys, time
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from webium import BasePage
from webium import Find, Finds

class LoginPage(BasePage):
    # override base url
    # url = 'http://www.google.com'

    """Usage 01:
    user_field = Find(by=By.ID, value='AppUserUsername')
    def enter_username(self, username):
        self.user_field.sendkeys(username)

    pass_field = Find(by=By.ID, value='AppUserPassword')
    def enter_password(self, pwd):
        self.pass_field.sendkeys(pwd)

    submit_button = Find(by=By.XPATH, value='//button[contains(text(),"Sign In")]')
    def click_on_submit_button(self):
        self.submit_button.click()
        time.sleep(5)
    """

    # Open url on the browser and maximize window
    """Usage 01:"""
    def visit(self):
        self.open()

    USERNAME_TEXT = (By.ID, 'AppUserUsername')
    def enter_username(self, username):
        self.enterTextInto(username, *self.USERNAME_TEXT)

    PASSWORD_TEXT = (By.ID, 'AppUserPassword')
    def enter_password(self, pwd):
        self.enterTextInto(pwd, *self.PASSWORD_TEXT)

    SUBMIT_BUTTON = (By.XPATH, '//button[contains(text(),"Sign In")]')
    def click_on_submit_button(self):
        self.clickOnElement(*self.SUBMIT_BUTTON)
        time.sleep(5)

    def get_title_page(self):
        return self.get_title()