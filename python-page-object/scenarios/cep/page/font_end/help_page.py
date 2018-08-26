__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test
from util.assertions import Assert


class HelpPage(BasePage, Assert):
    modal_title = (By.XPATH, "//div[@id='contactsModal']//h4[@class='modal-title']")
    body_des = (By.XPATH, "//div[@id='contactsModal']//div[@class='modal-body']/p")
    contact_options = (By.XPATH, "//div[@id='contactsModal']//div[@class='modal-body']/ol/li")
    close_form = (By.XPATH, "//div[@id='contactsModal']//div[@class='modal-footer']/button[text()='Close']")

    @Test()
    def get_title_help_page(self):
        return self.element(*self.modal_title).wait_until_present().get_text_value()

    @Test()
    def get_body_description(self):
        return self.get_text_values(*self.body_des)

    @Test()
    def get_contact_options(self):
        return self.get_text_values(*self.contact_options)

    @Test()
    def click_on_close(self):
        self.element(*self.close_form).click()
