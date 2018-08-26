__author__ = 'jacob@vsee.com'

import os
import sys

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.console import start_test
from util.support import create_gif
from resource import ODTC

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.font_end.provider.my_clinic import MyClinicSteps


testID = sys.argv[1]  # test case ID


# Tester thread
def provider_update_visit_option_in_my_clinic():
    _actor = LoginSteps()
    _my_clinic = MyClinicSteps()
    odtc = ODTC()

    room_name = odtc.get_room_name_by(env='tele')
    index = 0
    try:
        _actor\
            .visit_telepsych() \
            .signin_as_provider(env='tele', index=index)\
            .access_my_clinic(env='tele', index=index)

        _my_clinic\
            .choose_waiting_room(room=room_name)\
            .description("Welcome to the room")\
            .add_new_visit_option(option='30-min Consultation', duration='30')\
            .should_see_message('Success! Update room details successfully')

        print "[PASSED]: TEST PASSED"
    except Exception as e:
        print type(e)
        print e.args
        print e
        print "[FAILED]: TEST FAILED"

    finally:
        _actor.quit()
        create_gif()


def main():
    start_test()
    provider_update_visit_option_in_my_clinic()


main()
