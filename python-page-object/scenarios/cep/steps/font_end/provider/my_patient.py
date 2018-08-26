__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from page.font_end.provider.my_patient import MyPatientPage
from page.font_end.provider.my_patient import AllVisitPage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from util.assertions import Assert
from util.date_time import get_current_datetime
from util.logger import Test
from util.date_time import calculate_age

from resource import ODTC

class MyPatientSteps(Assert):

    on_my_patient_page = MyPatientPage()

    def has_tab(self, tab_name):
        self.verifyEquals(self.on_my_patient_page.is_tab_active(tab_name), True)
        return self

    def select_tab(self, tab_name):
        self.on_my_patient_page.focus_on_tab(tab_name)
        return self

    def should_see_my_patient_table_with_title(self, columns):
        cols = columns.split(",")
        col_index = 1
        for col in cols:
            self.verifyEquals(col, self.on_my_patient_page.get_column_title_of_my_patient_table(col_index))
            col_index = col_index + 1
        return self

    def should_see_no_data_available_in_table(self):
        self.verifyEquals(self.on_my_patient_page.get_data_table_empty(), "No data available in table")
        return self

    def should_see_name_patient(self, name=""):
        self.verifyContainsString(name, self.on_my_patient_page.get_patient_name())
        return self

    def should_see_gender_patient(self, gender=""):
        self.verifyEquals(gender, self.on_my_patient_page.get_patient_gender())
        return self

    def should_see_age_patient(self, age=""):
        self.verifyContainsString(age, self.on_my_patient_page.get_patient_age())
        return self

    def should_see_email_patient(self, email=""):
        if "" != email:
            self.verifyEquals(email, self.on_my_patient_page.get_patient_email())
        return self

    def should_see_phone_patient(self, phone=""):
        if "" != phone:
            self.verifyEquals(phone, self.on_my_patient_page.get_patient_phone())
        return self

    def should_see_last_visit_patient(self, times):
        self.verifyContainsString(times, self.on_my_patient_page.get_date_last_visit())
        return self

    def go_to_visit_note(self, full_name):
        self.on_my_patient_page.click_on_patient_name(full_name)
        return self

    def search_patient_by(self, value):
        self.on_my_patient_page.enter_search_box(value)
        return self

    def should_see_no_matching_records_found(self):
        self.verifyEquals(
            self.on_my_patient_page.get_text_no_matching_records_found(), "No matching records found")
        return self

    def should_see_default_number_rows_is_shown(self, value):
        self.verifyEquals(self.on_my_patient_page.get_default_show_entries(), value)
        return self

    def should_see_all_options(self, options):
        self.verifyEquals(options, self.on_my_patient_page.get_all_options_show_entries())
        return self

    def should_see_avatar_with_size(self, width, height):
        self.verifyEquals(width, self.on_my_patient_page.get_width_avatar())
        self.verifyEquals(height, self.on_my_patient_page.get_height_avatar())
        return self

    def should_see_full_name(self, full_name):
        self.verifyEquals(full_name, self.on_my_patient_page.get_full_name())
        return self

    def should_see_the_email(self, email):
        self.verifyContainsString(email, self.on_my_patient_page.get_email())
        return self

    @Test(("Group Steps", ""))
    def should_see_the_upcoming_visits_table_with_columns(self, columns):
        cols = columns.split(",")
        col_index = 1
        for col in cols:
            self.verifyEquals(col, self.on_my_patient_page.get_column_title_of_upcoming_visits(col_index))
            col_index = col_index + 1
        return self

    @Test(("Group Steps", ""))
    def should_see_the_visit_history_table_with_columns(self, columns):
        cols = columns.split(",")
        col_index = 1
        for col in cols:
            self.verifyEquals(col, self.on_my_patient_page.get_column_title_of_visit_history(col_index))
            col_index = col_index + 1
        return self

    def back_to_my_patient(self):
        self.on_my_patient_page.click_on_back_to_my_patient()
        return self

    @Test(("Group Steps", ""))
    def should_see_the_all_visit_history_table_with_columns(self, columns):
        cols = columns.split(",")
        col_index = 1
        for col in cols:
            self.verifyEquals(col, self.on_my_patient_page.get_column_title_of_all_visit_history(col_index))
            col_index = col_index + 1
        return self

    @Test(("Group Steps", ""))
    def should_see_the_headings(self, headings):
        _headings = headings.split(",")
        index = 1
        for heading in _headings:
            self.verifyEquals(heading, self.on_my_patient_page.get_heading(index))
            index = index + 1
        return self


class AllVisitSteps(Assert):

    on_visit_history_page = AllVisitPage()

    def show_entries(self, rows):
        self.on_visit_history_page.select_number_records_per_page(rows)
        return self

    def search_history_visit_by(self, value):
        self.on_visit_history_page.enter_search_box(value)
        return self

    def should_see_the_status_visit(self, value):
        self.verifyEquals(value, self.on_visit_history_page.get_visit_status())
        return self

    def should_see_the_patient_name(self, patient):
        self.verifyContainsString(patient, self.on_visit_history_page.get_patient_name())
        return self

    def should_see_the_provider_name(self, patient):
        self.verifyContainsString(patient, self.on_visit_history_page.get_provider_name())
        return self

    def should_see_the_waiting_room(self, waiting_room):
        self.verifyContainsString(waiting_room, self.on_visit_history_page.get_waiting_room())
        return self

    def should_see_the_email(self, email):
        self.verifyEquals(email, self.on_visit_history_page.get_patient_email())
        return self

    def should_see_no_matching_records_found(self):
        self.verifyEquals(
            self.on_visit_history_page.get_text_no_matching_records_found(), "No matching records found")
        return self

    def should_see_visit_information(self, index):
        self.patient_information(index)
        self.provider_information(0)
        self.verifyContainsString(get_current_datetime(), self.on_visit_history_page.get_visit_time())
        self.should_see_the_status_visit("Completed")
        return self

    def should_see_appointment_information(self, index):
        self.patient_information(index)
        self.provider_information(0)
        self.verifyContainsString(get_current_datetime(), self.on_visit_history_page.get_visit_time())
        self.should_see_the_status_visit("Confirmed")
        return self

    def patient_information(self, index=0):
        odtc = ODTC()

        patients = odtc.get_cep_patient()
        patient_email = patients[index].split(",")[0]
        f_name = patients[index].split(",")[1]
        l_name = patients[index].split(",")[2]
        patient_name = f_name + " " + l_name
        dob = patients[index].split(",")[3]

        age = calculate_age(dob)
        # room
        rooms = odtc.get_cep_room()
        name_room = rooms[0].split(",")[3]

        self.verifyContainsString(patient_name, self.on_visit_history_page.get_patient_name())
        self.verifyEquals(patient_email, self.on_visit_history_page.get_patient_email())

        self.verifyEquals(name_room, self.on_visit_history_page.get_waiting_room())
        self.verifyEquals("Male", self.on_visit_history_page.get_patient_gender())
        self.verifyEquals(age, self.on_visit_history_page.get_patient_age())
        self.verifyEquals("View", self.on_visit_history_page.get_action())
        return self

    @Test(("Group Steps", ""))
    def provider_information(self, index=0):
        odtc = ODTC()
        # Providers
        provider_name = odtc.get_fullname_provider(index=index)

        # room
        rooms = odtc.get_cep_room()
        name_room = rooms[0].split(",")[3]

        patients = odtc.get_cep_patient()
        dob = patients[index].split(",")[3]
        age = calculate_age(dob)

        self.verifyContainsString(provider_name, self.on_visit_history_page.get_provider_name())
        self.verifyEquals(name_room, self.on_visit_history_page.get_waiting_room())
        self.verifyEquals("Male", self.on_visit_history_page.get_patient_gender())
        self.verifyEquals(age, self.on_visit_history_page.get_patient_age())
        self.verifyEquals("View", self.on_visit_history_page.get_action())
        return self

    def view(self):
        self.on_visit_history_page.select_view_visit_history()
        return self

    def has_tab(self, tab_name):
        self.verifyEquals(self.on_visit_history_page.is_tab_active(tab_name), True)
        return self

    def change_sorting_by(self, column):
        self.on_visit_history_page.click_on_column_title(column)
        return self

    def default_sorting_by(self, column, sort_by):
        self.verifyEquals(self.on_visit_history_page.is_active_sort(column), sort_by)
        return self

    def should_see_sorting(self, column, label):
        self.verifyEquals(self.on_visit_history_page.get_label_sorting(column), label)
        return self
