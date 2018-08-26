__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from webium.base_page import BasePage
from scenarios.resource import user_dir

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test


class PatientProfilePage(BasePage):
    edit_link = (By.XPATH, "//h4/a[@title='Edit']")
    update_btn = (By.ID, "UpdateProfile")
    photo = (By.NAME, "file")

    def get_profile_information_by_text(self, label):
        item_infor = "//h4[contains(text(),'Profile')]/" \
                     "following-sibling::div//dt[text()='{0}']/" \
                     "following-sibling::dd[1]".format(label)
        locator = (By.XPATH, item_infor)
        return self.element(*locator).wait_until_present().get_text_value()

    def edit_information_by_text(self, label, value):
        item_field = "//dt[text()='{0}']/following-sibling::dd[1]/p/input".format(label)
        locator = (By.XPATH, item_field)
        self.element(*locator).clear().type(value)
        return self

    def edit_information_by_option(self, label, option):
        item_field = "//dt[text()='{0}']/following-sibling::dd[1]/p/select".format(label)
        locator = (By.XPATH, item_field)
        self.element(*locator).select_option_by_text(option)
        return self

    def edit_bod_information(self, label, option):
        index = 0
        values = option.split(",")
        for value in values:
            index = index + 1
            item_field = "//dt[text()='{0}']/following-sibling::dd[1]/p/select[{1}]".format(label, index)
            locator = (By.XPATH, item_field)
            self.element(*locator).select_option_by_text(value)
        return self

    @Test(edit_link)
    def click_on_edit_button(self):
        self.element(*self.edit_link).wait_until_present().click_and_wait(2)
        return self

    @Test(update_btn)
    def click_on_update(self):
        self.element(*self.update_btn).wait_until_present().click_and_wait(3)
        return self

    @Test(photo)
    def upload_photo(self, upload, path_file):
        if upload == 'yes':
            path_pic = user_dir + "\\images\\" + path_file
            self.click_on_element(*self.photo).wait_a_bit(3)
            self.upload_file(path_pic)
        return self


class ProviderProfilePage(BasePage):
    edit_link = (By.ID, "edit-profile-link")
    update_btn = (By.XPATH, "//button[@class='form-btn-update btn btn-primary']")
    photo = (By.NAME, "file")
    cancel_form = (By.ID, "cancel-edit-profile")

    def get_profile_information_by_text(self, label):
        item_infor = "//div[@id='provider-profile-view']//dt[text()='{0}']/following-sibling::dd[1]".format(label)
        locator = (By.XPATH, item_infor)
        return self.element(*locator).wait_until_present().get_text_value()

    def edit_information_by_text(self, label, value):
        item_field = "//form[@id='ProviderAccountForm']//dt[text()='{0}']/following-sibling::dd[1]/p/input".format(
            label)
        locator = (By.XPATH, item_field)
        self.element(*locator).clear().type(value)
        return self

    def edit_information_by_textarea(self, label, value):
        item_field = "//form[@id='ProviderAccountForm']//dt[text()='{0}']/following-sibling::dd[1]/textarea".format(
            label)
        locator = (By.XPATH, item_field)
        self.element(*locator).clear().type(value)
        return self

    def edit_information_by_option(self, label, option):
        item_field = "//form[@id='ProviderAccountForm']//dt[text()='{0}']/following-sibling::dd[1]/p/select".format(
            label)
        locator = (By.XPATH, item_field)
        self.element(*locator).select_option_by_text(option)
        return self

    @Test(edit_link)
    def click_on_edit_button(self):
        self.element(*self.edit_link).wait_until_present().click_and_wait(2)
        return self

    @Test(update_btn)
    def click_on_update(self):
        self.element(*self.update_btn).wait_until_present().click_and_wait(3)
        return self

    @Test(cancel_form)
    def click_on_cancel(self):
        self.element(*self.cancel_form).wait_until_present().click_and_wait(3)

    @Test(photo)
    def upload_photo(self, upload, path_file):
        if upload == 'yes':
            path_pic = user_dir + "\\images\\" + path_file
            self.click_on_element(*self.photo).wait_a_bit(3)
            self.upload_file(path_pic)
        return self
