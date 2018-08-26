__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from util.logger import Test


class NewVisitPage(BasePage):
    new_visit = (By.ID, "newVisitButton")
    room_sect = (By.XPATH, '//*[.="Select room..."]')
    patient_sect = (By.XPATH, '//*[.="Select patient ..."]')
    continue_btn = (By.XPATH, '//*[@data-bind="click: next"]')

    @Test(new_visit)
    def click_on_new_visit(self):
        self.element(*self.new_visit).wait_until_present().click_and_wait(5)
        return self

    @Test()
    def is_visit_type_present(self, value):
        visit_type = (By.XPATH, '//h4[.="Visit Type"]'
                                '/following-sibling::div/label[text()="{0}"]/input'.format(value))
        return self.element(*visit_type).is_present()

    def is_date_time(self, value):
        visit_type = (By.XPATH, '//h4[.="Date & Time"]'
                                '/following-sibling::div/label[contains(.,"{0}")]/input'.format(value))
        return self.element(*visit_type).is_present()

    @Test()
    def is_visit_type_active(self, value):
        visit_type = (By.XPATH, '//h4[.="Visit Type"]'
                                '/following-sibling::div/label[text()="{0}"]'.format(value))
        type_status = self.element(*visit_type).get_attribute_value("class")
        if "btn btn-primary active" == type_status:
            return True
        else:
            return False

    @Test()
    def is_date_time_active(self, value):
        visit_type = (By.XPATH, '//h4[.="Date & Time"]'
                                '/following-sibling::div/label[contains(.,"{0}")]'.format(value))
        type_status = self.element(*visit_type).get_attribute_value("class")
        if "btn btn-primary active" == type_status:
            return True
        else:
            return False

    @Test(room_sect)
    def select_room(self, room):
        self.click_on_element(*self.room_sect)
        input_data = (By.XPATH, '//*[@id="select2-drop"]/div/input')
        self.element(*input_data).wait_until_clickable()\
            .highlight_element()\
            .click().type_and_wait(room) \
            .type_and_wait(Keys.ENTER, 1)
        return self

    input_data = (By.XPATH, '//*[@id="select2-drop"]/div/input')
    new_patient = (By.LINK_TEXT, 'create a new patient')

    @Test(patient_sect)
    def select_patient(self, name):
        self.enter_patient_name(name)
        self.element(*self.input_data).type_and_wait(Keys.ENTER, 1)
        return self

    def enter_patient_name(self, name):
        self.click_on_element(*self.patient_sect)
        self.element(*self.input_data).wait_until_clickable()\
            .highlight_element()\
            .click().type_and_wait(name,timeout=5)
        return self

    @Test()
    def select_visit_type(self, vtype):
        if 'default' != vtype:
            visit_type = (By.XPATH, '//h4[.="Visit Type"]/following-sibling::div/label[text()="{0}"]/input'.format(vtype))
            self.element(*visit_type).highlight_element().click()
        return self

    @Test()
    def select_option(self, option):
        visit_option = (By.XPATH, '//*[.="{0}"]/ancestor-or-self::td/preceding-sibling::td/input'.format(option))
        self.element(*visit_option).highlight_element().click()
        return self

    @Test()
    def select_date_time(self, opt, date="", timer=""):
        date_time = (By.XPATH, '//h4[.="Date & Time"]/following-sibling::div/label[contains(.,"{0}")]'.format(opt))
        self.element(*date_time).highlight_element().click()
        if 'Schedule for a later time' == opt:
            self.enter_date_time(date, timer)
        return self

    chart_number = (By.NAME, "encounter_number")
    medical_number = (By.NAME, "MRN")
    insurance_type = (By.NAME, "insurance_type")
    note_provider = (By.NAME, "note_to_provider")

    @Test(chart_number)
    def enter_encounter_number(self, number):
        if "" != number:
            self.element(*self.chart_number).type(number)
        return self

    @Test(medical_number)
    def enter_medical_record_number(self, number):
        if "" != number:
            self.element(*self.medical_number).type(number)
        return self

    @Test(insurance_type)
    def select_insurance_type(self, insurance_type):
        if "" != insurance_type:
            self.element(*self.insurance_type).select_option_by_text(insurance_type)
        return self

    @Test(note_provider)
    def enter_information_to_provider(self, note):
        if "" != note:
            self.element(*self.note_provider).type(note)
        return self

    @Test(continue_btn)
    def go_to_continue(self):
        self.element(*self.continue_btn).highlight_element().click_and_wait()
        return self

    @Test()
    def enter_date_time(self, date, timer):
        date_input = (By.XPATH, '//input[contains(@data-bind,"startDate")]')
        self.element(*date_input).highlight_element().clear().type(date)
        time_input = (By.XPATH, '//input[contains(@data-bind,"startDate")]/following-sibling::input')
        self.element(*time_input).highlight_element().clear().type(timer)
        return self

    def get_visit_type(self):
        element = (By.XPATH, "//dt[text()='Visit Type']/following-sibling::dd[1]")
        return self.element(*element).get_text_value()

    def get_visit_option(self):
        element = (By.XPATH, "//dt[text()='Visit Option']/following-sibling::dd[1]")
        return self.element(*element).get_text_value()

    def get_date_time(self, date_time):
        if "Now" in date_time:
            element = (By.XPATH, "//dt[text()='Date & Time']/following-sibling::dd[1]/span")
        else:
            element = (By.XPATH, "//dt[text()='Date & Time']/following-sibling::dd[1]/span[2]")
        return self.element(*element).get_text_value()

    def get_patient_name(self):
        element = (By.XPATH, "//dt[text()='Patient Name']/following-sibling::dd[1]")
        return self.element(*element).get_text_value()

    def get_encounter_number(self):
        element = (By.XPATH, "//dt[text()='Encounter number (Chart number)']/following-sibling::dd[1]")
        return self.element(*element).get_text_value()

    def get_medical_record_number(self):
        element = (By.XPATH, "//dt[text()='Medical record number']/following-sibling::dd[1]")
        return self.element(*element).get_text_value()

    def get_insurance_type(self):
        element = (By.XPATH, "//dt[text()='Insurance type']/following-sibling::dd[1]")
        return self.element(*element).get_text_value()

    def get_information_for_provider(self):
        element = (By.XPATH, "//dt[text()='Information for Provider']/following-sibling::dd[1]")
        return self.element(*element).get_text_value()

    confirm_btn = (By.XPATH, "//button[@data-loading-text='Processing...']")

    @Test(confirm_btn)
    def click_on_confirm(self):
        self.element(*self.confirm_btn).highlight_element().click_and_wait(5)

    @Test()
    def accept_go_to_detail_page(self, alert_text, option):
        if 'yes' == option:
            self.accept_alert(alert_text).wait_a_bit(5)
        else:
            self.dismiss_alert(alert_text).wait_a_bit(5)
        return self

    @Test(new_patient)
    def create_new_patient(self, name):
        self.enter_patient_name(name)
        self.element(*self.new_patient).click()
        return self

    @Test()
    def enter_first_name(self, value):
        element = (By.NAME, 'first_name')
        self.element(*element).highlight_element().clear().type(value)
        return self

    @Test()
    def enter_last_name(self, value):
        element = (By.NAME, 'last_name')
        self.element(*element).highlight_element().clear().type(value)
        return self

    @Test()
    def enter_email(self, value):
        element = (By.NAME, 'email')
        self.element(*element).highlight_element().clear().type(value)
        return self

    @Test()
    def select_gender(self, value):
        element = (By.XPATH, "//span[text()='{0}']/preceding-sibling::input".format(value))
        self.element(*element).highlight_element().click()
        return self

    month_dob_nurse = (By.XPATH, "//select[@class='form-control month']")
    day_dob_nurse = (By.XPATH, "//input[@class='form-control day']")
    year_dob_nurse = (By.XPATH, "//input[@class='form-control year']")

    def enter_month_of_birth(self, month):
        self.element(*self.month_dob_nurse).select_option_by_value(month)
        return self

    def enter_day_of_birth(self, day):
        self.element(*self.day_dob_nurse).type(day)
        return self

    def enter_year_of_birth(self, year):
        self.element(*self.year_dob_nurse).type(year)
        return self

    @Test()
    def enter_date_of_birth(self, dob):
        _dob = dob.split("-")
        self.enter_month_of_birth(_dob[1])
        self.enter_day_of_birth(_dob[2])
        self.enter_year_of_birth(_dob[0])
        return self

    @Test()
    def click_on_create_button(self):
        element = (By.XPATH, "//input[@value='Create']")
        self.element(*element).highlight_element().click_and_wait(5)
        return self