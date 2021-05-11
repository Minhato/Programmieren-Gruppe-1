#Google API Connection
from pprint import pprint
import sys
from oauth2client import client
from googleapiclient import sample_tools


service, flags = sample_tools.init(sys.argv,'calendar', 'v3', __doc__, __file__, scope=['https://www.googleapis.com/auth/calendar'])
def googleConnection():
    """Zum Abfragen des Token und zurückgeben der Kalenderliste (Minh) """

    page_token = None
    while True:
        calendar_list = service.calendarList().list(pageToken=page_token).execute()
        for calendar_list_entry in calendar_list['items']:
            print (calendar_list_entry['id'], calendar_list_entry['summary'])
            page_token = calendar_list.get('nextPageToken')
        if not page_token:
            break

#googleConnection()
def getId(kalender):
    """Zum zurückgeben der ID durch Kalender Name (Minh) """
    page_token = None
    calendar_list = service.calendarList().list(pageToken=page_token).execute()
    for calendar_list_entry in calendar_list['items']:
       # print(calendar_list_entry['summary'] == kalender)
        if (calendar_list_entry['summary'] == kalender):
            print(calendar_list_entry.get('id'))
            return calendar_list_entry.get('id')

#getId('jaEndlich')

googleConnection()
#Kommentar:Minh ist der beste!
#sdölkfgölsfd
