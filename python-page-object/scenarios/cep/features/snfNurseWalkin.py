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
from steps.install_steps import InstallSteps
from steps.web_chat import WebChatSteps
from steps.navigate_steps import NavigateSteps
from steps.font_end.provider.my_patient import AllVisitSteps
from steps.font_end.nurse.nurse_steps import NurseSteps

from model.patient import patient_gmail
from model.patient import password_gmail

testID = sys.argv[1]  # test case ID
bType = sys.argv[2]  # type of browser
osType = sys.argv[3]  # type of platform
userID = int(sys.argv[4])  # userID
src = sys.argv[5]  # Local VM ID
dst = sys.argv[6]  # Remote VM ID
is_install = int(sys.argv[7])  # Install VSee client if equal to 1


def walk_in():
    # Objects
    _actor = LoginSteps()
    _nurse = NurseSteps()
    _install = InstallSteps()
    _webchat = WebChatSteps()
    _navigate = NavigateSteps()
    _all_visit = AllVisitSteps()

    patient_index = 0

    odtc = ODTC()
    patients = odtc.get_snf_patient()
    f_name = patients[patient_index].split(",")[0]
    l_name = patients[patient_index].split(",")[1]
    dob = patients[patient_index].split(",")[2]

    full_name = f_name + " " + l_name

    provider_full_name = odtc.get_fullname_provider(env='snf')

    try:
        with MailBox(patient_gmail, password_gmail) as mbox:
            mbox.delete_all()

        _actor\
            .visit_snf() \
            .signin_as_nurse(env='snf')

        _nurse \
            .should_see_menu_bar('Dashboard,Patients') \
            .should_contains_menu_item('Dashboard,Patients') \
            .should_see_menu_item_default('Dashboard')

        _nurse\
            .enter_patient_information(first_name=f_name,
                                       last_name=l_name,
                                       dob=dob,
                                       gender="Male") \
            .account_lookup(patient='new') \
            .add_more_patient_information(date_of_most_recent_admission="2017-11-22",
                                          principal_diagnosis_upon_admission_to_the_facility='Hip fracture',
                                          reason_for_visit='Vomiting') \
            .click_to_continue() \
            .patient_vitals(hr='99 BPM',
                            bp='180/120 mmHg',
                            temp='38 C',
                            rr='99 BPM',
                            SpO2='53%',
                            glucose='120 mg/dL',
                            upload='no') \
            .past_medical_history(conditions='CHF, COPD') \
            .should_see_the_past_medical_history_is_updated('CHF, COPD') \
            .past_surgeries(procedures='Heart valve replaced, Hernia repair') \
            .should_see_the_past_surgeries_is_updated('Heart valve replaced, Hernia repair') \
            .allergies(drug_name='5HT1 agonist,12 Hour Nasal') \
            .should_see_the_allergies_is_updated('5HT1 agonist,12 Hour Nasal') \
            .click_to_continue() \
            .please_help_us_improve_our_service_by_answering_the_followin(option='Call nurse supervisor')

        # VM is installed the first time
        if is_install:
            _install.install_vsee()
        _install.launch_vsee(is_install)
        _install.accept_privacy_and_term_GDPR()

        # Launch VM if already installed
        _webchat\
            .wait_for_message_from_sender("How are you going?") \
            .reply_message("Thanks Doctor, I am doing well") \
            .wait_for_message_from_sender("Do you exercise everyday?") \
            .reply_message("Yes, Walking and Running 7km everyday") \
            .wait_for_message_from_sender("Please, Should not eat fish, meat, butter") \
            .reply_message("Absolutely, Yes") \
            .reply_message("Thank you for your advices.") \
            .close_web_chat() \
            .should_not_see_web_chat_of(provider_full_name)

        # Launch VM if already installed
        _nurse.wait_doctor_visit(testID, src, dst) \
            .wait_doctor_complete_visit(testID, src) \
            .patient_rate_and_end_visit()

        _navigate\
            .goto_patient_page()\
            .re_type_password()
        # All Visit is default
        _all_visit \
            .search_history_visit_by(value=full_name) \
            .should_see_the_status_visit("Completed")\
            .view()

        print "[PASSED]: TEST PASSED"

    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[INFO]: TEST FAILED"
    finally:
        _actor.quit()
        create_gif()


def main():
    start_test()
    walk_in()


main()
