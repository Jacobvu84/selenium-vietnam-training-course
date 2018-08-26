__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webium.base_page import BasePage
from scenarios.resource import user_dir

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test


class CommonAction(BasePage):

    def click_on_update_by_name(self, name):
        item_xpath = "//strong[text()='{0}']/following-sibling::a[text()='Update']".format(name)
        item = (By.XPATH, item_xpath)
        self.element(*item).click()

    def click_on_cancel_by_name(self, name):
        item_xpath = "//strong[text()='{0}']/following-sibling::a[text()='Cancel']".format(name)
        item = (By.XPATH, item_xpath)
        self.element(*item).click()

    # need update
    def click_on_add_button_by_name(self, name):
        item_xpath = "//h4[text()='{0}']/ancestor-or-self::div[@class='modal-header']/" \
                     "following-sibling::div[@class='modal-body']//button[@data-bind='click: add']".format(name)
        item = (By.XPATH, item_xpath)
        self.element(*item).click()

    def check_item_by_text(self, value):
        item_xpath = "//td[contains(text(),'{0}')]/preceding-sibling::td/span".format(value)
        item = (By.XPATH, item_xpath)
        self.element(*item).click_and_wait(2)

    def get_all_item_by_id(self, id):
        list_items = (By.XPATH, "//div[@id='{0}']/following-sibling::ul/li".format(id))
        return self.get_text_values(*list_items)

    def enter_text_filed_by_label(self, value, label):
        input_field = (By.XPATH, "//label[text()='{0}']/following-sibling::div/input".format(label))
        self.element(*input_field).type(value)
        return self


class PatientHealthInforPage(CommonAction):

    hr_field = (By.NAME, 'vital_heart_rate')
    bp_field = (By.NAME, 'vital_blood_pressure')
    temp_field = (By.NAME, 'vital_temperature')
    rr_field = (By.NAME, 'vital_rr')
    height_field = (By.NAME, 'vital_height')
    weight_field = (By.NAME, 'vital_weight')
    spo2_field = (By.NAME, 'vital_spo2')
    glucose_field = (By.NAME, 'vital_glucose')
    upload_field = (By.LINK_TEXT, "Click Here")


    @Test(hr_field)
    def enter_hr(self, hr):
        self.element(*self.hr_field).wait_until_present().type(hr)
        return self

    @Test(bp_field)
    def enter_bp(self, bp):
        self.element(*self.bp_field).type(bp)
        return self

    @Test(temp_field)
    def enter_temp(self, temp):
        self.element(*self.temp_field).type(temp)
        return self

    @Test(rr_field)
    def enter_rr(self, rr):
        self.element(*self.rr_field).type(rr)
        return self

    @Test(height_field)
    def enter_height(self, height):
        if "" != height:
            self.element(*self.height_field).type(height)
        return self

    @Test(weight_field)
    def enter_weight(self, weight):
        if "" != weight:
            self.element(*self.weight_field).type(weight)
        return self

    def enter_spO2(self, value):
        if "" != value:
            self.element(*self.spo2_field).type(value)
        return self

    def enter_glucose(self, value):
        if "" != value:
            self.element(*self.glucose_field).type(value)
        return self

    @Test(upload_field)
    def upload(self, upload, path_file):
        if upload == 'yes':
            path_pic = user_dir + "\\images\\" + path_file
            self.element(*self.upload_field).click_and_wait()
            self.upload_file(path_pic)
        return self

    def click_on_update_past_medical_history(self):
        self.click_on_update_by_name("Past Medical History")
        return self

    def click_on_update_past_surgeries(self):
        self.click_on_update_by_name("Past Surgeries")
        return self

    def click_on_cancel_past_medical_history(self):
        self.click_on_cancel_by_name("Past Medical History")
        return self

    def click_on_cancel_past_surgeries(self):
        self.click_on_cancel_by_name("Past Surgeries")
        return self

    def click_on_conditions(self, condition):
        self.check_item_by_text(condition)
        return self

    def get_conditions(self):
        return self.get_all_item_by_id("Past Medical HistoryList")

    def click_on_procedures(self, condition):
        self.check_item_by_text(condition)
        return self

    def get_procedures(self):
        return self.get_all_item_by_id("Past SurgeriesList")

    def click_on_update_medications(self):
        self.click_on_update_by_name("Medications")
        return self

    @Test()
    def click_on_cancel_medications(self):
        self.click_on_cancel_by_name("Medications")
        return self

    def enter_medications(self, medication):
        self.enter_text_filed_by_label(medication, "Name of Medication")
        add_btn = (By.XPATH,
                   "//label[text()='Name of Medication']"
                   "/ancestor-or-self::form[@class='form-horizontal']/div[2]//button[text()='Add']")
        self.element(*add_btn).click()
        return self

    def get_medications(self):
        return self.get_all_item_by_id("MedicationsList")

    def click_on_update_allergies(self):
        self.click_on_update_by_name("Allergies")
        return self

    @Test()
    def click_on_cancel_allergies(self):
        self.click_on_cancel_by_name("Allergies")
        return self

    def enter_allergies(self, drugs):
        item_input = (By.XPATH, "//label[text()='Name of Drug']/following-sibling::div/div//input")
        self.element(*item_input).highlight_element().type(drugs).type(Keys.ENTER).type(Keys.TAB)

        add_btn = (By.XPATH,
                   "//label[text()='Name of Drug']"
                   "/ancestor-or-self::form[@class='form-horizontal']/div[2]//button[text()='Add']")
        self.element(*add_btn).click()
        return self

    def get_drug_name(self):
        return self.get_all_item_by_id("AllergiesList")