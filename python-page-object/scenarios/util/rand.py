from random import *
import string
import calendar, time


def generate(num):
    return str(calendar.timegm(time.gmtime()) / num)


def random_string(size):
    # min_char = size
    # max_char = size + 4
    allchar = string.ascii_letters + string.digits + "_________"
    return "".join(choice(allchar) for x in range(randint(size, size)))


def random_int(size):
    # return randint(10000,99999)
    allchar = string.digits
    return "".join(choice(allchar) for x in range(randint(size, size)))


def random_state():
    state = ['California', 'Nevada', 'Texas', 'Alaska', 'Colorado']
    return choice(state)


def random_npi():
    npi = ['1699779256', '1234567893']
    return choice(npi)


def random_spcial(size):
    allchar = string.ascii_letters + string.punctuation + string.digits
    return "".join(choice(allchar) for x in range(randint(size, size)))


def random_answer(option):
    """
    Give the answers when take the survey
    :param option:
        1 : answer for question "If this telehealth service was not available to me, I would:"
        2 : answer for question "I want the following from my telehealth visit today:"
    :return: random answer is selected
    """
    if option == 1:
        answers = ["Go to an emergency department",
                   "Go to an urgent care",
                   "See my primary care doctor",
                   "Ask a friend or family member what to do",
                   "Wait and hope I get better"
                   ]
        return choice(answers)
    else:
        answers = ["To understand what is wrong with me",
                   "To know that I don't have a dangerous condition",
                   "To have my symptoms (i.e. runny nose, fever, cough, etc.) managed",
                   "To have my pain managed",
                   "To feel better so I can go to work/school",
                   "To get an excuse note for work/school"]
        return choice(answers)


def feedback_on_patient(option):
    """
    Provider will select answer to provide feedback.
    This task is last step, that will do after complete the visit
    :param option:
        1 : answer for question "Were you comfortable addressing the patient's needs through this platform?"
        2 : answer for question "Did you refer the patient for in-person care?"
        3 : answer for question "If Yes, why did you refer for in-person patient care via telehealth?"
    """
    if option == 1:
        answers = ["1. Not comfortable at all",
                   "2. Hardly comfortable",
                   "3. Neutral",
                   "4. Somewhat comfortable",
                   "5. Very comfortable"
                   ]
        return choice(answers)
    elif option == 2:
        answers = ["Yes",
                   "No"
                   ]
        return choice(answers)
    else:
        answers = ["I felt like I needed to conduct an in-person physical exam",
                   "I felt like I needed vital signs",
                   "I felt like lab testing was indicated",
                   "I felt like the patient needed an x-ray",
                   "I felt like the patient required Ultrasound, CT, or MRI",
                   "I felt like the patient required IV medication(s)/fluid"
                   ]
        return choice(answers)
