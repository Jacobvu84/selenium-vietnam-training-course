__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from util.logger import Test


class ControlPanelPage(BasePage):
    @Test()
    def click_on_video_call(self):
        """Something click on the video call doesn't work well"""
        video_call = (By.XPATH, "//*[@id='VisitsDetail']//a[@data-action='Visit.call']")
        linkdownload = (By.XPATH, "//a[@class='install-vsee' and text()='click here to install VSee']")
        self.element(*video_call).wait_until_clickable() \
            .highlight_element().click_and_wait(2)

        while not self.element(*linkdownload).wait_until_present().is_present():
            self.element(*video_call).click()
        return self

    @Test()
    def click_on_chat(self):
        chat = (By.CSS_SELECTOR, ".btn.btn-info")
        self.element(*chat).wait_until_clickable().highlight_element().click_and_wait(3)
        return self

    @Test()
    def is_in_a_call(self):
        in_a_call = (By.XPATH, "//span[@class='vsee_status vsee_presence_inacall']")
        if self.element(*in_a_call).wait_until_present().is_present():
            return True
        else:
            return False

    def is_online(self):
        online = (By.XPATH, "//span[@class='vsee_status vsee_presence_available']")
        if self.element(*online).wait_until_present().is_present():
            return True
        else:
            return False

