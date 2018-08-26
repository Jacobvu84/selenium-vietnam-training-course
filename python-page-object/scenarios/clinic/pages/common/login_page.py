__author__ = 'jacob@vsee.com'

import os, sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../../")
from selenium.webdriver.common.by import By
from webium.clinic_page import ClinicPage
from webium.base_page import Test 


class LoginPage(ClinicPage):
    def __init__(self, ClinicPage):
        self.set_attribute(ClinicPage)
    
    click_here_to_login = (By.PARTIAL_LINK_TEXT, 'Click here to log in.')
    login_button = (By.PARTIAL_LINK_TEXT, 'Login')
    sign_up = (By.PARTIAL_LINK_TEXT, 'Sign Up')
    username = (By.ID, 'AppUserUsername')
    password = (By.ID, 'AppUserPassword')
    submit_button = (By.XPATH, '//button[contains(text(),"Sign In")]')
    full_nanme = (By.XPATH, "//*[@class='username']")

    @Test(click_here_to_login)
    def click_on_login_link(self):
        # For Admin, SA, Provider e.t.c
        self.element(*self.click_here_to_login) \
            .highlight_element().click()
#             .wait_until_clickable() \
        return self

    @Test(login_button)
    def click_on_login_button(self):
        # For patient
        self.element(*self.login_button) \
            .wait_until_clickable() \
            .highlight_element().click()
        return self

    @Test(username)
    def enter_username(self, username):
        self.element(*self.username) \
            .wait_until_clickable() \
            .highlight_element() \
            .type(username)
        return self

    @Test()
    def enter_password(self, pwd):
        self.enter_text_into(pwd, *self.password)
        return self

    @Test(submit_button)
    def click_on_submit_button(self):
        self.element(*self.submit_button).highlight_element().click_and_wait(10)
        return self

    @Test()
    def get_title_page(self):
        return self.get_title()

    @Test(full_nanme)
    def get_full_name_user(self):
        return self.element(*self.full_nanme).get_text_value()

    @Test()
    def user_logout(self):
        self.get_driver().get(self.get_url() + "/users/logout")
        return self

    @Test(sign_up)
    def click_on_sign_up(self):
        self.element(*self.sign_up).highlight_element().click()
        return self

    forget_pwd = (By.ID, "GuestUserResetPassword")

    @Test(forget_pwd)
    def click_on_the_forget_password(self):
        self.element(*self.forget_pwd).highlight_element().click()
        return self

    email_txt = (By.ID, "AppUserEmail")

    @Test(email_txt)
    def enter_the_email(self, email):
        self.element(*self.email_txt).wait_until_visible().clear().type(email)
        return self

    reset_pwd = (By.XPATH, "//button[contains(text(),'Reset your Password')]")

    @Test(reset_pwd)
    def click_on_reset_your_email(self):
        self.element(*self.reset_pwd).click_and_wait(2)
        return self

    warning_email = (By.ID, "AppUserEmail-error")

    @Test(warning_email)
    def get_warning_message(self):
        return self.element(*self.warning_email).wait_until_present().get_text_value()

    alert_success_msg = (By.XPATH, "//div[@class='alert alert-success fade in']")

    @Test(alert_success_msg)
    def get_alert_success_message(self):
        return self.element(*self.alert_success_msg).wait_until_present().get_text_value()

    new_pwd = (By.ID, 'AppUserNewPassword')

    @Test(new_pwd)
    def enter_new_password(self, pwd):
        self.element(*self.new_pwd).clear().type(pwd)
        return self

    confirm_pwd = (By.ID, 'AppUserConfirmPassword')

    @Test(confirm_pwd)
    def enter_confirm_password(self, pwd):
        self.element(*self.confirm_pwd).clear().type(pwd)
        return self

    submit_btn = (By.XPATH, "//button[@type='submit']")

    @Test(submit_btn)
    def reset(self):
        self.element(*self.submit_btn).click_and_wait(5)
        return self

    succ_msg = (By.XPATH, "//div[@class='alert alert-info']")

    @Test(succ_msg)
    def get_success_message(self):
        return self.element(*self.succ_msg).wait_until_present().get_text_value().encode('utf-8')

    err_msg = (By.XPATH, "//div[@class='alert alert-danger']")

    @Test(err_msg)
    def get_error_message(self):
        return self.element(*self.err_msg).wait_until_present().get_text_value().encode('utf-8')

    account_profile = (By.XPATH, "//ul[@class='dropdown-menu']//a[contains(.,'My Profile')]")

    @Test(account_profile)
    def click_on_user_profile(self, full_name):
        user_name = (By.XPATH, "//a[@id='top_menu_content_user']/span[text()='{0}']".format(full_name))
        self.element(*user_name).wait_until_clickable().click()

        # Tips: Make sure My Profile is expanse
        if not self.element(*self.account_profile).is_present():
            self.element(*user_name).wait_until_clickable().click()

        self.element(*self.account_profile).click_and_wait(3)
        return self

    admin_panel = (By.XPATH, "//ul[@class='dropdown-menu']//a[contains(.,'Admin panel')]")

    @Test(admin_panel)
    def click_on_admin_panel(self, full_name):
        user_name = (By.XPATH, "//a[@id='top_menu_content_user']/span[text()='{0}']".format(full_name))
        self.element(*user_name).wait_until_clickable().click()

        # Tips: Make sure My Profile is expanse
        if not self.element(*self.account_profile).is_present():
            self.element(*user_name).wait_until_clickable().click()

        self.element(*self.admin_panel).click_and_wait(3)
        return self

    my_clinic = (By.XPATH, "//ul[@class='dropdown-menu']//a[contains(.,'My Clinic')]")

    @Test(my_clinic)
    def click_on_my_clinic(self, full_name):
        user_name = (By.XPATH, "//a[@id='top_menu_content_user']/span[text()='{0}']".format(full_name))
        self.element(*user_name).wait_until_clickable().click()

        # Tips: Make sure My Profile is expanse
        if not self.element(*self.account_profile).is_present():
            self.element(*user_name).wait_until_clickable().click()

        self.element(*self.my_clinic).click_and_wait(3)
        return self
