__author__ = 'jacob@vsee.com'

import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.login_page import LoginPage
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.configured_environment import EnvironmentVariables

class LoginSteps():
    config = EnvironmentVariables()
    _username = config.provider_user()
    _password = config.provider_password()

    on_login_page = LoginPage()

    # Open url on the browser and maximize window
    def open_browser_on(self):
        self.on_login_page.visit()


    # Login the url with username and password
    def sign_in(self, username = _username, pwd=_password):
        self.on_login_page.enter_username(username)
        self.on_login_page.enter_password(pwd)
        self.on_login_page.click_on_submit_button()

    def is_title_matches(self):
        # Verifies that the hardcoded text "eVisit-Dev" appears in page title
        return "eVisit-Dev" in self.on_login_page.get_title_page()
