__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from util.logger import Test


class MyClinicPage(BasePage):
    select_room = (By.XPATH, "//a/span[.='Select Waiting Room']")
    des_area = (
        By.XPATH, "//label[text()='Room Description']/following-sibling::div//div[@class='note-editing-area']")
    add_new_btn = (By.XPATH, '//div[@id="ConsultationTypes"]/a[contains(@data-bind,"click:add")]')
    visit_des =(
        By.XPATH,"//*[@id='ConsultationTypes']//tbody/tr[last()]/td/input[@data-bind='value: description']")
    visit_duration = (
        By.XPATH, "//*[@id='ConsultationTypes']//tbody/tr[last()]/td/input[@data-bind='value: duration']")
    update_btn = (
        By.XPATH, "//*[@data-bind='enable: roomCode, click: updateRoomDetails']")
    alert_mesg = (By.XPATH, "//*[@class='alert alert-success fade in']")

    @Test(select_room)
    def select_waiting_room(self, room):
        self.element(*self.select_room).click().type(room).type_and_wait(Keys.TAB, 1)
        return self

    @Test(des_area)
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

    @Test(add_new_btn)
    def click_on_add_new_visit_option(self):
        self.element(*self.add_new_btn).highlight_element().click()
        return self

    @Test(visit_des)
    def enter_visit_option(self, des_option):
        self.element(*self.visit_des).highlight_element().type(des_option)
        return self

    @Test(visit_duration)
    def enter_duration(self, duration):
        self.element(*self.visit_duration).highlight_element().clear().type(duration)
        return self

    @Test(update_btn)
    def click_on_update(self):
        self.element(*self.update_btn).highlight_element().click_and_wait(2)
        return self

    def get_alert_message(self):
        return self.element(*self.alert_mesg).get_text_value()
