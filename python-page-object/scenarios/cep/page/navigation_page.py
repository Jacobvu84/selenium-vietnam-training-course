__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test


class NavigatePage(BasePage):
    # Backend
    dashboard_menu = (By.LINK_TEXT, 'Dashboard')
    user_menu = (By.LINK_TEXT, 'Users')
    provider_tab = (By.XPATH, '//*[@id="userTabs"]//a[text()="Providers"]')
    room_menu = (By.LINK_TEXT, 'Rooms')
    clinics_menu = (By.LINK_TEXT, 'Clinics')
    schedule_menu = (By.LINK_TEXT, 'Schedule')
    visit_menu = (By.LINK_TEXT, 'Visits')
    data_menu = (By.LINK_TEXT, 'Data')
    all_tab = (By.XPATH, '//*[@id="userTabs"]//a[text()="All users"]')
    admin_tab = (By.XPATH, '//*[@id="userTabs"]//a[text()="Admin"]')
    patient_tab = (By.XPATH, '//*[@id="userTabs"]//a[text()="Patients"]')

    @Test(user_menu)
    def go_to_provider_screen(self):
        self.element(*self.user_menu).click_and_wait(5)
        return self

    @Test(provider_tab)
    def select_provider_tab(self):
        self.element(*self.provider_tab).click_and_wait(5)

    @Test(room_menu)
    def go_to_room_screen(self):
        self.element(*self.room_menu).click_and_wait(5)

    @Test(clinics_menu)
    def go_to_clinic_screen(self):
        self.element(*self.clinics_menu).click_and_wait(5)

    # Front end: Provider
    patient_menu = (By.LINK_TEXT, 'Patients')
    calendar_menu = (By.LINK_TEXT, 'Calendar')

    @Test(patient_menu)
    def go_to_patient_page(self):
        self.element(*self.patient_menu).click_and_wait(5)

    @Test(dashboard_menu)
    def go_to_dashboard(self):
        self.element(*self.dashboard_menu).click_and_wait(5)

    @Test(calendar_menu)
    def go_to_calendar_page(self):
        self.element(*self.calendar_menu).click_and_wait(5)

    # Front end: Patient
    link_home = (By.XPATH, "//a[text()='Home']")
    link_health = (By.PARTIAL_LINK_TEXT, "Health")
    link_help = (By.XPATH, "//a[contains(text(), 'Help')]")
    link_visits = (By.PARTIAL_LINK_TEXT, "Visits")

    @Test(link_health)
    def go_to_health_page(self):
        self.element(*self.link_health).click_and_wait(5)

    @Test(link_home)
    def go_to_home_page(self):
        self.element(*self.link_home).click_and_wait(5)

    @Test(link_help)
    def go_to_help_page(self):
        self.element(*self.link_help).click_and_wait(5)

    @Test(link_visits)
    def go_to_visit_page(self):
        self.element(*self.link_visits).click_and_wait(5)

    my_patients= (By.XPATH, "//li/a[text()='My Patients']")
    re_pwd = (By.NAME, "password")
    submit_btn = (By.XPATH, "//form[@id='PasswordForm']//input[@value='Submit']")

    @Test(my_patients)
    def go_to_my_patient(self):
        self.element(*self.my_patients).click_and_wait(5)
        return self

    @Test(re_pwd)
    def re_enter_password(self):
        self.element(*self.re_pwd).highlight_element().type("Vsee@)!*2018")
        return self

    @Test(submit_btn)
    def click_on_submit(self):
        self.element(*self.submit_btn).highlight_element().click_and_wait(5)
        return self
