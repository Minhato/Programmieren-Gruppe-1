import datetime
from pprint import pprint
import sys
from oauth2client import client
from googleapiclient import sample_tools
import GoogleAPIConnection as gac
  
def setKalender(kalenderName):
  """Zum erstellen eines neuen Kalender (Minh)"""
  gac.googleConnection()
  calendar = {
    'summary': kalenderName,
    'timeZone': 'Europe/Berlin' 
    }
  created_calendar = gac.service.calendars().insert(body=calendar).execute()
  print (created_calendar['id'])

def deleteKalender(kalender):
  """Zum löschen eines erstellten Kalender (Minh)  """
  id = gac.getId(kalender)
  gac.service.calendars().delete(calendarId= id).execute()

def terminAnlegen(jahr, monat, tag, startStunde, startMinute, endStunde, endMinute, summary, description):
    """ Zum Anlegen eines neuen Termin (Minh) """
    startZeit = str(datetime.datetime(jahr, monat, tag, startStunde, startMinute)).replace(" ","T")
    endZeit = str(datetime.datetime(jahr,monat,tag,endStunde,endMinute)).replace(" ","T")
    event = {
    'summary': summary,
    #'location': '800 Howard St., San Francisco, CA 94103',
    'description': description,
    'start': {
    'dateTime': startZeit,
    'timeZone': 'Europe/Berlin',
  },
    'end': {
    'dateTime': endZeit,
    'timeZone': 'Europe/Berlin',
  },
#     'recurrence': [
#     'RRULE:FREQ=DAILY;COUNT=2'
#   ],
    'attendees': [
  ],
    'reminders': {
    'useDefault': False,
    'overrides': [
      {'method': 'email', 'minutes': 24 * 60},
      {'method': 'popup', 'minutes': 10},
    ],
  },
}
    id = goc.getId("TestKalender")
    event = goc.service.events().insert(calendarId=id, body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))


def terminanzeigen(jahr, monat, tag,):
  """Zum anzeigen aller Termine an dem jeweiligen Tag (Minh) """
  events = goc.service.events().list(calendarId= goc.getId('TestKalender')).execute()
  datum = str(datetime.date(jahr,monat,tag))
  print("Die Termine für den", datum, ":")
  for event in events['items']:
     if datum in event.get('start')['dateTime']: 
      print( event.get('summary')+ " um " + event.get('start')['dateTime'])
  

def terminBearbeiten():
  pass
def terminloeschen():
  pass

#deleteKalender("jaEndlich")