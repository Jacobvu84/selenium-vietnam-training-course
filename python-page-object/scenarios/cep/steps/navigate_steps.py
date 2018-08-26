__author__ = 'jacob@vsee.com'

import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.navigation_page import NavigatePage


class NavigateSteps():
    # Navigation in the back end
    on_navigate_page = NavigatePage()

    def goto_provider_screen(self):
        self.on_navigate_page \
            .go_to_provider_screen().select_provider_tab()

    def goto_all_user_screen(self):
        self.on_navigate_page \
            .go_to_provider_screen()

    def goto_room_screen(self):
        self.on_navigate_page.go_to_room_screen()

    def goto_clinic_screen(self):
        self.on_navigate_page.go_to_clinic_screen()

    # Navigation in the front end: Provider
    def goto_patient_page(self):
        self.on_navigate_page.go_to_patient_page()
        return self

    def goto_calendar_page(self):
        self.on_navigate_page.go_to_calendar_page()

    # Navigation in the front end: Patient
    def goto_health(self):
        self.on_navigate_page.go_to_health_page()

    def goto_home_page(self):
        self.on_navigate_page.go_to_home_page()

    def goto_dashboard(self):
        self.on_navigate_page.go_to_dashboard()

    def goto_help_page(self):
        self.on_navigate_page.go_to_help_page()

    def goto_visit_page(self):
        self.on_navigate_page.go_to_visit_page()

    def goto_my_patients(self):
        self.on_navigate_page.go_to_my_patient()
        return self

    def re_type_password(self):
        """
        Just for Nurse on Telep
        """
        self.on_navigate_page\
            .re_enter_password()\
            .click_on_submit()