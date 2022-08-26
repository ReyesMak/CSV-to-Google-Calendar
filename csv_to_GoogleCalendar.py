from datetime import datetime
import pandas as pd
import os
import pickle
import datetime
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import random
import string

# create api service function


def create_service(client_secret_file, api_name, api_version, *scopes, prefix=''):
    CLIENT_SECRET_FILE = client_secret_file
    API_SERVICE_NAME = api_name
    API_VERSION = api_version
    SCOPES = [scope for scope in scopes[0]]
    cred = None
    working_dir = os.getcwd()
    token_dir = 'token files'
    pickle_file = f'token_{API_SERVICE_NAME}_{API_VERSION}{prefix}.pickle'

    # check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))
    if os.path.exists(os.path.join(working_dir, token_dir, pickle_file)):
        with open(os.path.join(working_dir, token_dir, pickle_file), 'rb') as token:
            cred = pickle.load(token)

    if not cred or not cred.valid:
        if cred and cred.expired and cred.refresh_token:
            cred.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE, SCOPES)
            cred = flow.run_local_server()

        with open(os.path.join(working_dir, token_dir, pickle_file), 'wb') as token:
            pickle.dump(cred, token)
    try:
        service = build(API_SERVICE_NAME, API_VERSION, credentials=cred)
        print(API_SERVICE_NAME, API_VERSION, 'service created successfully')
        return service
    except Exception as e:
        print(e)
        print(f'Failed to create service instance for {API_SERVICE_NAME}')
        os.remove(os.path.join(working_dir, token_dir, pickle_file))
        return None


# convert datetime function
def convert_to_RFC_datetime(start_year=1900, start_month=1, start_day=1, hour=0, minute=0):
    dt = datetime.datetime(start_year, start_month,
                           start_day, hour, minute, 0).isoformat()+"Z"
    return dt


# launch api
CLIENT_SECRET_FILE = "client_secret.json"
API_NAME = 'calendar'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/calendar']

service = create_service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)


# list calendars
calendar_list = service.calendarList().list(pageToken=None).execute()


# delete already existing calendar
# for calendar_list_entry in calendar_list['items']:
#     if 'CALENDAR_NAME' in calendar_list_entry['summary']:          #CALENDAR_NAME is the name of the calendar in the account
#         id = calendar_list_entry['id']
#         service.calendars().delete(calendarId=id).execute()


# list calendars
calendar_list = service.calendarList().list(pageToken=None).execute()

# calendarId of the calendar
# Replace with the specific calendarId
# Current id is for [CWB] Summer 22 Boot Camp
id = "preface.education_9me0qsqf7qepo2gq6tama7ujls@group.calendar.google.com"


# format attendees' emails
def create_guests(email):
    return {
        'email': email,
        'optional': False,
        'responsiveStatus': False
    }


# insert events to google calendar function
def insert_events(color):
    letters = string.ascii_letters

    # validate if it is an all-day event or not

    def is_all_day_event(i):
        if ("FALSE" or "False" or "false") in all_day_event[i]:
            return False
        else:
            return True
    x = 0
    for i in range(len(wb)):
        if is_all_day_event(i):
            all_day_event_true_start.append(
                "{}-{}-{}".format(start_year[i], start_month[i], start_day[i]))
            all_day_event_true_end.append(
                "{}-{}-{}".format(end_year[i], end_month[i], end_day[i]))
            event_request_body = {
                'start': {
                    'date': all_day_event_true_start[x],
                },
                'end': {
                    'date': all_day_event_true_end[x],
                },
                'summary': courseName[i],
                'description': description[i],
                'location': location[i],
                'colorId': color,
                'visibility': is_private[i],
                'attendees': [create_guests(k) for k in guest[i]],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 10},
                    ]
                },
                "conferenceData": {  # Google Meet conference link automatically generated
                    "createRequest": {
                        # Generate random string for requestID
                        "requestId": "".join(random.choice(letters) for i in range(10)),
                        "conferenceSolutionKey": {"type": "hangoutsMeet"}
                    }
                },
            }
            print({courseName[i]: event_request_body["conferenceData"]
                  ["createRequest"]["requestId"]})
            service.events().insert(calendarId=id, body=event_request_body,
                                    conferenceDataVersion=1).execute()
            x += 1

        else:
            adjust_timezone = +8  # (HK time UTC+8)
            finalised_start_hour = 24 + int(fstart_hour[i]) - adjust_timezone if (int(
                fstart_hour[i]) - adjust_timezone) < 0 else int(fstart_hour[i]) - adjust_timezone
            finalised_end_hour = 24 + int(fend_hour[i]) - adjust_timezone if (
                int(fend_hour[i]) - adjust_timezone) < 0 else int(fend_hour[i]) - adjust_timezone
            finalised_start_day = int(
                start_day[i]) - 1 if (int(fstart_hour[i]) - adjust_timezone) < 0 else int(start_day[i])
            finalised_end_day = int(
                end_day[i]) - 1 if (int(fend_hour[i]) - adjust_timezone) < 0 else int(end_day[i])
            finalised_start_minute = int(fstart_min[i])
            finalised_end_minute = int(fend_min[i])
            event_request_body = {
                'start': {
                    'dateTime': convert_to_RFC_datetime(int(start_year[i]), int(start_month[i]), finalised_start_day, finalised_start_hour, finalised_start_minute),
                },
                'end': {
                    'dateTime': convert_to_RFC_datetime(int(end_year[i]), int(end_month[i]), finalised_end_day, finalised_end_hour, finalised_end_minute),
                },
                'summary': courseName[i],
                'description': description[i],
                'location': location[i],
                'colorId': color,
                'visibility': is_private[i],
                'attendees': [create_guests(k) for k in guest[i]],
                'reminders': {
                    'useDefault': False,
                    'overrides': [
                        {'method': 'email', 'minutes': 10},
                    ]
                },
                "conferenceData": {  # Google Meet conference link automatically generated
                    "createRequest": {
                        # Generate random string for requestID
                        "requestId": "".join(random.choice(letters) for i in range(10)),
                        "conferenceSolutionKey": {"type": "hangoutsMeet"},
                    },
                },
            }
            print({courseName[i]: event_request_body["conferenceData"]
                  ["createRequest"]["requestId"]})
            service.events().insert(calendarId=id, body=event_request_body,
                                    conferenceDataVersion=1).execute()


all_day_event_true_start = []
all_day_event_true_end = []


# convert csv file to excel and export to Excel for recording purposes
wb = pd.read_csv('csv_file.csv')

# copy course name
courseName = []
for i in range(len(wb)):
    courseName.append(wb.iloc[i]["Course Name"])


# FORMATTING START DATE
# copy start date
start_date = []
for i in range(len(wb)):
    start_date.append(wb.iloc[i]["Start Date"])

# append lists
start_month = []
start_day = []
start_year = []

# format start month, day & year
for i in range(len(wb)):
    start_month.append(start_date[i])
    start_day.append(start_date[i])
    start_year.append(start_date[i])

start_month = [x[:-6] for x in start_month]
start_day = [x[3:-3] for x in start_day]
start_year = ['20' + x[6:] for x in start_year]


# FORMATTING START TIME
# copy start time
start_time = []
for i in range(len(wb)):
    start_time.append(wb.iloc[i]["Start Time"])

# format start hour
fstart_hour = []
for i in range(len(start_time)):
    fstart_hour.append(start_time[i])
fstart_hour = [x[:-3] for x in fstart_hour]

# format start minutes
fstart_min = []
for i in range(len(start_time)):
    fstart_min.append(start_time[i])
fstart_min = [x[3:5] for x in fstart_min]


# FORMATTING END DATE
# copy end date
end_date = []
for i in range(len(wb)):
    end_date.append(wb.iloc[i]["End Date"])


# append lists
end_month = []
end_day = []
end_year = []

# format end month, day & year
for i in range(len(wb)):
    end_month.append(end_date[i])
    end_day.append(end_date[i])
    end_year.append(end_date[i])

end_month = [x[:-6] for x in end_month]
end_day = [x[3:-3] for x in end_day]
end_year = ['20' + x[6:] for x in end_year]


# FORMATTING END TIME
# copy end time
end_time = []
for i in range(len(wb)):
    end_time.append(wb.iloc[i]["End Time"])

# format end time
fend_hour = []
for i in range(len(end_time)):
    fend_hour.append(end_time[i])
fend_hour = [x[:-3] for x in fend_hour]

# format end minute
fend_min = []
for i in range(len(end_time)):
    fend_min.append(end_time[i])
fend_min = [x[3:5] for x in fend_min]


# copy all-day event
all_day_event = []
for i in range(len(wb)):
    all_day_event.append(wb.iloc[i]["All Day Event"])


for i in range(len(all_day_event)):
    all_day_event[i] = str(all_day_event[i]).upper()


# copy description
description = []
for i in range(len(wb)):
    description.append(wb.iloc[i]["Description"])


# copy location
location = []
for i in range(len(wb)):
    location.append(wb.iloc[i]["Location"])


# copy private
is_private = []
for i in range(len(wb)):
    is_private.append(wb.iloc[i]["Private"])

# FORMATTING email address
# copy guest email address
guest = []
for i in range(len(wb)):
    emailAddress = wb.iloc[i]["Guests"].split(",")
    guest.append(emailAddress)

# adapt private to fit jsonxf
for i in range(len(is_private)):
    is_private[i] = str(is_private[i]).upper()
    if ("TRUE" or "True" or "true") in is_private[i]:
        is_private[i] = "private"
    else:
        is_private[i] = "default"


# insert events(color) ---> check available colors here => https://lukeboyle.com/blog/posts/google-calendar-api-color-id
insert_events(7)
