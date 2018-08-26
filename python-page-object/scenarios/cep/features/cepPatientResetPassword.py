__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from util.mailbox import MailBox
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.patient.create_account import CreateAccountSteps
from steps.mail_box import MailBoxSteps

from model.patient import patient_gmail
from model.patient import password_gmail

testID = sys.argv[1]  # test case ID


def reset_password():
    # Objects
    _actor = LoginSteps()
    _patient = CreateAccountSteps()
    _mailbox = MailBoxSteps()

    with MailBox(patient_gmail, password_gmail) as mbox:
        mbox.delete_all()


    #email = patient[2].split(",")[0]

    odtc = ODTC()
    email = odtc.get_email_patient(index=2)
    patient = odtc.get_cep_patient()
    f_name = patient[2].split(",")[1]
    l_name = patient[2].split(",")[2]

    try:
        _actor.access_waiting_room().expanse_forget_password_form()

        _actor.provides_email_to_restore_password(email="") \
            .should_see_warning_message("This field is required.")

        _actor.provides_email_to_restore_password(email="jacob.vsee.com") \
            .should_see_warning_message("Please enter a valid email address.")

        _actor.provides_email_to_restore_password(email=email) \
            .should_see_success_message("Success! Please check your email for instruction to reset your password.")

        with MailBox(patient_gmail, password_gmail) as inbox:
            _mailbox.open_link_from_email(mail_title=_mailbox.reset_password, mbox=inbox)

        # All fields are empty
        _actor.reset_your_password(password="", confirm_password="") \
            .should_see_error_message("Please fill in the new password and confirm password fields.")

        # Confirm password is empty
        _actor.reset_your_password(password="VSee@)!*", confirm_password="") \
            .should_see_error_message("Please fill in the new password and confirm password fields.")

        # new password is empty
        _actor.reset_your_password(password="", confirm_password="VSee@)!*") \
            .should_see_error_message("Please fill in the new password and confirm password fields.")

        _actor.reset_your_password(password="VSee2018", confirm_password="Vsee2018") \
            .should_see_error_message("The passwords entered did not match.")

        _actor.reset_your_password(password="vsee", confirm_password="vsee") \
            .should_see_error_message("Input validation failed:The password must have at least 6 characters.")

        _actor.reset_your_password(password="VSee2018@)!*", confirm_password="VSee2018@)!*") \
            .should_see_password_changed("Password changed. You can now login with your new password.")

        _actor.login_as(username=email, password="VSee2018@)!*") \
            .should_see_full_name(f_name + " " + l_name).logout()
        # full name is changed in test case 11004: Provider Edit Account

        print "[PASSED]: TEST PASSED"
    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[FAILED]: TEST FAILED"
    finally:
        with MailBox(patient_gmail, password_gmail) as mbox:
            mbox.delete_all()
        _actor.quit()
        create_gif()


def main():
    start_test()
    reset_password()


main()
