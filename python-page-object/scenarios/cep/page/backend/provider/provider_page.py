__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from scenarios.resource import user_dir
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test


class RolePage(BasePage):
    save_button = (By.XPATH, '//*[@id="UserForm"]/div//button[text()="Save"]')

    def input_data_by_label(self, label, value):
        item = (By.XPATH, "//*[text()='{0}']/following-sibling::div/input".format(label))
        self.element(*item).type(value)

    def get_data_by_label(self, label):
        item = (By.XPATH, "//*[text()='{0}']/following-sibling::div/input".format(label))
        return self.element(*item).get_value()

    def enter_first_name(self, value):
        self.input_data_by_label("First Name", value)
        return self

    def enter_last_name(self, value):
        self.input_data_by_label("Last Name", value)
        return self

    def enter_email(self, value):
        self.input_data_by_label("Email", value)
        return self

    def get_first_name(self):
        return self.get_data_by_label("First Name")

    def get_last_name(self):
        return self.get_data_by_label("Last Name")

    def get_email(self):
        return self.get_data_by_label("Email")

    @Test()
    def select_role(self, role):
        item = (By.XPATH, "//*[text()='Roles']/following-sibling::div/select")
        self.element(*item).select_option_by_text(role)
        return self

    @Test(save_button)
    def click_on_save(self):
        self.element(*self.save_button).click_and_wait(5)
        return self


class ProviderPage(RolePage):
    new_button = (By.CSS_SELECTOR, ".new-provider-btn")
    searchChkBox = (By.XPATH, '//input[@type="search"]')
    first_row = (By.XPATH, "//table[@id='providers-table']/tbody/tr/td[3]")
    new_pwd = (By.ID, 'AppUserNewPassword')
    alert_msg = (By.XPATH, "//*[text()='Sign In']/following-sibling::div/div[@class='alert alert-info']")
    permission_link = (By.XPATH, '//a[@title="Manage permission"]')

    @Test(new_button)
    def create_a_one(self):
        self.click_on_element(*self.new_button)
        return self

    @Test(searchChkBox)
    def search_provider(self, email):
        self.element(*self.searchChkBox).clear().type(email).type_and_wait(Keys.TAB, 5)
        return self

    @Test(permission_link)
    def click_on_manage_permession(self):
        self.element(*self.permission_link).click_and_wait(5)
        return self

    @Test(first_row)
    def provider_found(self):
        """list_mail = self.getSourceHTML()
        # Regex Extract Email
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', list_mail)
       """
        return self.element(*self.first_row).get_text_value()

    @Test(new_pwd)
    def reset_password(self, pwd):
        confirm_pwd = (By.ID, 'AppUserConfirmPassword')
        sumbit_btn = (By.XPATH, "//button[@type='submit']")

        self.element(*self.new_pwd).type(pwd)
        self.element(*confirm_pwd).type(pwd)
        self.element(*sumbit_btn).click_and_wait(5)

    @Test(alert_msg)
    def get_alert_password_changed(self):
        return self.element(*self.alert_msg).get_text_value()


class SubTypePage(BasePage):
    provider_type = (By.ID, 'UserSubtype')

    @Test(provider_type)
    def select_subtype(self, label):
        next_btn = (By.XPATH, ".//*[@id='step1']//button")
        self.element(*self.provider_type).select_option_by_text(label)
        self.click_on_element(*next_btn)
        return self


class DemographicsPage(BasePage):
    first_name = (By.ID, 'UserFirstName')
    last_name = (By.ID, 'UserLastName')
    email_field = (By.ID, 'UserEmail')
    title_field = (By.ID, 'ProviderTitle')
    suffix_field = (By.ID, 'ProviderSuffix')
    phone_field = (By.ID, 'UserPhone')
    address_field = (By.ID, 'UserStreetAddr')
    city_field = (By.ID, 'UserCity')
    state_drop = (By.XPATH, "//label[@for='UserState']/following-sibling::div/div")
    search_state = (By.XPATH, "//ul[@role='listbox']/preceding-sibling::div/input")
    zip_field = (By.ID, 'UserZip')
    step2 = (By.XPATH, "//*[@id='step2']//button")

    user_name = (By.ID, "UserUsername")
    pwd_txt = (By.ID, "UserPassword")
    confirm_pwd = (By.ID, "UserTemppassword")

    @Test(first_name)
    def fill_first_name(self, firtName):
        self.enter_text_into(firtName, *self.first_name)
        return self

    def fill_last_name(self, lastName):
        self.enter_text_into(lastName, *self.last_name)
        return self

    def fill_email(self, email):
        self.enter_text_into(email, *self.email_field)
        return self

    def fill_username(self, username):
        if "" != username:
            self.enter_text_into(username, *self.user_name)
        return self

    def fill_password(self, password):
        if "" != password:
            self.enter_text_into(password, *self.pwd_txt)
        return self

    def fill_confirm_password(self, confirm_password):
        if "" != confirm_password:
            self.enter_text_into(confirm_password, *self.confirm_pwd)
        return self

    def fill_title(self, title):
        self.enter_text_into(title, *self.title_field)
        return self

    def fill_suffix(self, suffix):
        self.enter_text_into(suffix, *self.suffix_field)
        return self

    def fill_phone(self, phone):
        self.enter_text_into(phone, *self.phone_field)
        return self

    def fill_address(self, addr):
        self.enter_text_into(addr, *self.address_field)
        return self

    def fill_city(self, city):
        self.enter_text_into(city, *self.city_field)
        return self

    def fill_state(self, state):
        self.click_on_element(*self.state_drop)
        self.type_and_enter(state, *self.search_state)
        return self

    def fill_zipcode(self, zipcode):
        self.enter_text_into(zipcode, *self.zip_field)
        return self

    @Test(step2)
    def process_demographics(self):
        self.element(*self.step2).click_and_wait(5)
        return self


class LicensePage(BasePage):
    dea_field = (By.ID, 'UserDataDEA')
    npi_field = (By.ID, 'UserDataNPI')
    specialties_field = (By.XPATH, "//label[text()='Specialties']/following-sibling::input")
    statesLicensed_field = (By.XPATH, "//label[text()='States Licensed']/following-sibling::input")
    states_serviced_field = (By.XPATH, "//label[text()='States Serviced']/following-sibling::input")
    step3 = (By.XPATH, "//*[@id='step3']//button")

    @Test(dea_field)
    def fill_dea(self, dea):
        if "" != dea:
            self.enter_text_into(dea, *self.dea_field)
        return self

    @Test(npi_field)
    def fill_npi(self, npi):
        if "" != npi:
            self.enter_text_into(npi, *self.npi_field)
        return self

    def type_into(self, value, *locator):
        """Delete the item if existed and fill it again
        value_xpath = "//div[text()='{0}']/following-sibling::a".format(value)
        count = len(self.find_elements(*(By.XPATH, value_xpath)))
        if count == 0:
        """
        self.type_and_enter(value, *locator)

    def fill_specialties(self, item_name):
        if "Default" != item_name:
            self.type_into(item_name, *self.specialties_field)
        return self

    def fill_states_licensed(self, item_name):
        self.type_into(item_name, *self.statesLicensed_field)
        return self

    @Test(states_serviced_field)
    def fill_states_serviced(self, item_name):
        self.type_into(item_name, *self.states_serviced_field)
        return self

    @Test(step3)
    def process_license(self):
        self.element(*self.step3).click_and_wait(5)
        return self


class ProfilePage(BasePage):
    medical_school_field = (By.ID, 'UserDataMedicalSchool')
    internship_field = (By.ID, 'UserDataInternship')
    residency_field = (By.ID, 'UserDataResidency')
    focus_language = (By.XPATH, "//input[@id='UserDataLanguage_']/following-sibling::div")
    bio_field = (By.ID, 'UserDataShortBio')
    picture_field = (By.LINK_TEXT, "Click Here")
    step4 = (By.XPATH, "//*[@id='step4']//button")

    @Test(medical_school_field)
    def fill_medical_school(self, medical_school):
        self.enter_text_into(medical_school, *self.medical_school_field)
        return self

    def fill_internship(self, internship):
        self.enter_text_into(internship, *self.internship_field)
        return self

    def fill_residency(self, residency):
        self.enter_text_into(residency, *self.residency_field)
        return self

    def fill_language(self, language):
        language_field = (By.XPATH, "//*[text()='Language']/following-sibling::input")
        # self.selectByVisibleText(language).From(*self.language_field)
        self.element(*self.focus_language).click_and_wait(3)
        self.type_and_enter(language, *language_field)
        return self

    def fill_bio(self, bio):
        self.enter_text_into(bio, *self.bio_field)
        return self

    @Test(picture_field)
    def upload_image_profile(self, avatar):
        path_pic = user_dir + "\\images\\" + avatar
        self.click_on_element(*self.picture_field).wait_a_bit(3)
        self.upload_file(path_pic)
        return self

    @Test(step4)
    def process_profile(self):
        self.element(*self.step4).click_and_wait(5)
        return self


class AssignmentPage(BasePage):
    clinic_radio = (By.XPATH, "//input[@value='clinic']")
    room_radio = (By.XPATH, "//input[@value='room']")
    rooms_field = (By.XPATH, "//*[@id='ExtraAssignmentClinics']/following-sibling::div/ul/li/input")
    step5 = (By.XPATH, "//*[@id='step5']//button")

    @Test(clinic_radio)
    def select_clinic(self):
        self.click_on_element(*self.clinic_radio)
        return self

    def select_room(self):
        self.click_on_element(*self.room_radio)
        return self

    def select_assignment(self, clinic):
        if clinic is True:
            self.select_clinic()
        return self

    @Test(rooms_field)
    def assign_to(self, name):
        self.element(*self.rooms_field).click()
        self.element(*self.rooms_field).type_and_wait(name, 5) \
            .type(Keys.ENTER) \
            .type_and_wait(Keys.TAB, 3)
        return self

    @Test(step5)
    def save(self):
        self.element(*self.step5).click_and_wait(5)
        return self
