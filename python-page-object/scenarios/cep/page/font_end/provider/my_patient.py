__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../../")
from webium.base_page import BasePage
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from util.logger import Test


class MyPatientPage(BasePage):
    search_box = (By.XPATH, "//div[@id='tabMyPatients']//input[@type='search']")
    col_xpath = "//table[@id='patients-table']/tbody/tr[1]/td[" \
                "count(//table[@id='patients-table']/thead/tr/th[text()='{0}']/preceding-sibling::*)" \
                " + 1]"

    # Get information on the table room
    def get_text_by_col_name(self, name):
        domain_col = (By.XPATH, self.col_xpath.format(name))
        return self.element(*domain_col).get_text_value()

    @Test(search_box)
    def enter_search_box(self, value):
        self.element(*self.search_box).clear().type(value).type_and_wait(Keys.TAB, 3)
        return self

    @Test(("Undefined", "Undefined"))
    def click_on_patient_name(self, name):
        patient_name = (By.XPATH, "//table[@id='patients-table']//a[text()='{0}']".format(name))
        self.element(*patient_name).click_and_wait(10)

    def get_patient_name(self):
        return self.get_text_by_col_name("Name")

    def get_patient_gender(self):
        return self.get_text_by_col_name("Gender")

    def get_patient_age(self):
        return self.get_text_by_col_name("Age")

    def get_patient_email(self):
        return self.get_text_by_col_name("Email")

    def get_patient_phone(self):
        return self.get_text_by_col_name("Phone Number")

    def get_date_last_visit(self):
        return self.get_text_by_col_name("Date of Last Visit")

    def focus_on_tab(self, tab_name):
        tab = (By.XPATH, "//ul[@class='nav nav-tabs']//a[text()='{0}']".format(tab_name))
        self.element(*tab).wait_until_clickable().click_and_wait(3)
        return self

    @Test(("Undefined", "Undefined"))
    def is_tab_active(self, tab_name):
        self.focus_on_tab(tab_name)

        active_tab = (By.XPATH, "//ul[@class='nav nav-tabs']//a[text()='{0}']/ancestor-or-self::li".format(tab_name))
        tab_status = self.element(*active_tab).get_attribute_value("class")

        if "active" == tab_status:
            return True
        else:
            return False

    no_record = (By.XPATH, "//*[@id='patients-table']//*[@class='dataTables_empty']")

    @Test(no_record)
    def get_text_no_matching_records_found(self):
        return self.element(*self.no_record).wait_for_text_to_appear('No matching records found').get_text_value()

    paging = (By.NAME, "visits-table_length")

    @Test(paging)
    def get_default_show_entries(self):
        return self.element(*self.paging).get_selected_visible_text_value()

    @Test(paging)
    def get_all_options_show_entries(self):
        return self.element(*self.paging).get_all_options()

    avatar = (By.CSS_SELECTOR, ".default-avatar")

    @Test(avatar)
    def get_width_avatar(self):
        return self.element(*self.avatar).capture_element("patient_avatar").get_width()

    @Test(avatar)
    def get_height_avatar(self):
        return self.element(*self.avatar).get_height()

    @Test()
    def get_full_name(self):
        name = (By.XPATH, "//div[@id='patientDetails']/div/strong")
        return self.element(*name).get_text_value()

    @Test()
    def get_email(self):
        email = (By.XPATH, "//div[@id='patientDetails']/div")
        return self.element(*email).get_text_value()

    def get_column_title_of_upcoming_visits(self, col_index):
        table_col = (By.XPATH, "//table[@id='upcomingVisits']/thead/tr/th[{0}]".format(col_index))
        return self.element(*table_col).get_text_value()

    def get_column_title_of_visit_history(self, col_index):
        table_col = (By.XPATH, "//table[@id='pastVisits']/thead/tr/th[{0}]".format(col_index))
        return self.element(*table_col).get_text_value()

    def get_column_title_of_all_visit_history(self, col_index):
        table_col = (By.XPATH, "//table[@id='visits-table']/thead/tr/th[{0}]".format(col_index))
        return self.element(*table_col).get_text_value()

    @Test()
    def click_on_back_to_my_patient(self):
        back_btn = (By.XPATH, "//i[@class='icon fa fa-chevron-left']/following-sibling::span[text()='My Patients']")
        return self.element(*back_btn).wait_until_clickable().highlight_element().click_and_wait(5)

    def get_heading(self, index):
        heading = (By.XPATH, "(//div[@id='medicalHistory']//h4[@class='pull-left'])[{0}]".format(index))
        return self.element(*heading).get_text_value()

    def get_column_title_of_my_patient_table(self, col_index):
        table_col = (By.XPATH, "//table[@id='patients-table']/thead/tr/th[{0}]".format(col_index))
        return self.element(*table_col).get_text_value()

    @Test()
    def get_data_table_empty(self):
        table_empty = (By.XPATH, "//table[@id='patients-table']//td[@class='dataTables_empty']")
        return self.element(*table_empty).get_text_value()

class AllVisitPage(BasePage):
    search_box = (By.XPATH, "//div[@id='visits-table_filter']//input[@type='search']")
    col_xpath = "//table[@id='visits-table']/tbody/tr[1]/td[" \
                "count(//table[@id='visits-table']/thead/tr/th[text()='{0}']/preceding-sibling::*)" \
                " + 1]"

    @Test(search_box)
    def enter_search_box(self, value):
        self.element(*self.search_box).clear().type(value).type_and_wait(Keys.TAB, 5)
        return self

    no_record = (By.XPATH, "//*[@id='visits-table']//*[@class='dataTables_empty']")

    @Test(no_record)
    def get_text_no_matching_records_found(self):
        return self.element(*self.no_record).wait_for_text_to_appear('No matching records found').get_text_value()

    # Get information on the table room
    def get_text_by_col_name(self, name):
        domain_col = (By.XPATH, self.col_xpath.format(name))
        return self.element(*domain_col).get_text_value()

    def get_visit_time(self):
        return self.get_text_by_col_name("Visit Time")

    def get_patient_name(self):
        return self.get_text_by_col_name("Patient")

    def get_waiting_room(self):
        return self.get_text_by_col_name("Waiting Room")

    def get_provider_name(self):
        return self.get_text_by_col_name("Provider")

    def get_patient_gender(self):
        return self.get_text_by_col_name("Gender")

    def get_patient_age(self):
        return self.get_text_by_col_name("Age")

    def get_patient_email(self):
        return self.get_text_by_col_name("Email")

    def get_visit_status(self):
        return self.get_text_by_col_name("Visit Status")

    def get_action(self):
        return self.get_text_by_col_name("Action")

    number_row = (By.NAME, "visits-table_length")

    @Test(number_row)
    def select_number_records_per_page(self, row):
        self.element(*self.number_row).select_option_by_text(row)
        return self

    view_btn = (By.XPATH, "//a[text()='View']")

    @Test(view_btn)
    def select_view_visit_history(self):
        self.element(*self.view_btn).wait_until_present().click_and_wait(2)
        return self

    def focus_on_tab(self, tab_name):
        tab = (By.XPATH, "//ul[@class='nav nav-tabs']//a[text()='{0}']".format(tab_name))
        self.element(*tab).wait_until_present().click_and_wait(2)
        return self

    @Test(("Undefined", "Undefined"))
    def is_tab_active(self, tab_name):
        self.focus_on_tab(tab_name)

        active_tab = (By.XPATH, "//ul[@class='nav nav-tabs']//a[text()='{0}']/ancestor-or-self::li".format(tab_name))
        tab_status = self.element(*active_tab).get_attribute_value("class")

        if "active" == tab_status:
            return True
        else:
            return False

    @Test(("Undefined", "Undefined"))
    def click_on_column_title(self, column):
        title_cols = (By.XPATH, "//table[@id='visits-table']//th[text()='{0}']".format(column))
        self.element(*title_cols).click_and_wait(5)
        return self

    @Test(("Undefined", "Undefined"))
    def is_active_sort(self, column):
        visit_time_col = (By.XPATH, "//table[@id='visits-table']//th[text()='{0}']".format(column))
        return self.element(*visit_time_col).get_attribute_value("aria-sort")

    @Test(("Undefined", "Undefined"))
    def get_label_sorting(self, column):
        visit_time_col = (By.XPATH, "//table[@id='visits-table']//th[text()='{0}']".format(column))
        return self.element(*visit_time_col).get_attribute_value("aria-label")
