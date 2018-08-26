__author__ = 'jacob@vsee.com'

import os
import sys
import platform
from waiting import wait

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from scenarios.resource import user_dir
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webium.base_page import BasePage
from testClass import runSikuli

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.rand import random_answer
from util import date_time
from util.logger import Test
from util.assertions import Assert


class PatientHomePage(BasePage, Assert):
    see_doctor = (By.XPATH, "//button[contains(@data-bind,'onClickWalkin')]")
    schedule_app = (By.XPATH, "//button[contains(@data-bind,'onClickAppointment')]")
    reason_for_visit = (By.XPATH, "//*[text()='Choose symptom(s) that best describe your situation']"
                                  "/following-sibling::input")
    degrees_field = (By.NAME, "vital_temperature")
    heart_field = (By.NAME, "vital_heart_rate")
    blood_field = (By.NAME, "vital_blood_pressure")
    picture_field = (By.LINK_TEXT, "Click Here")
    next_radio = (By.LINK_TEXT, "Continue")
    agreed_radio = (By.NAME, "consent")
    phone_field = (By.NAME, "phone")
    location_field = (By.NAME, 'location')
    patient_xpath = "//*[@id='ImpersonationModal']//*[contains(text(),'{0}')]"
    edit_xpath = "//*[.='{0}']/following-sibling::a[@title='Edit']"
    cancel_xpath = "//*[.='{0}']/following-sibling::a[@title='Cancel']"
    next_screen_btn = (By.XPATH, "//span[.='Please verify and update the following information']"
                                 "/ancestor::div[@class='modal-header']"
                                 "/following-sibling::div[2]/a[contains(.,'Continue')]")
    pharmacy = (By.XPATH, "//label[.='Pharmacy Name:']/following-sibling::div/input")

    @Test(see_doctor)
    def click_on_see_a_doctor_now(self):
        self.wait_a_bit(10)  # unstable
        self.element(*self.see_doctor).wait_until_clickable().click()
        return self

    @Test(schedule_app)
    def click_on_schedule_appointment(self):
        self.wait_a_bit(10)  # unstable
        self.element(*self.schedule_app).wait_until_clickable().click()
        return self

    @Test(patient_xpath)
    def select_who_visit_for(self, firstname):
        patient = (By.XPATH, self.patient_xpath.format(firstname))

        self.element(*patient)\
            .wait_until_visible() \
            .wait_until_clickable() \
            .highlight_element() \
            .click()

        return self

    @Test(reason_for_visit)
    def choose_symptom_that_best_describe_situation_(self, reasons):
        # Update the conditions
        symptoms = reasons.split(",")
        for symptom in symptoms:
            self.element(*self.reason_for_visit).wait_until_clickable() \
                .highlight_element().type(symptom).type(Keys.ENTER).type(Keys.TAB)
        return self

    @Test(degrees_field)
    def temperature(self, degrees):
        if "" != degrees:
            self.element(*self.degrees_field) \
                .highlight_element().type(degrees)
        return self

    @Test(heart_field)
    def heart_rate(self, rate):
        if "" != rate:
            self.element(*self.heart_field) \
                .highlight_element().type(rate)
        return self

    @Test(blood_field)
    def blood_pressure(self, pressure):
        if "" != pressure:
            self.element(*self.blood_field) \
                .highlight_element().type(pressure)
        return self

    @Test(picture_field)
    def upload_relevant_information(self, upload, path_file):
        if upload == 'yes':
            path_pic = user_dir + "\\images\\" + path_file
            self.click_on_element(*self.picture_field).wait_a_bit(3)
            self.upload_file(path_pic)
        return self

    @Test(next_radio)
    def next_process(self):
        self.element(*self.next_radio) \
            .highlight_element().click()
        return self

    @Test(agreed_radio)
    def agreed_to_the_terms_(self, yes):
        if yes == 'yes':
            check = self.element(*self.agreed_radio) \
                .highlight_element().is_checked()
            if check == None:
                self.element(*self.agreed_radio).click()
                self.next_process()
        return self

    @Test(phone_field)
    def phone_number_can_reach_you_today_(self, phone_number):
        self.element(*self.phone_field).wait_until_visible() \
            .highlight_element().clear().type(phone_number)
        return self

    @Test(location_field)
    def current_location(self, states):
        # why only California
        self.element(*self.location_field).select_option_by_text(states)
        return self

    @Test(edit_xpath)
    def update_item_by_label(self, label):
        # click on the edit button
        edit_btn = (By.XPATH, self.edit_xpath.format(label))
        self.element(*edit_btn).wait_until_visible().click()

    @Test(cancel_xpath)
    def cancel_item_by_label(self, label):
        # click on the edit button
        canel_btn = (By.XPATH, self.cancel_xpath.format(label))
        self.element(*canel_btn).click()

    @Test()
    def update_past_and_current_medical_conditions(self, condition):
        if "," in condition:
            # click on the edit button
            self.update_item_by_label('Past and Current Medical Conditions')

            # Update the conditions
            conditions = condition.split(",")
            for cond in conditions:
                check_box = (By.XPATH, "//td[.='{0}']/"
                                       "preceding-sibling::td/span/i".format(cond))
                status = self.element(*check_box) \
                    .wait_until_clickable().get_attribute_value("class")

                if status != 'fa fa-check-square-o':
                    self.element(*check_box).highlight_element().click()
            # click on the cancel button
            self.cancel_item_by_label('Past and Current Medical Conditions')
        return self

    @Test()
    def add_others_medical_conditions(self, conditions):
        if "," in conditions:
            # click on the edit button
            self.update_item_by_label('Past and Current Medical Conditions')

            # Update the conditions
            others_conditions = conditions.split(",")
            condition_field = (By.NAME, "condition")
            for condition in others_conditions:
                self.element(*condition_field).wait_until_visible() \
                    .highlight_element().type(condition).type(Keys.ENTER)

            # click on the cancel button
            self.cancel_item_by_label('Past and Current Medical Conditions')
        return self

    @Test()
    def update_allergies(self, drug_list):
        if "," in drug_list:
            self.update_item_by_label('Allergies')
            drugs = drug_list.split(",")
            drug_field = (By.XPATH, "//label[.='Name of Drug']/"
                                    "following-sibling::div/div/div/input")
            for drug in drugs:
                self.element(*drug_field).wait_until_visible() \
                    .highlight_element().click().type(drug).type(Keys.ENTER)
            self.cancel_item_by_label('Allergies')
        return self

    @Test()
    def update_current_medications(self, medication_list):
        if "," in medication_list:
            self.update_item_by_label('Current Medications')
            medications = medication_list.split(",")
            medication_name = (By.XPATH, "//label[.='Name of Medication']/"
                                         "following-sibling::div/input")
            for medication in medications:
                self.element(*medication_name).wait_until_visible() \
                    .highlight_element().type(medication).type(Keys.ENTER)
            self.cancel_item_by_label('Current Medications')
        return self

    @Test(next_screen_btn)
    def next_screen_(self):
        self.element(*self.next_screen_btn).click_and_wait(3)
        return self

        # Select Pharmacy

    @Test(pharmacy)
    def pharmacy_name(self, pharmacy_name):
        self.element(*self.pharmacy) \
            .wait_until_visible() \
            .highlight_element().type(pharmacy_name)
        return self

    @Test()
    def city(self, city_name='San Jose'):
        city_field = (By.NAME, "city")
        self.element(*city_field) \
            .wait_until_visible() \
            .highlight_element().type(city_name)
        return self

    @Test()
    def state(self, state='CA'):
        city_field = (By.NAME, "state")
        self.element(*city_field) \
            .highlight_element().clear().type(state)
        return self

    @Test()
    def zipcode(self, zipcode='95116'):
        zip_field = (By.NAME, "zip")
        self.element(*zip_field) \
            .highlight_element().clear().type(zipcode)
        return self

    @Test()
    def search_pharmacy(self):
        search_btn = (By.XPATH, "//button[@title='Search']")
        self.element(*search_btn).click()
        return self

    @Test()
    def select_pharmacy(self, pharmacy_name):
        if "no" != pharmacy_name:
            self.pharmacy_name(pharmacy_name) \
                .city().state().zipcode().search_pharmacy()
            the_pharmacy = (By.XPATH, "//td/strong[.='{0}']".format(pharmacy_name))
            self.element(*the_pharmacy).click_and_wait(1)
        return self

    @Test()
    def continues_(self):
        next_btn = (By.XPATH, "//*[contains(.,'If you need a prescription today, where would you like it sent?')]"
                              "/ancestor::div[@class='modal-header']"
                              "/following-sibling::div[2]/a[contains(.,'Continue')]")
        self.element(*next_btn).click()
        return self

    # To Do Survey
    @Test(("Undefined", "Undefined"))
    def answer_random(self, option):
        answer = random_answer(option)
        answer_check = (By.XPATH, '//span[contains(text(),"{0}")]'
                                  '/preceding-sibling::input'.format(answer))
        status = self.element(*answer_check).wait_until_visible().is_checked()
        if status == None:
            self.element(*answer_check).check().wait_a_bit(1)
        return self

    @Test(("Undefined", "Undefined"))
    def select_answer(self, inputs):
        if "," in inputs:
            answers = inputs.split(",")
            for answer in answers:
                answer_check = (By.XPATH, '//span[contains(text(),"{0}")]'
                                          '/preceding-sibling::input'.format(answer))
                status = self.element(*answer_check).wait_until_visible().is_checked()
                if status == None:
                    self.element(*answer_check).check()
        return self

    @Test(("Undefined", "Undefined"))
    def other_answer(self, others):
        anwser_field = (By.NAME, "want_from_telehealth_today_other")
        self.element(*anwser_field) \
            .highlight_element().clear().type(others)
        return self

    @Test(("Undefined", "Undefined"))
    def select_a_doctor(self, firstname):
        doctor = (By.XPATH, "//a/strong[contains(text(),'{0}')]".format(firstname))
        self.element(*doctor) \
            .wait_until_clickable() \
            .highlight_element().click_and_wait(5)
        return self

    @Test()
    def submit_(self):
        submit_btn = (By.XPATH, "//a[text()='Submit']")
        self.element(*submit_btn).click_and_wait(3)
        return self

    @Test()
    def click_book_an_appointment(self):
        book_app = (By.XPATH, "//*[text()='Would you like to see this provider?']"
                              "/following-sibling::button/span[text()='Book an Appointment']")
        self.element(*book_app) \
            .wait_until_clickable() \
            .highlight_element().click()
        return self

    star_5 = (By.XPATH, "//form[@id='VisitSurveyForm']/div/a[6]/i")

    @Test(star_5)
    def click_on_5_star(self):
        self.element(*self.star_5).wait_until_visible() \
            .highlight_element().click()
        return self

    endvisit_btn = (By.XPATH, "//a[.='End Visit']")

    @Test(endvisit_btn)
    def click_end_visit(self):
        self.element(*self.endvisit_btn).wait_until_visible() \
            .highlight_element().click_and_wait(10)
        return self

    @Test()
    def wait_for_call_from_provider(self, testID, src, dst):
        if "Windows-7" in platform.platform():
            runSikuli.runWin("waitCall.sikuli", [testID, src, dst, str(180), "False", "False"])
        return self

    @Test()
    def wait_for_endcall(self, testID, src):
        if "Windows-7" in platform.platform():
            runSikuli.runWin("waitEndcall.sikuli", [testID, src, str(180), "False", "False"])

    @Test(("Undefined", "Undefined"))
    def should_see_the_message(self, msg, date, time):
        msg_elemt = (By.XPATH, "//h4[text()='{0}']/following-sibling::h5[text()='{1} {2}']".format(msg, date, time))
        self.verifyEquals(self.element(*msg_elemt).is_present(), True)
        return self

    button_confirm = (By.XPATH, "//div[@id='PickerModal']//button[text()='Confirm']")

    @Test(button_confirm)
    def click_on_confirm(self):
        self.element(*self.button_confirm).click_and_wait(5)
        return self

    @Test(("Undefined", "Undefined"))
    def should_see_start_appointment_in_upcoming_appointments(self, day, time):
        appointments_elemt = "//div[@id='upcomingPanel']//span[text()='{0}, {1}']" \
                             "/ancestor-or-self::p[@class='text-muted']" \
                             "/following-sibling::p//button[contains(text(),'Start Appointment')]".format(time, day)

        appointment = (By.XPATH, appointments_elemt)
        self.verifyEquals(self.element(*appointment).wait_until_present().is_present(), True)
        return self

    start_appointment = (By.CSS_SELECTOR, ".btn.btn-success.btn-small")

    @Test(start_appointment)
    def click_on_start_appointment(self):
        self.element(*self.start_appointment).wait_until_present().click()
        return self

    @Test(("Undefined", "Undefined"))
    def select_visit_option(self, option):
        visit_option = (By.XPATH, "//td[text()='{0}']/preceding-sibling::td/input".format(option))
        self.element(*visit_option).wait_until_present().click()
        return self

    just_exit = (By.XPATH, "//a[text()='Or just exit']")

    @Test(just_exit)
    def click_on_just_exit(self):
        self.element(*self.just_exit).wait_for_element_available().click_and_wait(3)
        return self

    def is_just_exit_present(self):
        """Wait the just_exit. Sikuli take almost timeout of Selenium, so need to special wait"""
        return self.element(*self.just_exit).is_present()

    # 15s wait for each iterator
    @Test(("Undefined", "Undefined"))
    def wait_for_element_available(self):
        wait(lambda: self.is_just_exit_present(), waiting_for='Wait For just_exit is in present',
             timeout_seconds=120)
        return self

    visit_option_next = (By.XPATH, "//h4[text()='Please select a visit option']"
                                   "/ancestor-or-self::div[@class='modal-content']/div[@class='modal-footer']"
                                   "/a[contains(text(),'Continue')]")

    @Test(visit_option_next)
    def next_to_continue(self):
        self.element(*self.visit_option_next).wait_until_present().click_and_wait(2)
        return self

    cancel_link = (By.XPATH, "//div[@id='upcomingPanel']//a[text()='Cancel']")

    @Test(cancel_link)
    def click_on_cancel_button(self):
        self.element(*self.cancel_link).wait_until_clickable().click()
        return self

    @Test(("Undefined", "Cancel of Cancel Appointment"))
    def say_no(self):
        button_no = (By.XPATH, "//div[@id='modal']/div/div/div[3]/button[1]")
        self.element(*button_no).wait_until_clickable().click()
        return self

    @Test(("Undefined", "Confirm to cancel Appointment"))
    def say_yes(self):
        button_yes = (By.ID, "VisitCancel")
        self.element(*button_yes).wait_until_clickable().click()
        return self

    panelUpcoming = (By.XPATH, "//div[@id='upcomingPanel']/div[2]/div")

    def should_see_message_cancel_appointment(self):
        alertSuccess = (By.CSS_SELECTOR, ".alert.alert-success.fade.in")
        return self.element(*alertSuccess).wait_until_present().get_text_value()

    @Test(("Undefined", "Undefined"))
    def select_slot_at(self, session, time):
        """ Select available time slot with special time that you want to input
            :param session: Morning, Afternoon, Evening
            :param time: special time
        """
        today = date_time.today_in_slot()
        evening = (
            By.XPATH, "//h4[text()='{0}']/following-sibling::div//h3[contains(text(),'{1}')]".format(today, session))
        self.element(*evening).highlight_element().click()

        time_slot = (By.XPATH,
                     "//h4[text()='{0}']"
                     "/following-sibling::div//a[@data-location='modal.calendar_picker']"
                     "/span[text()='{1}']".format(today, time))
        self.element(*time_slot).highlight_element().click()
        return self

    @Test(("Undefined", "Undefined"))
    def select_first_available_time_lost(self, day):
        """ Check all session, if the session have available time slot > 1 then select it and return value
            Select the first available time slot in session
                :param session: Morning, Afternoon, Evening
                :param day: the day you want to create slot, today is default
        """
        sessions = ["Morning", "Afternoon", "Evening"]
        for session in sessions:
            available_time_slot = (
                By.XPATH,
                "//h4[text()='{0}']"
                "/following-sibling::div//h3[contains(text(),'{1}')]"
                "/ancestor-or-self::div[@class='panel-heading']"
                "/following-sibling::div[@class='panel-collapse collapse']"
                "//a[@class='list-group-item']".format(day, session))
            slots = self.element(*available_time_slot).size()
            if slots > 1:
                evening = (
                    By.XPATH,
                    "//h4[text()='{0}']/following-sibling::div//h3[contains(text(),'{1}')]".format(day, session))
                # expanse the all available time slot in the session
                self.element(*evening).highlight_element().click()

                # click on the first slot in the session
                time_slot = (By.XPATH,
                             "//h4[text()='{0}']"
                             "/following-sibling::div//h3[contains(text(),'{1}')]"
                             "/ancestor-or-self::div[@class='panel-heading']"
                             "/following-sibling::div[@class='panel-collapse collapse in']//a[2]".format(day, session))
                while not self.element(*time_slot).is_present():
                    self.element(*evening).highlight_element().click()
                self.element(*time_slot).highlight_element().click()
                return self
            elif slots == 1:
                session_xpath = (
                    By.XPATH,
                    "//h4[text()='{0}']/following-sibling::div//h3[contains(text(),'{1}')]".format(day, session))
                # expanse the all available time slot in the session
                self.element(*session_xpath).highlight_element().click()

                # click on the first slot in the session
                time_slot = (By.XPATH,
                             "//h4[text()='{0}']"
                             "/following-sibling::div//h3[contains(text(),'{1}')]"
                             "/ancestor-or-self::div[@class='panel-heading']"
                             "/following-sibling::div[@class='panel-collapse collapse in']//a[1]".format(day, session))
                while not self.element(*time_slot).is_present():
                    self.element(*session_xpath).highlight_element().click()
                self.element(*time_slot).highlight_element().click()
                return self
        return self

    @Test(("Undefined", "Undefined"))
    def get_first_available_time_lost(self, day):
        # Check all session, if the session have available time slot > 1 then select it and return value
        sessions = ["Morning", "Afternoon", "Evening"]
        for session in sessions:
            available_time_slot = (
                By.XPATH,
                "//h4[text()='{0}']"
                "/following-sibling::div//h3[contains(text(),'{1}')]"
                "/ancestor-or-self::div[@class='panel-heading']"
                "/following-sibling::div[@class='panel-collapse collapse']"
                "//a[@class='list-group-item']".format(day, session))
            slots = self.element(*available_time_slot).size()
            if slots > 1:
                time_slot = (By.XPATH,
                             "//h4[text()='{0}']/following-sibling::div//h3[contains(text(),'{1}')]"
                             "/ancestor-or-self::div[@class='panel-heading']"
                             "/following-sibling::div[@class='panel-collapse collapse']//a[2]/span".format(day, session))
                return self.get_driver().find_element(*time_slot).get_attribute("innerText")
            elif slots == 1:
                time_slot = (By.XPATH,
                             "//h4[text()='{0}']/following-sibling::div//h3[contains(text(),'{1}')]"
                             "/ancestor-or-self::div[@class='panel-heading']"
                             "/following-sibling::div[@class='panel-collapse collapse']//a[1]/span".format(day, session))
                return self.get_driver().find_element(*time_slot).get_attribute("innerText")

    re_schdule = (By.XPATH, "//button[@data-bind='click: $root.endSessionReschedule']")

    @Test(re_schdule)
    def click_on_exist_and_schedule_appointment(self):
        self.element(*self.re_schdule).highlight_element().click_and_wait(3)
        return self
