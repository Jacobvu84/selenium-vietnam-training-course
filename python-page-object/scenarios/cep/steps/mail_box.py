__author__ = 'jacob@vsee.com'

import os
import sys
from waiting import wait

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../../")
from webium.base_page import BasePage

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import Test
from util.setting import _project_name
from util.setting import _snf_name
from util.setting import _telesych_name
from util.setting import _neuro_name

class MailBoxSteps(BasePage):

    # Mail tile in project
    welcome_provider = "Welcome to " + _project_name
    cancel_appointment = _project_name + " appointment canceled"
    visit_summary = "Your visit summary is available"
    make_appointment = "Your appointment has been scheduled"
    appointment_schedule = "Someone has scheduled an appointment with you"
    reset_password = _project_name + " Password Reset"
    active_account = "Activate your " + _project_name + " account"
    visit_notification = _project_name + " walk-in notification"

    # SNF
    welcome_snf = "Welcome to " + _snf_name

    # Tele-Psych
    welcome_telepsych = "Welcome to " + _telesych_name

    # Neuro
    welcome_neuro="Welcome to " + _neuro_name

    @Test()
    def open_link_from_email(self, mail_title, mbox, time_out=600):
        self.wait_for_email(mail_title, mbox, time_out)
        self.open_url(self._link)
        return self

    @Test()
    def get_content_in_email(self, mail_title, mbox):
        self.wait_for_content_email(mail_title, mbox)
        return self._content

    def is_link_in_mail(self, mail_title, mbox):
        self._link, content = mbox.get_link_and_content_mail(mail_title)
        if self._link:
            return True

    def is_content_in_mail(self, mail_title, mbox):
        link, self._content = mbox.get_link_and_content_mail(mail_title)
        if self._content:
            return True

    @Test()
    def wait_for_email(self, mail_title, mbox, time_out=600):
        wait(lambda: self.is_link_in_mail(mail_title, mbox), waiting_for='Wait For Link in the Email',
             timeout_seconds=time_out)

    @Test()
    def wait_for_content_email(self, mail_title, mbox, time_out=600):
        wait(lambda: self.is_content_in_mail(mail_title, mbox), waiting_for='Wait For Content in the Email',
             timeout_seconds=time_out)