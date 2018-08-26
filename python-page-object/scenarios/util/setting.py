import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)) + "/../../")
from properties import Properties
cfg = Properties("vsee.properties")

_capture_mode = str(cfg.take_screenshots())
_wait_timeout = float(cfg.explicit_time_out())
_webdriver_driver = cfg.webdriver_driver()
_implicit_timeout = float(cfg.implicitly_time_out())
_empty_log = str(cfg.empty_log())
_record_screen = str(cfg.record_screen())
_take_screenshot_driver_exception = cfg.take_screenshots_on_driver_exception()
_take_screenshot_browser = cfg.take_screenshots_on_browser()

# On-Duty
_domain = str(cfg.project_domain())
_version = str(cfg.project_version())
_url = str(cfg.base_url())
_project_name = str(cfg.project_name())

# Tele-Psych
_telesych_domain = str(cfg.telesych_domain())
_telesych_version = str(cfg.telesych_version())
_telesych_url = str(cfg.telesych_url())
_telesych_name = str(cfg.telesych_name())

# SNF
_snf_domain = str(cfg.snf_domain())
_snf_version = str(cfg.snf_version())
_snf_url = str(cfg.snf_url())
_snf_name = str(cfg.snf_name())

# Neuro
_neuro_domain = str(cfg.neuro_domain())
_neuro_version = str(cfg.neuro_version())
_neuro_url = str(cfg.neuro_url())
_neuro_name = str(cfg.neuro_name())

# Decorator
_wait_decorator = float(cfg.decorator_speed())
