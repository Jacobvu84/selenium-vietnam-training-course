__author__ = 'jacob@vsee.com'

import sys, os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from page.login_page import LoginPage
from util.assertions import Assert
from util.setting import _snf_url
from util.setting import _telesych_url
from util.setting import _neuro_url
from util.logger import Test

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from resource import ODTC
from model.patient import patient_pwd
from model.provider import new_pass
import time


class LoginSteps(Assert):
    on_login_page = LoginPage()
    odtc = ODTC()

    def browse_the_web(self):
        self.on_login_page.open()
        self.open_login_form()
        return self

    def visit_telepsych(self):
        self.on_login_page.navigate_to(url=_telesych_url)
        self.open_login_form()
        return self

    def visit_snf(self):
        self.on_login_page.navigate_to(url=_snf_url)
        self.open_login_form()
        return self

    def visit_neuro(self):
        self.on_login_page.navigate_to(url=_neuro_url)
        self.open_login_form()
        return self

    @Test()
    def signin_as_provider(self, env='cep', index=0):
        email = self.odtc.get_email_provider(env=env, index=index)
        self.login_as(email, new_pass)
        return self

    def signin_as_patient(self, index=0):
        email = self.odtc.get_email_patient(index=index)
        self.login_as(email, patient_pwd)
        return self

    def signin_as_nurse(self, env='snf', index=0):
        username = self.odtc.get_nurse_username(env=env, index=index)
        self.login_as(username, patient_pwd)
        return self

    # Patient
    def access_waiting_room(self, env='cep', index=0):
        if 'cep' == env:
            room = self.odtc.get_cep_room()
        elif 'snf' == env:
            room = self.odtc.get_snf_room()
        elif 'neu' == env:
            room = self.odtc.get_neuro_room()
        else:
            room = self.odtc.get_tele_room()

        url = room[index].split(",")[0]
        self.on_login_page.navigate_to(url)
        time.sleep(3)
        self.on_login_page.click_on_login()
        return self

    def enter_waiting_room(self, env='neu', index=0):
        if 'cep' == env:
            room = self.odtc.get_cep_room()
        elif 'snf' == env:
            room = self.odtc.get_snf_room()
        elif 'neu' == env:
            room = self.odtc.get_neuro_room()
        else:
            room = self.odtc.get_tele_room()

        url = room[index].split(",")[0]
        self.on_login_page.navigate_to(url)
        time.sleep(3)
        return self

    def login_as(self, username="admin", password="Evc0nnect="):
        self.on_login_page.enter_username(username)
        self.on_login_page.enter_password(password)
        self.on_login_page.click_on_submit_button()
        return self

    def should_see_full_name(self, fullname):
        self.verifyEquals(
            self.on_login_page.get_full_name_user(), fullname)
        return self

    def should_see_title_page(self, title_page):
        # Verifies that the hardcoded text "eVisit-Dev" appears in page title
        assert title_page in self.on_login_page.get_title_page(), title_page + " title doesn't match."

    def quit(self):
        # self.on_login_page.getDriver().quit()
        # self.on_login_page._driver.quit()
        self.on_login_page.close()

    def logout(self):
        self.on_login_page.user_logout()
        return self

    def sign_up(self):
        self.on_login_page.click_on_sign_up()
        return self

    def open_login_form(self):
        self.on_login_page.click_on_login_link()
        return self

    def expanse_forget_password_form(self):
        self.on_login_page.click_on_the_forget_password()
        return self

    def ask_reset_password(self):
        self.on_login_page.click_on_reset_your_email()
        return self

    def provides_email_to_restore_password(self, email):
        self.on_login_page.enter_the_email(email)
        self.ask_reset_password()
        return self

    def should_see_warning_message(self, msg):
        self.verifyEquals(
            self.on_login_page.get_warning_message(), msg)
        return self

    def should_see_success_message(self, msg):
        self.verifyEquals(
            self.on_login_page.get_alert_success_message(), msg)
        return self

    def reset_your_password(self, password, confirm_password):
        self.on_login_page.enter_new_password(password) \
            .enter_confirm_password(confirm_password).reset()
        return self

    def should_see_error_message(self, err_msg):
        self.verifyContainsString(err_msg, self.on_login_page.get_error_message())
        return self

    def should_see_password_changed(self, ok_msg):
        self.verifyContainsString(ok_msg, self.on_login_page.get_success_message())
        return self

    def open_profile(self, full_name):
        self.on_login_page.click_on_user_profile(full_name)
        return self

    @Test()
    def access_admin_panel(self, env='cep', index=0):
        full_name = self.odtc.get_fullname_provider(env=env, index=index)
        self.on_login_page.click_on_admin_panel(full_name)
        return self

    def access_my_clinic(self, env='cep', index=0):
        full_name = self.odtc.get_fullname_provider(env=env, index=index)
        self.on_login_page.click_on_my_clinic(full_name)
        return self

    def should_see_providers(self, providers):
        self.on_login_page.wait_a_bit(5)
        for provider in providers:
            f_name = provider.split(",")[1]
            l_name = provider.split(",")[2]
            full_name = "Dr. " + f_name + " " + l_name + ", Ph.D"
            self.verifyContainsString(full_name, self.on_login_page.get_providers())
        return self
