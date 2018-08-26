__author__ = 'jacob@vsee.com'

from support import empty_dir_target
import logging


def start_test():
    log = logging.getLogger('report')
    empty_dir_target()
    log.debug("\n")
    log.debug(" |__   __|  ____|/ ____|__   __|  / ____|__   __|/\\   |  __ \\__   __|")
    log.debug("    | |  | |__  | (___    | |    | (___    | |  /  \\  | |__) | | |   ")
    log.debug("    | |  |  __|  \\___ \\   | |     \\___ \\   | | / /\\ \\ |  _  /  | |")
    log.debug("    | |  | |____ ____) |  | |     ____) |  | |/ ____ \\| | \\ \\  | |   ")
    log.debug("    |_|  |______|_____/   |_|    |_____/   |_/_/    \\_\\_|  \\_\\ |_| \n")
