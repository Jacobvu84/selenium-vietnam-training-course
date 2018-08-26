__author__ = 'jacob@vsee.com'

import os
import sys
import logging

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../")
from steps.login_steps import LoginSteps
from steps.navigate_steps import NavigateSteps
from steps.backend.room.room_steps import RoomSteps

from model.room import RoomData

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from util.logger import setup_logger
from util.console import start_test
from util.support import mkdir
from util.support import TEMP_DIR_WIN
from util.support import create_gif
from resource import ODTC

testID = sys.argv[1]  # test case ID


def create_room():
    # Objects
    _actor = LoginSteps()
    _navigate = NavigateSteps()
    _room = RoomSteps()

    data = RoomData()

    mkdir("bin")
    setup_logger('room', TEMP_DIR_WIN + 'bin\\room.log', level=logging.DEBUG)
    log = logging.getLogger('room')

    try:
        _actor.browse_the_web().login_as(username="admin", password="Evc0nnect=")
        _navigate.goto_room_screen()

        rooms = data.get_cep_room()

        for room in rooms[0:3]:
            """[TEST] CREATE A ROOM"""
            log.debug(room.url + "," + room.slug + "," + room.code + "," + room.name + ",[end]")
            _room.add_new_room(room).should_see_the_room_in_room_table()

        """
        [TEST] DELETE A ROOM:
        room[x].split(",")[y]
          - x: number of row/records of room (from 0)
          - y: 0 - url
               1 - slug
               2 - code
        """
        odtc = ODTC()
        room = odtc.get_cep_room()
        slug = room[2].split(",")[1]

        _room.delete_room(slug).should_see_the_room_is_delete()

        print "[PASSED]: TEST PASSED"
    # Catch any exception from test failure
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
    create_room()


main()
