from functools import wraps

import driver
import settings


def no_wait(func):
    @wraps(func)
    def without_wait(*args, **kwargs):
        try:
            driver.get_driver().implicitly_wait(0)
            return func(*args, **kwargs)
        finally:
            driver.get_driver().implicitly_wait(settings.implicit_timeout)

    return without_wait
