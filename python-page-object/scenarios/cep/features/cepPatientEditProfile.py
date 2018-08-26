__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.account_steps import PatientProfileSteps
from steps.login_steps import LoginSteps

testID = sys.argv[1]  # test case ID


def edit_profile():
    # Objects
    _actor = LoginSteps()
    _profile = PatientProfileSteps()
    odtc = ODTC()

    patient = odtc.get_cep_patient()
    email = patient[2].split(",")[0]
    f_name = patient[2].split(",")[1]
    l_name = patient[2].split(",")[2]
    full_name = f_name + " " + l_name

    try:
        _actor.access_waiting_room().signin_as_patient(2).open_profile(full_name=full_name)
        _profile.should_see_profile_information(password="xxxxxxxxxxxx",
                                                email=email,
                                                first_name=f_name,
                                                last_name=l_name,
                                                gender="Male",
                                                dob="December 24, 2012",
                                                street_address="".ljust(1),
                                                city="".ljust(1),
                                                state="Alabama",
                                                zipcode="36445",
                                                phone_number="".ljust(1),
                                                timezone="UTC-07:00 Pacific Time (US & Canada)",
                                                primary_care_physician_name="".ljust(1),
                                                primary_care_physician_phone="".ljust(1))
        _profile.edit_profile(first_name="none",
                              last_name="none",
                              gender="none",
                              dob="none",
                              street_address="10075 62ND st N",
                              city="Pinellas Park",
                              state="Florida",
                              zipcode="32745",
                              phone_number="0988345678",
                              timezone="UTC+07:00 Hanoi, Hochiminh City, Bangkok",
                              primary_care_physician_name="WHO Headquarters in Geneva",
                              primary_care_physician_phone="+41-22-79121",
                              photo="yes")

        _profile.should_see_profile_information(password="xxxxxxxxxxxx",
                                                email=email,
                                                first_name=f_name,
                                                last_name=l_name,
                                                gender="Male",
                                                dob="December 24, 2012",
                                                street_address="10075 62ND st N",
                                                city="Pinellas Park",
                                                state="Florida",
                                                zipcode="32745",
                                                phone_number="0988345678",
                                                timezone="UTC+07:00 Hanoi, Hochiminh City, Bangkok",
                                                primary_care_physician_name="WHO Headquarters in Geneva",
                                                primary_care_physician_phone="+41-22-79121")
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
    edit_profile()


main()
