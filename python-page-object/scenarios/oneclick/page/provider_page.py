__author__ = 'jacob@vsee.com'

import os,sys,re
from time import sleep
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.by import By
from webium import BasePage
from webium import Find, Finds

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from selenium.webdriver.common.keys import Keys


class ProviderPage(BasePage):
    """A class for providers locators."""
    new_button = Find(by=By.XPATH, value='//a[@data-action="Providers.add"]')
    DEL_BUTTON = (By.XPATH, '//a[@data-action="Providers.delete"]')
    EDIT_BUTTON = (By.XPATH, '//a[@data-action="Providers.Providers.edit"]')
    SEARCH_BOX = (By.XPATH, '//input[@type="search"]')  # typeAndTab
    ACTIVE_CHECKBOX = (By.ID, 'ShowInactiveUsers')

    """Provider form"""
    FIRST_NAME_TEXT = (By.NAME, 'firstname')
    LAST_NAME_TEXT = (By.NAME, 'lastname')
    JOB_TITLE_TEXT = (By.NAME, 'title')
    VSEE_ID_TEXT = (By.NAME, 'vseeid')
    STATUS_CHECKBOX = (By.NAME, 'status')
    DEPARTMENT_BOX = (By.ID, 'select2-chosen-1')
    SEARCH_TEXT = (By.ID, 's2id_autogen1_search')  # typeAndEnter
    CREATE_BUTTON = (By.XPATH, '//button[text()="Create"]')
    FORM_HIDE = (By.XPATH, "//div[@id='AddProviderModal' and @style='display: none;']")

    first_row = Find(by=By.XPATH, value="//table[@id='provider-table']/tbody/tr/td[3]")

    def click_on_new_button(self):
        self.new_button.click()

    def type_first_name(self, firstname):
        self.element(*self.FIRST_NAME_TEXT).send_keys(firstname)

    def type_last_name(self, lastname):
        self.element(*self.LAST_NAME_TEXT).send_keys(lastname)

    def type_job_title(self, job_title):
        self.element(*self.JOB_TITLE_TEXT).send_keys(job_title)

    def type_vsee_id(self, vsee_id):
        self.element(*self.VSEE_ID_TEXT).send_keys(vsee_id)

    def active(self, active):
        if(active == True):
            self.clickOnElement(*self.STATUS_CHECKBOX)

    def select_department(self, department):
        self.clickOnElement(*self.DEPARTMENT_BOX)
        self.element(*self.SEARCH_TEXT).send_keys(department + Keys.ENTER)

    def click_on_create_button(self):
        self.clickOnElement(*self.CREATE_BUTTON)
        sleep(5)

    def provider_found(self):
        """list_mail = self.getSourceHTML()
        # Regex Extract Email
        emails = re.findall(r'[\w\.-]+@[\w\.-]+', list_mail)
       """
        return self.first_row.text

    def provider_not_found(self):
        page = self.getSourceHTML()
        return "No matching records found" in page

    def search_provider(self, email):
        element = self.element(*self.SEARCH_BOX)
        element.clear()
        element.send_keys(email)
        element.send_keys(Keys.TAB)
        sleep(5)

    def delete_provider(self):
        self.clickOnElement(*self.DEL_BUTTON)
        self.acceptAlert()
        sleep(5)

    def edit_provider_by_email(self):
        self.clickOnElement(self.EDIT_BUTTON)

    # Filter provider has status is inactive
    def show_inactive_users(self):
        self.clickOnElement(self.ACTIVE_CHECKBOX)
