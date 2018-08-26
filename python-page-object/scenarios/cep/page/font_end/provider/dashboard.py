__author__ = 'jacob@vsee.com'

import os, sys
from waiting import wait

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from util.logger import Test


class DashBoardPage(BasePage):

    def is_patient_present(self, f_name):
        """Wait the patient in waiting room"""
        patient_xpath = "//h4[contains(text(),'Ready for Visit')]" \
                        "/ancestor-or-self::div[@class='visit-group-header panel-heading']" \
                        "/following-sibling::div[@class='visit-group-content']//div[contains(text(),'{0}')]" \
                        "/ancestor-or-self::div[@class='row walk-in']" \
                        "//*[contains(@class,'text-center')]/a/i".format(f_name)

        patient_view = (By.XPATH, patient_xpath)

        return self.element(*patient_view).is_present()

    def is_patient_in_getting_ready(self, number='1'):
        title_expanse = (By.XPATH, "//h4[text()='Getting ready ({0})']".format(number))
        return self.element(*title_expanse).is_present()

    def is_patient_in_progress(self, number='1'):
        title_expanse = (By.XPATH, "//h4[text()='In Progress ({0})']".format(number))
        return self.element(*title_expanse).is_present()

        # 15s wait for each iterator
    @Test(("Undefined", "Undefined"))
    def wait_for_patient_available(self, f_name):
        wait(lambda: self.is_patient_present(f_name), waiting_for='Wait For Patient is in waiting room',
             timeout_seconds=600)
        self.refresh_page().wait_a_bit(5)
        return self

    @Test(("Undefined", "Undefined"))
    def wait_for_patient_in_getting_ready(self , number='1'):
        wait(lambda: self.is_patient_in_getting_ready(number), waiting_for='Wait For Patient is in getting ready',
             timeout_seconds=600)
        self.refresh_page().wait_a_bit(5)
        title_expanse = (By.XPATH, "//h4[text()='Getting ready ({0})']".format(number))
        self.element(*title_expanse).click()
        return self

    def wait_for_patient_has_in_progress(self, number='1'):
        wait(lambda: self.is_patient_in_progress(number), waiting_for='Wait For Patient is in Progress',
             timeout_seconds=600)
        self.refresh_page().wait_a_bit(1)
        title_expanse = (By.XPATH, "//h4[text()='In Progress ({0})']".format(number))
        self.element(*title_expanse).click()
        return self

    def should_see_vsee_status_is_offline(self, f_name):
        patient_xpath = "//h4[contains(text(),'Getting ready')]" \
                        "/ancestor-or-self::div[@class='visit-group-header panel-heading']" \
                        "/following-sibling::div[@class='visit-group-content']//div[contains(text(),'{0}')]" \
                        "/ancestor-or-self::div[@class='row walk-in']" \
                        "//*[contains(@class,'text-center')]/a/i".format(f_name)

        patient_view = (By.XPATH, patient_xpath)

    @Test(("Undefined", "Undefined"))
    def view_patient_by_name(self, f_name):
        try:
            if "" != f_name:
                view_xpath = (By.XPATH, "//*[contains(text(),'{0}')]"
                                        "/ancestor-or-self::div[@class='row walk-in']"
                                        "//*[contains(@class,'text-center')]/a/i".format(f_name))
            else:
                view_xpath = (By.XPATH, "//*[contains(text(),'{0}')]"
                                        "/ancestor-or-self::div[@class='row walk-in']"
                                        "//*[contains(@class,'text-center')]/a/i".format(f_name))
            self.element(*view_xpath).wait_until_clickable() \
                .highlight_element().click_and_wait(5)
        except StaleElementReferenceException:
            self.view_patient_by_name(f_name)
        return self

    def click_on_resume(self, f_name):
        try:
            if "" != f_name:
                view_xpath = (By.XPATH, "//*[contains(text(),'{0}')]"
                                        "/ancestor-or-self::div[@class='row walk-in']"
                                        "//*[contains(@class,'text-center')]/a[text()='Resume']/i".format(f_name))
            else:
                view_xpath = (By.XPATH, "//*[contains(text(),'{0}')]"
                                        "/ancestor-or-self::div[@class='row walk-in']"
                                        "//*[contains(@class,'text-center')]/a[text()='Resume']/i".format(f_name))
            self.element(*view_xpath).wait_until_clickable() \
                .highlight_element().click_and_wait(5)
        except StaleElementReferenceException:
            self.view_patient_by_name(f_name)
        return self

    schedule = (By.XPATH, "//h3[text()=\"Today's Schedule\"]/following-sibling::div//div[@class=\"address\"]")

    @Test(schedule)
    def get_schedule(self):
        return self.element(*self.schedule).get_text_value()

    visit_empty = (By.XPATH, "//div[@class='visit visit-empty']")

    @Test(visit_empty)
    def get_visit_empty(self):
        return self.element(*self.visit_empty).get_text_value()

    @Test(("Undefined", "Undefined"))
    def is_view_button_visible(self):
        view_ready = "//h4[contains(text(),'Ready for Visit')]" \
                        "/ancestor-or-self::div[@class='visit-group-header panel-heading']" \
                        "/following-sibling::div[@class='visit-group-content']//a[@data-action='Visits.view']"
        patient_view = (By.XPATH, view_ready)
        return self.element(*patient_view).is_visible()

    @Test()
    def is_section_present(self, section):
        section_view = (By.XPATH, "//div[@id='ProviderDashboard']//h3[contains(.,'{0}')]".format(section))
        return self.element(*section_view).is_present()

    @Test()
    def is_create_new_visit_button_visible(self):
        button = (By.XPATH, "//a[@id='newVisitButton' and contains(.,'Create New Visit')]")
        return self.element(*button).is_visible()

    @Test()
    def is_today_schedule_section_present(self):
        # section = (By.XPATH, "//*[.='No appointments at this time.')]")
        section = (By.XPATH, '//h3[.="Today\'s Schedule"]')
        return self.element(*section).is_present()

    @Test()
    def is_start_appointment_button_visible(self, patient):
        start_btn = (By.XPATH, "//*[contains(.,'{0}')]"
                               "/ancestor-or-self::div[@class='well well-bordered']/p"
                               "/a[contains(.,'Start Appointment')]".format(patient))
        if self.element(*start_btn).is_visible() == True:
            return True
        else:
            return False

    @Test()
    def is_cancel_button_visible(self, patient):
        cancel_btn = (By.XPATH, "//*[contains(.,'{0}')]"
                               "/ancestor-or-self::div[@class='well well-bordered']/p"
                               "/a[contains(.,'Cancel')]".format(patient))
        if self.element(*cancel_btn).is_visible() == True:
            return True
        else:
            return False

    @Test()
    def get_full_name(self):
        full_name = (By.XPATH, "//div[@data-bind='text: Member.first_name + \" \" + Member.last_name ']")
        return self.element(*full_name).get_text_value()

    @Test()
    def get_gender(self):
        element = (By.XPATH, "//span[contains(@data-bind,'Member.gender')]")
        return self.element(*element).get_text_value()

    @Test()
    def get_dob(self):
        element = (By.XPATH, "//span[contains(@data-bind,'Member.dob')][2]")
        return self.element(*element).get_text_value()

    @Test()
    def get_room_infor(self):
        element = (By.XPATH, "//div[contains(@data-bind,'text: Visit.room_id')]")
        return self.element(*element).get_text_value()

    @Test()
    def get_reason_visit(self):
        element = (By.XPATH, "//p[contains(@data-bind,'Intake.reason_for_visit')]")
        return self.element(*element).get_text_value()

    @Test()
    def get_attachment_file(self):
        element = (By.XPATH, "//div[contains(@data-bind,'Intake.attachments')]")
        return self.element(*element).get_text_value()

    @Test()
    def click_on_cancel_button(self, patient):
        cancel_btn = (By.XPATH, "//*[contains(.,'{0}')]"
                               "/ancestor-or-self::div[@class='well well-bordered']/p"
                               "/a[contains(.,'Cancel')]".format(patient))
        self.element(*cancel_btn).wait_until_visible().click()
        return self


    reason_select = (By.NAME, 'reason')

    @Test(reason_select)
    def select_the_reason(self, reason):
        self.element(*self.reason_select).wait_until_present().select_option_by_text(reason)
        return self

    description_area = (By.NAME, 'description')

    @Test(description_area)
    def enter_description(self, des):
        self.element(*self.description_area).type(des)
        return self

    cancel_apt = (By.XPATH, "//button[text()='Yes, Cancel Appointment']")

    @Test(cancel_apt)
    def click_on_yes_to_cancel(self):
        self.element(*self.cancel_apt).click_and_wait()
        return self

    @Test()
    def click_on_start_appointment_by_name(self, patient):
        start_btn = (By.XPATH, "//*[contains(.,'{0}')]"
                               "/ancestor-or-self::div[@class='well well-bordered']/p"
                               "/a[contains(.,'Start Appointment')]".format(patient))
        self.element(*start_btn).wait_until_present().scroll_element_into_view() \
            .highlight_element().click_and_wait()
        return self

    @Test(("Undefined", "Undefined"))
    def click_on_resume_appointment_by_name(self, patient):
        start_btn = (By.XPATH, "//*[contains(.,'{0}')]"
                               "/ancestor-or-self::div[@class='well well-bordered']/p"
                               "/a[contains(.,'Resume')]".format(patient))
        self.element(*start_btn).wait_until_present().scroll_element_into_view() \
            .highlight_element().click_and_wait()
        return self

    @Test(("Undefined", "Undefined"))
    def is_patient_online(self, patient):
        vsee_status = (By.XPATH,
                       "//div[contains(text(),'{0}')]"
                       "/ancestor-or-self::div"
                       "/preceding-sibling::div"
                       "/span[@class='vsee_status vsee_presence_available' or @class='vsee_status vsee_presence_idle']"
                       .format(patient))
        return self.element(*vsee_status).is_visible()

    @Test(("Undefined", "Undefined"))
    def is_patient_offline(self, patient):
        vsee_status = (By.XPATH,
                       "//div[contains(text(),'{0}')]"
                       "/ancestor-or-self::div"
                       "/preceding-sibling::div"
                       "/span[@class='vsee_status vsee_presence_offline']"
                       .format(patient))
        return self.element(*vsee_status).is_visible()

    @Test(("Undefined", "Undefined"))
    def is_patient_incall(self, patient):
        vsee_status = (By.XPATH,
                       "//div[contains(text(),'{0}')]"
                       "/ancestor-or-self::div"
                       "/preceding-sibling::div"
                       "/span[@class='vsee_status vsee_presence_inacall']"
                       .format(patient))
        return self.element(*vsee_status).is_visible()

    def is_provider_online(self, provider):
        vsee_status = (By.XPATH,
                       "//strong[contains(.,'{0}')]"
                       "/following-sibling::span[@class='vsee_status vsee_presence_available']"
                       .format(provider))
        return self.element(*vsee_status).is_visible()

    login_link = (By.LINK_TEXT, 'Login')

    @Test(login_link)
    def is_login_button_visible(self):
        return self.element(*self.login_link).is_present()

    see_doctor = (By.XPATH, "//span[text()='See a Doctor Now']")

    @Test(see_doctor)
    def is_see_doctor_now_visible(self):
        return self.element(*self.see_doctor).is_present()

    @Test(see_doctor)
    def click_on_see_a_doctor_now(self):
        self.element(*self.see_doctor).click_and_wait()
        return self

    number_patients = (By.XPATH, "//p[contains(text(),'Current number of patients waiting')]/span")

    @Test(number_patients)
    def get_current_number_of_patients_waiting(self):
        return self.element(*self.number_patients).get_text_value()

    @Test(("Undefined", "Undefined"))
    def is_room_description(self, des):
        room_des = (By.XPATH, "//div[@id='room']//p[text()='{0}']".format(des))
        return self.element(*room_des).is_visible()
