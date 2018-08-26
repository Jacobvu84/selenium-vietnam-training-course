__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from scenarios.resource import user_dir
from scenarios.util.support import TARGET

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from util.logger import Test


class MySchedulePage(BasePage):
    create_btn = (By.ID, "ActionTypeCreateSlots")
    confirm_btn = (By.ID, "SlotAddButton")
    repeat_btn = (By.ID, "SlotRepeat")
    update_btn = (By.ID, "SlotUpdateButton")
    delete_btn = (By.ID, "SlotDeleteButton")
    dele_today = (By.ID, 'SlotGroupDeleteTodayButton')
    dele_group = (By.XPATH, '//a[text()="Delete All Slots in This Series"]')

    alert_mesg = (By.XPATH, "//div[@class='alert alert-success fade in']")
    clear_date = (By.XPATH, "//label[text()='When:']"
                            "/following-sibling::div//abbr[@class='select2-search-choice-close']")

    date_start = (By.NAME, "slot_date_start")
    date_end = (By.NAME, "slot_date_end")

    next_date_btn = (By.XPATH, "//span[@class='fc-button fc-button-next fc-state-default fc-corner-right']")
    prve_date_btn = (By.XPATH, "//span[@class='fc-button fc-button-prev fc-state-default fc-corner-left']")

    range_time_slot = (By.XPATH, "//div[@class='fc-event-time']")
    provider_name = (By.XPATH, "//div[@class='fc-event-title']")

    @Test(("Undefined", "Undefined"))
    def select_day(self, day):
        on_date = (By.XPATH, "//tr[@class='fc-first fc-last']/td[{0}]//div[@class='fc-day-content']".format(day))
        self.element(*on_date).highlight_element().click()
        return self

    @Test(("Undefined", "Undefined"))
    def select_time_to_edit(self, times):
        on_date = (By.XPATH, "//div[@class='fc-event-time' and text()='{0}']".format(times))
        self.element(*on_date).highlight_element().click().click_and_wait(5)
        elements = self.find_elements(*self.clear_date)
        for element in elements:
            element.click()
        return self

    @Test(("Undefined", "Undefined"))
    def select_time_to_delete(self, times):
        on_date = (By.XPATH, "//div[@class='fc-event-time' and text()='{0}']".format(times))
        self.element(*on_date).highlight_element().click().click_and_wait(5)
        return self

    @Test(("Undefined", "Undefined"))
    def select_day_on_next_week(self, day=3):
        self.element(*self.next_date_btn).highlight_element().click()
        on_date = (By.XPATH, "//tr[@class='fc-first fc-last']/td[{0}]//div[@class='fc-day-content']".format(day))
        self.element(*on_date).highlight_element().click()
        return self

    @Test(create_btn)
    def click_on_create_slots(self):
        self.element(*self.create_btn).click_and_wait(2)
        elements = self.find_elements(*self.clear_date)
        for element in elements:
            element.click()
        return self

    @Test(date_start)
    def set_date(self, day):
        """
        Set the day to start slot if you don't want to use date default today
        """
        self.element(*self.date_start).highlight_element().click().clear().type(day).type(Keys.TAB)
        return self

    @Test(date_end)
    def enter_end_date(self, day):
        """
        Set the day to end slot if you don't want to use date default today
        """
        self.element(*self.date_end).highlight_element().click().clear().type(day).type(Keys.TAB)
        return self

    @Test(confirm_btn)
    def click_on_confirm(self):
        self.element(*self.confirm_btn).click_and_wait(2)
        return self

    @Test(update_btn)
    def click_on_update(self):
        self.element(*self.update_btn).click_and_wait(5)
        return self

    @Test(delete_btn)
    def click_on_delete(self):
        self.element(*self.delete_btn).click_and_wait(5)
        return self

    @Test(dele_today)
    def click_on_delete_only_today_slot(self):
        self.element(*self.delete_btn).click()
        self.element(*self.dele_today).click_and_wait(2)
        return self

    @Test(dele_group)
    def click_on_delete_all_slot(self):
        self.element(*self.delete_btn).click()
        self.element(*self.dele_group).click_and_wait(2)
        return self

    @Test(("Undefined", "Undefined"))
    def set_start_time(self, start):
        start_time = (By.XPATH, "//span[text()='Start Time']")
        self.element(*start_time).highlight_element().click().type(start).type(Keys.ENTER)
        return self

    @Test(("Undefined", "Undefined"))
    def set_end_time(self, end):
        start_time = (By.XPATH, "//span[text()='End Time']")
        self.element(*start_time).highlight_element().click().type(end).type(Keys.ENTER)
        return self

    @Test(repeat_btn)
    def click_on_repeat(self):
        self.element(*self.repeat_btn).click()
        return self

    @Test(("Undefined", "Undefined"))
    def repeat_on_day(self, day):
        on_date = (By.XPATH, "//label[text()='Day of the week:']"
                             "/following-sibling::div/label[contains(.,'{0}')]".format(day))
        self.element(*on_date).click()
        return self

    @Test(alert_mesg)
    def get_alert_message(self):
        return self.element(*self.alert_mesg).get_text_value()

    @Test(range_time_slot)
    def get_range_time_of_slot(self):
        slots_date = []
        self.wait_a_bit(5)
        slots = self.find_elements(*self.range_time_slot)
        for slot in slots:
            slots_date.append(slot.text)
        return slots_date

    @Test(provider_name)
    def get_provider_name(self):
        return self.element(*self.provider_name).get_text_value()

    @Test(("Undefined", "Undefined"))
    def capture_calenda_legend(self, image_name):
        calenda_legend = (By.ID, 'calendarLegend')
        self.element(*calenda_legend).capture_element(image_name)
        return  TARGET+image_name+'.png'

    @Test(("Undefined", "Undefined"))
    def get_image_resource(self, file='calendarLegend.png'):
        path_pic = user_dir + "\\images\\" + file
        return path_pic
