__author__ = 'jacob@vsee.com'

import os
import sys
from waiting import wait

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test

class MenuBarPage(BasePage):

    menu_lelf = (By.XPATH, "//div[@id='top_menu-navbar-collapse']/ul[@class='nav navbar-nav navbar-left']/li")

    @Test()
    def is_menu_active(self, menu):
        menu_item = (By.XPATH, "//ul[@class='nav navbar-nav navbar-left']//a[text()='{0}']"
                                "/ancestor-or-self::li".format(menu))
        tab_status = self.element(*menu_item).get_attribute_value("class")

        if "active" == tab_status:
            return True
        else:
            return False

    @Test()
    def is_item_present(self, menu):
        menu_item = (By.XPATH, "//ul[@class='nav navbar-nav navbar-left']/li/a[.='{0}']".format(menu))
        return self.element(*menu_item).is_present()

    @Test()
    def get_all_menu_items(self):
        return self.get_text_values(*self.menu_lelf)


