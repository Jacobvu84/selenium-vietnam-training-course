__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from util.mailbox import MailBox
from util.date_time import get_current_datetime

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.patient_steps import PatientHomeSteps
from steps.mail_box import MailBoxSteps

from model.provider import main_email
from model.provider import email_pwd

from model.patient import patient_gmail
from model.patient import password_gmail

testID = sys.argv[1]  # test case ID


def nurse_cancel_appointment():
    # Objects
    _actor = LoginSteps()
    _patient = PatientHomeSteps()
    _mailbox = MailBoxSteps()

    with MailBox(patient_gmail, password_gmail) as mbox:
        mbox.delete_all()

    try:

        _actor.access_waiting_room().signin_as_patient(2)
        _patient.schedule_appointment(2)

        _patient.do_you_want_to_cancel_this_upcoming_appointment("no")
        _patient.do_you_want_to_cancel_this_upcoming_appointment("yes")

        # provider checks email of Appointment Cancellation
        with MailBox(main_email, email_pwd) as inbox:
            content = _mailbox.get_content_in_email(mail_title=_mailbox.cancel_appointment, mbox=inbox)

        time_slot = _patient.time

        assert "The appointment for {0} {1} (PDT) with you has been canceled.".\
                   format(get_current_datetime(), time_slot) in content

        # patient checks email of Appointment Cancellation
        with MailBox(patient_gmail, password_gmail) as inbox:
            content_ = _mailbox.get_content_in_email(mail_title=_mailbox.cancel_appointment, mbox=inbox)

        assert "appointment for {0} {1} (PDT) has been canceled.".format(get_current_datetime(), time_slot) in content_

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
        _actor.quit()
        create_gif()


def main():
    start_test()
    nurse_cancel_appointment()


main()
