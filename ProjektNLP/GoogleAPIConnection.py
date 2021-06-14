#Google API Connection
import datetime
#from pprint import pprint
import sys
from oauth2client import client
from googleapiclient import sample_tools

# die Variable service und googleConnection wurde aus der Example Python aus der offiziellen Google API kopiert, da bei unser service es zu technischen Komplikationen kam
# die Token haben sich bei uns nicht erneuert und waren statisch. D.h nur ein vorher gespeicherter Token konnte genutzt werden
# Da wir auf keine Lösung kamen, entschieden wir uns hier ein bisschen den Code abzuschauen
# Alles andere während des Projektes ist zu 100% von uns selber.
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

def getEventId(jahr, monat, tag, stunde, minute):

    events = service.events().list(calendarId= getId('TestKalender')).execute()
    startZeit = str(datetime.datetime(jahr, monat, tag, stunde, minute)).replace(" ","T")
    print(startZeit)
    for event in events['items']:
        print(event['summary'])
        print(event['start']['dateTime'])
        if startZeit in  event['start']['dateTime']:
            eventID= event['id']
    return eventID
#getId('jaEndlich')
#print("event ID",getEventId(2021,5,13,13,30))
googleConnection()
#sdölkfgölsfd
