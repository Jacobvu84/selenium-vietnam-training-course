'''
Created on Jun 4, 2018

@author: Thang Nguyen
Including locators for Users page on admin
Including actions 
'''

import os, sys
from waiting import wait
from time import sleep

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from selenium.webdriver.common.keys import Keys
from webium.clinic_page import ClinicPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from webium.base_page import Test


class UsersPage(ClinicPage):
    def __init__(self, ClinicPage):
        self.set_attribute(ClinicPage)
    
    users_link = (By.PARTIAL_LINK_TEXT, "Users")
    
    @Test(users_link)
    def click_users_link(self):
        self.element(*self.users_link) \
        .wait_until_clickable().click()
        
    # Locator on all users tab
    all_users_tab = (By.PARTIAL_LINK_TEXT, "All users")
    all_users_search = (By.XPATH, "//div[@id='users']//input[@type='search']")
    all_users_datatable = (By.XPATH, ".//*[@id='users-table']//tr")
    
    @Test(users_link)
    def check_visibile_of_users_link(self):
        self.element(*self.users_link) \
        .wait_until_visible()
    
    @Test(all_users_tab)
    def wait_visibile_of_all_users_tab(self):
        self.element(*self.all_users_tab) \
        .wait_until_visible()
    
    @Test(all_users_search)
    def wait_visibile_of_all_users_search_field(self):
        self.element(*self.all_users_search) \
        .wait_until_visible()
    
    @Test(all_users_datatable)
    def wait_for_all_users_datatable(self):
        wait(lambda: self.check_datatable_is_loaded(self.all_users_datatable), waiting_for='Wait for all users data table is loaded',
             timeout_seconds=20)
        
    # Locator on admin tab
    admin_tab = (By.PARTIAL_LINK_TEXT, "Admin")
    
    # Locator on Providers tab
    providers_tab = (By.PARTIAL_LINK_TEXT, "Providers")
    providers_search = (By.XPATH, ".//*[@id='providers-table_filter']//input[@type='search']")
    providers_new_user_btn = (By.XPATH, ".//*[@id='providers']//a[contains(string(), 'New user')]")
    providers_datatable = (By.XPATH, ".//*[@id='providers-table']//tr")
    impersonate_provider_btn = (By.XPATH, "//a[@data-action='Providers.impersonate']")
    impersonate_btn = (By.XPATH, "//button[text()='Impersonate']")
    
    @Test(providers_tab)
    def click_providers_tab(self):
        self.element(*self.providers_tab) \
        .wait_until_clickable().click()
    
    @Test(providers_datatable)
    def wait_for_provider_datatable(self):
        wait(lambda: self.check_datatable_is_loaded(self.providers_datatable), waiting_for='Wait for provider data table is loaded',
             timeout_seconds=20)
    
    @Test(providers_datatable)
    def wait_for_number_of_providers_on_datatable(self, number_of_result):
        wait(lambda: self.check_number_of_results_on_datatable(self.providers_datatable, number_of_result), 
             waiting_for='Wait for providers data table returns {0} result(s)'.format(str(number_of_result)),
             timeout_seconds=20) 
    
    @Test(providers_search)
    def wait_visibile_of_providers_search_field(self):
        self.element(*self.providers_search) \
        .wait_until_visible()
    
    @Test(providers_search)
    def enter_provider_email_into_search(self, email):
        self.element(*self.providers_search) \
        .wait_until_visible() \
        .type(email)
    
    @Test(providers_new_user_btn)
    def click_new_providers_button(self):
        self.element(*self.providers_new_user_btn) \
        .wait_until_clickable().click()
    
    # if there're more than 1 result, click on first one
    @Test(impersonate_provider_btn)
    def click_into_impersonate_provider_icon(self):
        self.element(*self.impersonate_provider_btn) \
        .wait_until_clickable().click()
    
    @Test(impersonate_btn)
    def check_visible_of_impersonate_button(self):
        try:
            self.element(*self.impersonate_btn) \
            .wait_until_visible()
            return True
        except:
            return False
    
    @Test(impersonate_btn)
    def click_into_impersonate_provider(self):
        self.element(*self.impersonate_btn) \
        .wait_until_clickable().click()
    
    @Test()
    def select_clinic_of_provider_by_name(self, clinic_name):
        xpath = "//a[@class = 'list-group-item' and contains(string(), '{0}')]".format(clinic_name)
        self.element(By.XPATH, xpath) \
        .wait_until_clickable().click()
    
    # Create a new provider wizard's locator
    create_a_provider_title = (By.XPATH, "//h4[text()='New provider']")
    
    @Test(create_a_provider_title)
    def wait_visibile_of_new_provider_title(self):
        self.element(*self.create_a_provider_title) \
        .wait_until_visible()
        
    # Sub type step
    create_a_provider_subtype = (By.ID, "UserSubtype")
    create_a_provider_subtype_next_btn = (By.XPATH, ".//*[@id='step1']//button")
    
    @Test(create_a_provider_subtype)
    def select_subtype(self, subtype):
        self.element(*self.create_a_provider_subtype) \
        .wait_until_clickable() \
        .select_option_by_text(subtype)
    
    @Test(create_a_provider_subtype_next_btn)
    def click_next_button_on_subtype_step(self):
        self.element(*self.create_a_provider_subtype_next_btn) \
        .wait_until_clickable() \
        .click()
        
    # Demographics step
    create_a_provider_fn = (By.ID, "UserFirstName")
    create_a_provider_ln = (By.ID, "UserLastName")
    create_a_provider_email = (By.ID, "UserEmail")
    create_a_provider_phone = (By.ID, "UserPhone")
    create_a_provider_address = (By.ID, "UserStreetAddr")
    create_a_provider_city = (By.ID, "UserCity")
    create_a_provider_zipcode = (By.ID, "UserZip")
    create_a_provider_state = (By.ID, "s2id_UserState")
    create_a_provider_demo_next_btn = (By.XPATH, ".//*[@id='step2']//button")
    
    @Test(create_a_provider_fn)
    def enter_provider_first_name(self, firstname):
        self.element(*self.create_a_provider_fn) \
        .wait_until_clickable() \
        .type(firstname)
    
    @Test(create_a_provider_ln)
    def enter_provider_last_name(self, lastname):
        self.element(*self.create_a_provider_ln) \
        .type(lastname)
        
    @Test(create_a_provider_email)
    def enter_provider_email(self, email):
        self.element(*self.create_a_provider_email) \
        .type(email)
        
    @Test(create_a_provider_address)
    def enter_provider_street_address(self, address):
        self.element(*self.create_a_provider_address) \
        .type(address)
    
    @Test(create_a_provider_city)
    def enter_provider_city(self, city):
        self.element(*self.create_a_provider_city) \
        .type(city)
    
    @Test(create_a_provider_state)
    def select_provider_state(self, state):
        self.element(*self.create_a_provider_state).click()
        sleep(0.5)
        self.send_keys_active_elem(state + Keys.ENTER)
        sleep(0.5)
    
    @Test(create_a_provider_zipcode)
    def enter_provider_zipcode(self, zipcode):
        self.element(*self.create_a_provider_zipcode) \
        .type(zipcode)
    
    @Test(create_a_provider_demo_next_btn)
    def click_next_button_on_demographics_step(self):
        self.element(*self.create_a_provider_demo_next_btn) \
        .wait_until_clickable() \
        .click()
    
    # License step
    create_a_provider_dea = (By.ID, "UserDataDEA")
    create_a_provider_npi = (By.ID, "UserDataNPI")
    create_a_provider_license_next_btn = (By.XPATH, ".//*[@id='step3']//button")
    
    @Test(create_a_provider_dea)
    def enter_provider_dea(self, dea):
        self.element(*self.create_a_provider_dea) \
        .wait_until_clickable() \
        .type(dea)
    
    @Test(create_a_provider_npi)
    def enter_provider_npi(self, npi):
        self.element(*self.create_a_provider_npi) \
        .type(npi)
    
    @Test(create_a_provider_license_next_btn)
    def click_next_button_on_license_step(self):
        self.element(*self.create_a_provider_license_next_btn) \
        .wait_until_clickable() \
        .click()
    
    # Profile steps
    create_a_provider_profile_next_btn = (By.XPATH, ".//*[@id='step4']//button")
    
    @Test(create_a_provider_profile_next_btn)
    def click_next_button_on_profile_step(self):
        self.element(*self.create_a_provider_profile_next_btn) \
        .wait_until_clickable() \
        .click()
    
    create_a_provider_assign_field = (By.XPATH, ".//*[@id='s2id_autogen6']")
    create_a_provider_save_btn = (By.XPATH, ".//*[@id='step5']//button")
    create_a_provider_assign_by_clinics = (By.XPATH, "//*[contains(text(),'By clinics')]")
    create_a_provider_assign_by_rooms = (By.XPATH, "//*[contains(text(),'By rooms')]")
    
    @Test(create_a_provider_assign_by_clinics)
    def choose_assign_by_clinics(self):
        self.element(*self.create_a_provider_assign_by_clinics) \
        .wait_until_clickable() \
        .click()
        
    @Test(create_a_provider_assign_by_rooms)
    def choose_assign_by_rooms(self):
        self.element(*self.create_a_provider_assign_by_rooms) \
        .wait_until_clickable() \
        .click()
    
    @Test(create_a_provider_assign_field)
    def assign_provider_to_clinics(self, clinic):
        self.element(*self.create_a_provider_assign_field).click()
        sleep(0.5)
        self.send_keys_active_elem(clinic)
        sleep(3)
        self.send_keys_active_elem(Keys.TAB)
    
    @Test(create_a_provider_assign_field)
    def assign_provider_to_rooms(self, provider_email):
        self.element(*self.create_a_provider_assign_field).click()
        sleep(0.5)
        self.send_keys_active_elem(provider_email)
        sleep(3)
        self.send_keys_active_elem(Keys.TAB)
    
    @Test(create_a_provider_save_btn)
    def click_save_button(self):
        self.element(*self.create_a_provider_save_btn) \
        .wait_until_clickable() \
        .click()
        
    # Locator on Patients tab
    patients_tab = (By.PARTIAL_LINK_TEXT, "Patients")
    patients_search = (By.XPATH, "//*[@id='members']//*[@type='search']")
    patients_new_user_btn = (By.CSS_SELECTOR, ".new-member-btn.pull-right.btn.btn-primary.btn-sm")
    patients_delete_patient_btn = (By.XPATH, "//*[@data-action='Members.delete']")
    patients_datatable = (By.XPATH, ".//*[@id='members-table']//tr")
    patients_create_success = (By.XPATH, "//div[contains(text(), 'Member created.')]")
    impersonate_patient_btn = (By.XPATH, "//a[@data-action='Members.impersonate']")
    
    @Test(patients_search)
    def wait_visibile_of_patients_created_successfully_text(self):
        self.element(*self.patients_create_success) \
        .wait_until_visible()
    
    @Test(patients_tab)
    def click_patients_tab(self):
        self.element(*self.patients_tab) \
        .wait_until_clickable().click()
    
    @Test(patients_search)
    def wait_visibile_of_patients_search_field(self):
        self.element(*self.patients_search) \
        .wait_until_visible()
    
    @Test(patients_search)
    def enter_patient_email_into_search(self, email):
        self.element(*self.patients_search) \
        .wait_until_visible() \
        .type(email)
    
    @Test(patients_datatable)
    def wait_for_patients_datatable(self):
        wait(lambda: self.check_datatable_is_loaded(self.patients_datatable), waiting_for='Wait for Patients data table is loaded',
             timeout_seconds=20)
    
    @Test(patients_datatable)
    def wait_for_number_of_patients_on_datatable(self, number_of_result):
        wait(lambda: self.check_number_of_results_on_datatable(self.patients_datatable, number_of_result), 
             waiting_for='Wait for patients data table returns {0} result(s)'.format(str(number_of_result)),
             timeout_seconds=20) 
        
    @Test(patients_new_user_btn)
    def click_into_new_user_button_on_patients_tab(self):
        self.element(*self.patients_new_user_btn) \
        .wait_until_clickable().click()
    
    @Test(impersonate_patient_btn)
    def click_into_impersonate_patient(self):
        self.element(*self.impersonate_patient_btn) \
        .wait_until_clickable().click()
    
    # Create a member modal's locator
    create_a_member_form = (By.ID, "MemberForm")
    create_a_member_account_code_select_arrow = (By.XPATH, "//div[@id='s2id_MemberAccountCode']//span[@class='select2-arrow']")
    create_a_member_account_search_result = (By.CLASS_NAME, "select2-result-label")
    create_a_member_selected_account = (By.XPATH, "//div[@id='s2id_MemberAccountCode']//span[@class='select2-chosen']")
    create_a_member_username = (By.ID, "AppUserUsername")
    create_a_member_pwd = (By.ID, "AppUserPassword")
    create_a_member_repwd = (By.ID, "AppUserTemppassword")
    create_a_member_fn = (By.ID, "AppUserFirstName")
    create_a_member_ln = (By.ID, "AppUserLastName")
    create_a_member_email = (By.ID, "AppUserEmail")
    create_a_member_gender = (By.ID, "s2id_AppUserGender")
    create_a_member_dob_month = (By.ID, "s2id_AppUserDobMonth")
    create_a_member_dob_day = (By.ID, "s2id_AppUserDobDay")
    create_a_member_dob_year = (By.ID, "s2id_AppUserDobYear")
    create_a_member_address = (By.ID, "AppUserStreetAddr")
    create_a_member_city = (By.ID, "AppUserCity")
    create_a_member_state = (By.ID, "s2id_AppUserState")
    create_a_member_zipcode = (By.ID, "AppUserZip")
    create_a_member_phone = (By.ID, "AppUserPhone")
    create_a_member_submit_button = (By.CSS_SELECTOR, "button[class='submit btn btn-primary']")
    newPatientAlert = (By.CSS_SELECTOR, ".alert.alert-danger.fade.in")
    
    @Test(create_a_member_form)
    def wait_for_create_a_member_form_is_visible(self):
        self.element(*self.create_a_member_form) \
        .wait_until_visible()
        sleep(2)
    
    @Test(create_a_member_account_code_select_arrow)
    def click_into_select_account_arrow(self):
        self.element(*self.create_a_member_account_code_select_arrow).click()
    
    @Test()
    def type_into_account_search(self, account_name):
        self.send_keys_active_elem(account_name)
        
    @Test(create_a_member_account_search_result)
    def select_account_by_name(self, account_name):
        sleep(3)
        elems = self.find_elements(*self.create_a_member_account_search_result)
        flag = False
        for elem in elems:
            if account_name in elem.text:
                flag = True
                elem.click()
                break
        if not flag:
            raise
    
    @Test(create_a_member_selected_account)
    def verify_selected_account_name(self, account_name):
        self.element(*self.create_a_member_selected_account)
        
    @Test(create_a_member_username)
    def enter_patient_username(self, username):
        self.element(*self.create_a_member_username).type(username)
    
    @Test(create_a_member_pwd)
    def enter_patient_password(self, password):
        self.element(*self.create_a_member_pwd).type(password)
    
    @Test(create_a_member_repwd)
    def retype_patient_password(self, password):
        self.element(*self.create_a_member_repwd).type(password)
    
    @Test(create_a_member_fn)
    def enter_patient_first_name(self, first_name):
        self.element(*self.create_a_member_fn).type(first_name)
    
    @Test(create_a_member_ln)
    def enter_patient_last_name(self, last_name):
        self.element(*self.create_a_member_ln).type(last_name)
    
    @Test(create_a_member_email)
    def enter_patient_email(self, email):
        self.element(*self.create_a_member_email).type(email)
    
    @Test(create_a_member_gender)
    def select_patient_gender(self, gender):
        self.element(*self.create_a_member_gender).click()
        sleep(0.5)
        self.send_keys_active_elem(gender + Keys.ENTER)
        sleep(0.5)
    
    @Test(create_a_member_dob_month)
    def select_patient_dob_month(self, month):
        self.element(*self.create_a_member_dob_month).click()
        sleep(0.5)
        self.send_keys_active_elem(month + Keys.ENTER)
        sleep(0.5)
    
    @Test(create_a_member_dob_day)
    def select_patient_dob_day(self, day):
        self.element(*self.create_a_member_dob_day).click()
        sleep(0.5)
        self.send_keys_active_elem(day + Keys.ENTER)
        sleep(0.5)
    
    @Test(create_a_member_dob_year)
    def select_patient_dob_year(self, year):
        self.element(*self.create_a_member_dob_year).click()
        sleep(0.5)
        self.send_keys_active_elem(year + Keys.ENTER)
        sleep(0.5)
    
    @Test(create_a_member_address)
    def enter_patient_address(self, address):
        self.element(*self.create_a_member_address).type(address)
    
    @Test(create_a_member_city)
    def enter_patient_city(self, city):
        self.element(*self.create_a_member_city).type(city)
        
    @Test(create_a_member_state)
    def select_patient_state(self, state):
        self.element(*self.create_a_member_state).click()
        sleep(0.5)
        self.send_keys_active_elem(state + Keys.ENTER)
        sleep(0.5)
    
    @Test(create_a_member_zipcode)
    def enter_patient_zipcode(self, zipcode):
        self.element(*self.create_a_member_zipcode).type(zipcode)
        
    @Test(create_a_member_phone)
    def enter_patient_phone(self, phone):
        self.element(*self.create_a_member_phone).type(phone)
    
    @Test(create_a_member_submit_button)
    def click_submit_new_patient(self):
        self.element(*self.create_a_member_submit_button)\
        .wait_until_clickable().click()