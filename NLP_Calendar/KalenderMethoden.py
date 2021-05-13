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
    id = gac.getId("TestKalender")
    event = gac.service.events().insert(calendarId=id, body=event).execute()
    print ('Event created: %s' % (event.get('htmlLink')))


def terminanzeigen(jahr, monat, tag,):
  """Zum anzeigen aller Termine an dem jeweiligen Tag (Minh) """
  events = gac.service.events().list(calendarId= gac.getId('TestKalender')).execute()
  datum = str(datetime.date(jahr,monat,tag))
  print(events['items'][0]['id'])
  print("__________")
  print("Die Termine für den", datum, ":")
  for event in events['items']:
     if datum in event.get('start')['dateTime']: 
      print( event.get('summary')+ " um " + event.get('start')['dateTime'])
  
terminanzeigen(2021,5,13)
def terminBearbeiten():
  pass
def terminloeschen(jahr,monat,tag,startStunde,startMinute):
  """Zum löschen eines Termin anhand des Datum und AnfangZeitpunkt (Minh) """
  events = gac.service.events().list(calendarId= gac.getId('TestKalender')).execute()
  print("die events", events['items'][4]['id'])
  startZeit = str(datetime.datetime(jahr, monat, tag, startStunde, startMinute)).replace(" ","T")
  print(startZeit)
  for event in events['items']:
    print(event['start'])
    if startZeit in event.get('start')['dateTime']:
      terminId = event.get('id')
      print("TerminID: ",terminId)
      gac.service.events().delete(calendarId= gac.getId('TestKalender'), eventId= terminId).execute()
      print("Termin wurde gelöscht!")
    else: 
      print("Etwas ist schief gelaufen, Termin nicht vorhanden/gefunden")
      break

#terminAnlegen(2021,5,14,16,0,18,0,'es geht','ez')
terminloeschen(2021,5,14,16,0)


#deleteKalender("jaEndlich")