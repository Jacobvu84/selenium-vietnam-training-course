import datetime
from datetime import timedelta
from datetime import date
from random import randint


def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%m/%d/%Y")


def get_next_date(day=1):
    # Add one day
    tomorrow = date.today() + timedelta(days=day)
    return '%02d' % tomorrow.month + "/" + '%02d' % tomorrow.day + "/" + '%04d' % tomorrow.year


def today_in_slot():
    """Use for create slot"""
    now = datetime.datetime.now()
    return now.strftime("%m/%d")


def next_day_in_slot(days=1):
    """Use for create slot"""
    now = datetime.datetime.now() + timedelta(days=days)
    return now.strftime("%m/%d")

def calculate_age(birth):
    born = datetime.datetime.strptime(birth, '%Y-%m-%d')
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))

# starting time = current + start, and shift to 00, 15,30, 45
# ending time = starting time + duration
def getTimeSlot(start, duration):
    nextDate = 0
    now = datetime.datetime.now() + datetime.timedelta(minutes=start)
    offset = (int(now.minute / 15) + 1) * 15 - int(now.minute)
    startingTime = now + datetime.timedelta(minutes=offset)
    endingTime = startingTime + datetime.timedelta(minutes=duration)
    # Thang: In case starttime and endtime are not in same day
    if endingTime.day - datetime.datetime.now().day != 0:
        nextDate = endingTime.day - datetime.datetime.now().day
        startingTime = now.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1)
        endingTime = startingTime + datetime.timedelta(minutes=duration)
        if nextDate < 0:  # Case last day of the month
            nextDate = 1
    return get_next_date(day=nextDate), timeString(startingTime), timeString(endingTime)


def get_weekday(st):
    wd = st.weekday()
    return str((wd + 1) % 7 + 1)


def timeString(dt):
    return dt.strftime("%I:%M %p")


def getDateString(day=1):
    # add day
    day = date.today() + timedelta(days=day)
    # return strtime with format %a, %m/%d
    # i.e: Tue, May 03
    return day.strftime("%a, %m/%d")


# Thang: Add hour to current time with format 11:00 PM
def addTimeHour(timeStr, addHour=1):
    time = datetime.datetime.strptime(timeStr, "%I:%M %p") + timedelta(hours=addHour)
    return time.strftime("%I:%M %p")


# Thang: Return datetime with format YYYY/mm/DD
def getYMD(day=1):
    # add day
    day = date.today() + timedelta(days=day)
    return day.strftime("%Y/%m/%d")


# Thang: retun startTime, endTime, isToday,slotDate, allSlot
# startTime is next rounded hour i.e 7:00
# endTime = startTime + duration
def getNextHourSlotTime(duration=15):
    # get current time
    now = datetime.datetime.now()

    # get start time
    startingTime = now.replace(minute=15, second=0, microsecond=0) + timedelta(hours=1)
    endingTime = startingTime + datetime.timedelta(minutes=duration)
    # if start time and end time are not same day
    if startingTime.day - endingTime.day == -1:
        startingTime = startingTime + datetime.timedelta(hours=1)
        endingTime = endingTime + datetime.timedelta(hours=1)
    # Date of creation slot
    slotDate = endingTime.strftime("%m/%d/%Y")
    return timeString(startingTime), timeString(endingTime), slotDate


# Thang: Return timeblock i.e: morning, afternoon, evening
# return value 0, 1, 2 equal to morning, afternoon, evening
def getTimeBlock(strTime):
    slotTime = datetime.datetime.strptime(strTime, "%I:%M %p")
    print slotTime
    if slotTime >= datetime.datetime.strptime("12:00 AM", "%I:%M %p") and slotTime < datetime.datetime.strptime(
            "12:00 PM", "%I:%M %p"):
        return 0
    elif slotTime >= datetime.datetime.strptime("12:00 PM", "%I:%M %p") and slotTime < datetime.datetime.strptime(
            "06:00 PM", "%I:%M %p"):
        return 1
    elif slotTime >= datetime.datetime.strptime("06:00 PM", "%I:%M %p") and slotTime <= datetime.datetime.strptime(
            "11:59 PM", "%I:%M %p"):
        return 2


# Thang: Return time format match with appointment time on sessions
# Param: toDate=0  means today
# timeString w/ format %I:%M %p
# returns: %m/%d/%Y %I:%M %p
def getSessionDate(string, toDate=0, forEmail=False):
    #     string = datetime.datetime.strptime(string, "%I:%M %p").strftime("%H:%M") # Conver string from 12 hour to 24 hour
    dateTime = date.today() + timedelta(days=toDate)  # add days
    if forEmail:
        dateTime = string + " " + dateTime.strftime("on %a, %b %d %Y")
    else:
        dateTime = dateTime.strftime("%m/%d/%Y") + " " + string  # string format %I:%M %p
    return dateTime


# Thang: Check if a session datetime is arround x mins before current time
# Param: string w/ format %m/%d/%Y %I:%M %p and in the past
# Return boolean
def isDateTimeInThePast(string, duration=10):
    dateTime = datetime.datetime.strptime(string, "%m/%d/%Y %I:%M %p")
    currentTime = datetime.datetime.now()
    if divmod((currentTime - dateTime).total_seconds(), 60)[0] > duration:
        return False
    return True


# Thang: this function will pick a random available slot and return list of available slots after picking
def pickSlotTime(slotList, slotRange):
    aftSlotList = []
    # Random a slot time from the list
    ranIndex = randint(0, len(slotList) - 1)  # random index from the list

    # Convert time
    ranTime = datetime.datetime.strptime(slotList[ranIndex], "%I:%M %p")
    for i in slotList:
        slotTime = datetime.datetime.strptime(i, "%I:%M %p")
        if abs((ranTime - slotTime).total_seconds() / 60) >= slotRange:
            aftSlotList.append(i)
    return slotList[ranIndex], aftSlotList

def getNextDate(day = 1):
    # Add one day
    tomorrow = date.today() + timedelta(days=day)
    # Return next date in as custom string
    # Thang: Change that return month in 2 digits that fit with calendar
    return '%02d' % tomorrow.month + "/" + str(tomorrow.day) + "/" + str(tomorrow.year)

# Thang: To return all possible slots from startTime to endTime
def returnSlotList(startTime, endTime, slotRange):
    timeRange = 5  # Range shows on patient's appointment table, 5 mins now

    slotList = []
    start = datetime.datetime.strptime(startTime, "%I:%M %p")
    end = datetime.datetime.strptime(endTime, "%I:%M %p")

    lastSlotTime = end - datetime.timedelta(minutes=slotRange)
    if lastSlotTime >= start:
        numOfSlot = int((lastSlotTime - start).total_seconds() / (timeRange * 60))
        for i in range(numOfSlot + 1):
            slotTime = start + datetime.timedelta(minutes=(i * timeRange))
            slotList.append(timeString(slotTime))
    return slotList
