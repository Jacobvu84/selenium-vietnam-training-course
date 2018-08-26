__author__ = 'jacob@vsee.com'

import os
import sys
from waiting import wait

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webium.base_page import BasePage
from scenarios.resource import user_dir

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test
from util.assertions import Assert


class NursePage(BasePage, Assert):
    # Please enter patient information
    first_name_nurse = (By.XPATH, "//div[@id='ParamedicsPatientSearch']//input[@name='first_name']")
    last_name_nurse = (By.XPATH, "//div[@id='ParamedicsPatientSearch']//input[@name='last_name']")
    month_dob_nurse = (By.ID, "jsonform-2-elt-dob_month")
    day_dob_nurse = (By.ID, "jsonform-2-elt-dob_day")
    year_dob_nurse = (By.ID, "jsonform-2-elt-dob_year")
    next_button = (By.XPATH, "//div[@class='panel-footer clearfix']/a[@data-bind='click: doSearch']")

    chart_number = (By.NAME, "encounter_number")
    medical_number = (By.NAME, "MRN")
    insurance_type = (By.NAME, "insurance_type")

    new_patient = (By.XPATH, "//a[contains(.,'Create new patient record')]")
    continue_patient = (By.XPATH, "//a[contains(.,'Continue as selected patient')]")

    exit_btn = (By.XPATH, "//button[@data-bind='click: $root.endSession']")
    confirm = (By.NAME, 'telemedicine_consent')

    @Test(first_name_nurse)
    def enter_first_name_nurse(self, fname):
        self.element(*self.first_name_nurse).wait_until_present().type(fname)
        return self

    @Test(last_name_nurse)
    def enter_last_name_nurse(self, lname):
        self.element(*self.last_name_nurse).type(lname)
        return self

    def enter_month_of_birth(self, month):
        # self.element(*self.month_dob_nurse).select_option_by_text(month)
        self.element(*self.month_dob_nurse).select_option_by_value(month)
        return self

    def enter_day_of_birth(self, day):
        self.element(*self.day_dob_nurse).type(day)
        return self

    def enter_year_of_birth(self, year):
        self.element(*self.year_dob_nurse).type(year)
        return self

    @Test()
    def enter_month_of_admission(self, month):
        month_admission = (By.ID, "jsonform-4-elt-first_admission_month")
        self.element(*month_admission).select_option_by_value(month)
        return self

    @Test()
    def enter_day_of_admission(self, day):
        day_doadmission = (By.ID, "jsonform-4-elt-first_admission_day")
        self.element(*day_doadmission).type(day)
        return self

    @Test()
    def enter_year_of_admission(self, year):
        year_admission = (By.ID, "jsonform-4-elt-first_admission_year")
        self.element(*year_admission).type(year)
        return self

    @Test()
    def enter_date_of_birth(self, dob):
        _dob = dob.split("-")
        self.enter_month_of_birth(_dob[1])
        self.enter_day_of_birth(_dob[2])
        self.enter_year_of_birth(_dob[0])
        return self

    @Test()
    def enter_date_of_most_recent_admission(self, dob):
        _dob = dob.split("-")
        self.enter_month_of_admission(_dob[1])
        self.enter_day_of_admission(_dob[2])
        self.enter_year_of_admission(_dob[0])
        return self

    @Test()
    def enter_principal_diagnosis_upon_admission_to_the_facility(self, values):
        text_field = (By.XPATH, "//label[text()=\"What is the patient's principal diagnosis upon admission to the facility?\"]"
                            "/following-sibling::input")
        symptoms = values.split(",")
        for symptom in symptoms:
            self.element(*text_field).wait_until_clickable() \
                .highlight_element().type(symptom).type(Keys.ENTER).type(Keys.TAB)
        return self

    reason = (By.XPATH, "//label[text()='Reason for visit']/following-sibling::input")
    @Test(reason)
    def enter_reason_for_visit(self, reasons):
        symptoms = reasons.split(",")
        for symptom in symptoms:
            self.element(*self.reason).wait_until_clickable() \
                .highlight_element().type(symptom).type(Keys.ENTER).type(Keys.TAB)
        return self

    @Test()
    def choose_option_to_improve(self, options):
        symptoms = options.split(",")
        for symptom in symptoms:
            my_idea = (By.XPATH, "//span[contains(text(),'{0}')]/preceding-sibling::input".format(symptom))
            self.element(*my_idea).wait_until_clickable() \
                .highlight_element().click()
        return self

    def click_on_submit(self):
        sbmit_btn = (By.XPATH, "//*[@id='IntakeSurvey']//a[text()='Submit']")
        self.element(*sbmit_btn).click()

    @Test(confirm)
    def click_on_confirm(self):
        self.element(*self.confirm).check()
        return self

    @Test()
    def select_gender(self, gender):
        gender_check = (By.XPATH, "//span[text()='{0}']/preceding-sibling::input[@name='gender']".format(gender))
        self.element(*gender_check).wait_until_present().click()
        return self

    @Test()
    def enter_encounter_number(self, number):
        if "" != number:
            self.element(*self.chart_number).type(number)
        return self

    @Test()
    def enter_medical_record_number(self, number):
        if "" != number:
            self.element(*self.medical_number).type(number)
        return self

    @Test()
    def select_insurance_type(self, insurance_type):
        if "" != insurance_type:
            self.element(*self.insurance_type).select_option_by_text(insurance_type)
        return self

    @Test(next_button)
    def click_on_next(self):
        self.element(*self.next_button).click_and_wait(3)
        return self

    @Test(new_patient)
    def click_on_create_new_patient(self):
        self.element(*self.new_patient).wait_until_present().click_and_wait(3)
        return self

    @Test(continue_patient)
    def click_on_continue(self):
        self.element(*self.continue_patient).wait_until_present().click_and_wait(3)
        return self

    @Test(("undefined", "undefined"))
    def select_patient(self, name):
        patient = (By.XPATH, "//span[contains(text(),'{0}')]".format(name))
        self.element(*patient).wait_until_present().click_and_wait(3)
        self.click_on_continue()
        return self

    @Test()
    def select_legal_status(self, status):
        legal = (By.XPATH, "//input[@value='{0}']".format(status))
        self.element(*legal).wait_until_present().click()
        continue_btn = (By.XPATH, "//div[@id='IntakeModal']//a[contains(.,'Continue')]")
        self.element(*continue_btn).wait_until_present().click_and_wait()
        return self

    @Test()
    def select_provider(self, provider):
        ele = (By.XPATH, "//label[.='Please select the psychiatrist to see availability']/following-sibling::select")
        self.element(*ele).wait_until_present().select_option_by_index(provider)

    @Test()
    def click_on_resume_by_name(self, patient):
        start_btn = (By.XPATH, "//*[contains(.,'{0}')]"
                               "/ancestor-or-self::div[@class='well well-bordered']/p"
                               "/a[contains(.,'Resume')]".format(patient))
        self.element(*start_btn).wait_until_present().click_and_wait()

    def chat_button_is_present(self, email, provider):
        chat_btn = (By.XPATH,
                    "//button[@data-vsee-id='{0}' and @data-name='{1}']".format(email, provider))
        return self.element(*chat_btn).wait_until_present().is_present()

    @Test()
    def click_on_chat_button(self, email, provider):
        chat_btn = (By.XPATH,
                    "//button[@data-vsee-id='{0}' and @data-name='{1}']".format(email, provider))
        self.element(*chat_btn).wait_until_clickable().highlight_element().click_and_wait(8)
        return self

    @Test()
    def click_on_exit_button(self):
        self.element(*self.exit_btn).wait_until_clickable().highlight_element().click_and_wait(8)
        return self

    @Test()
    def exit_button_is_present(self):
        return self.element(*self.exit_btn).wait_until_present().is_present()

    visit_status = (By.XPATH, "//div[@id='WaitingRoom']//div[@class='panel-body text-center']/h4")

    @Test()
    def get_visit_status(self):
        return self.element(*self.visit_status).wait_until_present().get_text_value()

    @Test()
    def get_first_message(self):
        msg_status = (By.XPATH, "//div[@id='WaitingRoom']//div[@class='panel-body']/h4")
        return self.element(*msg_status).wait_until_present().get_text_value()

    @Test()
    def wait_for_chat_button_clickable(self, email, provider):
        wait(lambda: self.chat_button_is_present(email, provider), waiting_for='Wait For Chat Button Is Present',
             timeout_seconds=600)
        self.wait_a_bit(5)
        return self

    # Visit option form
    continue_visit = (By.XPATH, "//div[@id='intake-flow']//div[@class='modal-footer']/a[contains(.,'Continue')]")

    @Test()
    def select_visit_option(self, visit_option):
        option_des = (By.XPATH, "//td[.='{0}']/preceding-sibling::td/input".format(visit_option))
        self.element(*option_des).wait_until_present().click()
        return self

    @Test()
    def click_on_visit_button(self):
        self.element(*self.continue_visit).wait_until_present().highlight_element().click_and_wait(5)
        return self

    upload_field = (By.LINK_TEXT, "Click Here")

    @Test(upload_field)
    def upload_attachment(self, path_file):
        path_pic = user_dir + "\\images\\" + path_file
        self.element(*self.upload_field).click_and_wait()
        self.upload_file(path_pic)
        return self

    @Test()
    def get_thanks(self):
        thanks = (By.XPATH, "//div[@data-bind='visible: visitFinished']/div[@class='panel-body text-center']/h4")
        return self.element(*thanks).wait_until_present().get_text_value()
