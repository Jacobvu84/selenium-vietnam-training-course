__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.account_steps import ProviderProfileSteps
from steps.login_steps import LoginSteps

testID = sys.argv[1]  # test case ID


def edit_profile():
    # Objects
    _actor = LoginSteps()
    _profile = ProviderProfileSteps()
    odtc = ODTC()

    provider = odtc.get_cep_provider()
    email = provider[2].split(",")[0]
    f_name = provider[2].split(",")[1]
    l_name = provider[2].split(",")[2]
    full_name = f_name + " " + l_name
    dea = provider[2].split(",")[4]
    npi = provider[2].split(",")[5]

    try:
        _actor.browse_the_web().signin_as_provider(index=2).open_profile(full_name=full_name)
        _profile.should_see_profile_information(email=email,
                                                first_name=f_name,
                                                last_name=l_name,
                                                short_bio="evisitqa06+test{last_name}@gmail.com",
                                                street_address="514 S. Magnolia St.",
                                                city="Orlando",
                                                state="Florida",
                                                zipcode="32806",
                                                phone_number="650.390.6970",
                                                timezone="UTC-07:00 Pacific Time (US & Canada)",
                                                DEA=dea,
                                                NPI=npi,
                                                educational_training="".ljust(1),
                                                professional_interests="".ljust(1),
                                                personal_interests="".ljust(1))
        _profile.edit_profile(first_name=l_name,
                              last_name=f_name,
                              short_bio="The life is not real",
                              street_address="7500 Security Boulevard",
                              city="Baltimore",
                              state="Maryland",
                              zipcode="21244",
                              phone_number="650.390.9999",
                              timezone="UTC-08:00 Alaska",
                              DEA="FJ0419999",
                              NPI="1234567893",
                              educational_training="Master's Degree in Healthcare Informatics",
                              professional_interests="Exploring the relationship between social media",
                              personal_interests="traveling and long walks on the beach",
                              photo="no")

        _profile.should_see_profile_information(email=email,
                                                first_name=l_name,
                                                last_name=f_name,
                                                short_bio="The life is not real",
                                                street_address="7500 Security Boulevard",
                                                city="Baltimore",
                                                state="Maryland",
                                                zipcode="21244",
                                                phone_number="650.390.9999",
                                                timezone="UTC-08:00 Alaska",
                                                DEA="FJ0419999",
                                                NPI="1234567893",
                                                educational_training="Master's Degree in Healthcare Informatics",
                                                professional_interests="Exploring the relationship between social media",
                                                personal_interests="traveling and long walks on the beach")
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
