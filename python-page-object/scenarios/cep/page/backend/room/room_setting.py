__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test


class RoomSettingPage(BasePage):
    setting_tab = (By.XPATH, "//a[@href='#roomSettings']")
    add_btn = (By.XPATH, "//div[@id='ConsultationTypes']/a[contains(.,'Add New Visit Option')]")
    des_text = (By.XPATH, "//div[@id='ConsultationTypes']//table/tbody/tr[last()]/td[1]/input")
    duration_text = (By.XPATH, "//div[@id='ConsultationTypes']//table/tbody/tr[last()]/td[2]/input")
    update_btn = (By.XPATH, "//button[@type='submit']")
    close_btn = (By.XPATH, "//*[@id='AddRoomForm']//h4[text()='Room Details']/preceding-sibling::button")
    alert_msg = (By.XPATH, "//ul[@id='roomTabs']/preceding-sibling::div")
    des_area = (
        By.XPATH, "//label[text()='Room Description']/following-sibling::div//div[@class='note-editing-area']")
    # Room setting
    @Test(setting_tab)
    def click_on_room_settings_tab(self):
        self.element(*self.setting_tab).wait_until_clickable().click()
        return self

    @Test(add_btn)
    def click_on_add_new_visit_option(self):
        self.element(*self.add_btn).scroll_element_into_view().highlight_element().click()
        return self

    @Test(des_text)
    def enter_visit_description(self, value):
        self.element(*self.des_text).clear().type(value)
        return self

    @Test(duration_text)
    def enter_duration(self, value):
        self.element(*self.duration_text).clear().type(value)
        return self

    @Test(update_btn)
    def click_on_update(self):
        self.element(*self.update_btn).click_and_wait()
        return self

    @Test(close_btn)
    def close_form(self):
        self.element(*self.close_btn).click()
        return self

    @Test(alert_msg)
    def get_alert_message(self):
        return self.element(*self.alert_msg) \
            .wait_for_text_to_appear('Success! Update room details successfully') \
            .get_text_value()

    def enter_room_description(self, comment):
        self.element(*self.des_area).highlight_element().click().wait_a_bit(2)
        self.evaluate_javascript("window.scrollTo(0, document.body.scrollHeight)")
        if 'firefox' == self.get_driver().name:
            self.get_driver().find_element_by_tag_name('body').send_keys(comment)
            self.wait_a_bit(5)
        else:
            self.get_driver().switch_to.active_element.send_keys(comment)
            self.wait_a_bit(5)
        return self
