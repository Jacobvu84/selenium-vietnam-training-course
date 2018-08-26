__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from util import date_time
from util.mailbox import MailBox
from util.date_time import get_next_date
import datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.patient_steps import PatientHomeSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_schedule import MyScheduleSteps
from steps.install_steps import InstallSteps
from steps.mail_box import MailBoxSteps

from model.provider import main_email
from model.provider import email_pwd

from model.patient import patient_gmail
from model.patient import password_gmail

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
is_install = int(sys.argv[6])  # Install VSee client if equal to 1


def reschedule_appointment():
    # Objects
    _user = LoginSteps()
    _patient = PatientHomeSteps()
    _install = InstallSteps()
    _navigate = NavigateSteps()
    _my_schedule = MyScheduleSteps()
    _mailbox = MailBoxSteps()

    # Time Slot
    start_date = date_time.get_weekday(datetime.datetime.today())
    end_date = date_time.get_next_date(3)
    start_time = "00:00"
    end_time = "00:00"

    try:

        # Given: Provider creates slot in calendar
        _user.browse_the_web().signin_as_provider(index=2)
        _navigate.goto_calendar_page()

        _my_schedule.create_slot(start_date, start_time, end_time) \
            .repeat("Mon,Tue,Wed,Thu,Fri,Sat,Sun") \
            .until(end_date)
        _user.logout()

        # Given: Patient select a provider and book an appointment
        _user.access_waiting_room().signin_as_patient(2)

        _patient.select_a_doctor_and_book_an_appointment_quickly(provider=2, patient=2)
        _navigate.goto_home_page()
        _patient.should_see_start_appointment_in_dashboard("Today")
        _patient.start_his_appointment()

        # Given: Install VSee Messenger
        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        # When: Patient reschedule an appointment
        date_app = date_time.next_day_in_slot()
        _patient.reschedule_appointment(other_day=date_app) \
            .should_see_end_call(testID, src)
        _patient.should_see_start_appointment_in_dashboard(date_app)

        # Then: provider checks email
        with MailBox(main_email, email_pwd) as inbox:
            content = _mailbox.get_content_in_email(mail_title=_mailbox.appointment_schedule, mbox=inbox)

        time_slot = _patient.time

        assert "An appointment has been scheduled with you for {0} {1} (PDT).".format(get_next_date(), time_slot) \
               in content

        # Then: Patient checks email
        with MailBox(patient_gmail, password_gmail) as inbox:
            content_ = _mailbox.get_content_in_email(mail_title=_mailbox.make_appointment, mbox=inbox)

        assert "appointment has been scheduled for {0} {1} (PDT).".format(get_next_date(), time_slot) in content_

        print "[PASSED]: TEST PASSED"
    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[FAILED]: TEST FAILED"
    finally:
        with MailBox(main_email, email_pwd) as mbox:
            mbox.delete_all()
        with MailBox(patient_gmail, password_gmail) as mbox:
            mbox.delete_all()
        _user.quit()
        create_gif()


def main():
    start_test()
    reschedule_appointment()


main()
