import sys

from oauth2client import client
from googleapiclient import sample_tools


def main(argv):
    # Authenticate and construct service.
    service, flags = sample_tools.init(
        argv, 'calendar', 'v3', __doc__, __file__,
        scope=['https://www.googleapis.com/auth/calendar'])

    try:
        page_token = None
        while True:
            calendar_list = service.calendarList().list(
                pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(calendar_list_entry['summary'])
            page_token = calendar_list.get('nextPageToken')
            #test zum erstellen eines neuen Kalender
            #calendar = { 'summary': 'KalenderTest1','timeZone': 'America/Los_Angeles'}
            #created_calendar = service.calendars().insert(body=calendar).execute()
            #print(created_calendar['id'])

            # request_body = { 'summary': 'JetztKlapptEs'}
            # respone = service.calendars().insert(body= request_body).execute()
            # print(respone)

            service.calendars().delete(calendarId = 'edbj45b2jmpcqm8fksj3tf7lls@group.calendar.google.com' ).execute()
            if not page_token:
                break




    except client.AccessTokenRefreshError:
        print('The credentials have been revoked or expired, please re-run'
              'the application to re-authorize.')

if __name__ == '__main__':
    main(sys.argv)