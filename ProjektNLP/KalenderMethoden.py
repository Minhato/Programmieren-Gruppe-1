import datetime
from pprint import pprint
import sys
from oauth2client import client
from googleapiclient import sample_tools
import GoogleAPIConnection as gac

def kalenderAnlegen(kalenderName):
  """Zum erstellen eines neuen Kalender (Minh)"""
  gac.googleConnection()
  calendar = {
    'summary': kalenderName,
    'timeZone': 'Europe/Berlin' 
    }
  created_calendar = gac.service.calendars().insert(body=calendar).execute()
  print (created_calendar['id'])

def kalenderLoeschen(kalender):
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
  for event in events['items']:
     if datum in event.get('start')['dateTime']: 
      print( event.get('summary')+ " um " + event.get('start')['dateTime'])

def terminBearbeiten(jahr,monat,tag,stunde,minute,titel):
  """Zum Termin Bearbeiten  """
  event = gac.service.events().get(calendarId=gac.getId('TestKalender'), eventId=gac.getEventId(jahr,monat,tag,stunde,minute)).execute()
  event['summary'] = titel
  #print("dieZeit:"+ event['start']['dateTime'])
  #print("endzeit:"+ event['end']['dateTime'])
  updatedEvent = gac.service.events().update(calendarId = gac.getId('TestKalender'), eventId= event['id'], body = event).execute()

#print("datetimeeeee "+ datetime.datetime.now().astimezone().replace(microsecond=0).isoformat())
#terminBearbeiten(2021,6,2,19,0,"neue")


def terminBearbeiten(jahr,monat,tag,stunde,minute,neueStunde,neueMinute,endStunde,endMinute):
  """Zum Termin Bearbeiten nur mit neue Uhrzeit """
  event = gac.service.events().get(calendarId=gac.getId('TestKalender'), eventId=gac.getEventId(jahr,monat,tag,stunde,minute)).execute()
  event['start'] ['dateTime'] = datetime.datetime(jahr,monat,tag,neueStunde,neueMinute).astimezone().replace(microsecond=0).isoformat()
  event['end'] ['dateTime'] = datetime.datetime(jahr,monat,tag,endStunde,endMinute).astimezone().replace(microsecond=0).isoformat()
  #print(event['start']['dateTime'])
  updatedEvent = gac.service.events().update(calendarId = gac.getId('TestKalender'), eventId= event['id'], body = event).execute()

#terminBearbeiten(2021,6,2,22,0,21,0,21,30)

def terminBearbeiten(jahr,monat,tag,stunde,minute,neuJahr,neuMonat,neuTag,neueStunde,neueMinute,endStunde,endMinute):
  """Zum Termin Bearbeiten nur mit neuen Datum """
  event = gac.service.events().get(calendarId=gac.getId('TestKalender'), eventId=gac.getEventId(jahr,monat,tag,stunde,minute)).execute()
  event['start'] ['dateTime'] = datetime.datetime(neuJahr,neuMonat,neuTag,neueStunde,neueMinute).astimezone().replace(microsecond=0).isoformat()
  event['end'] ['dateTime'] = datetime.datetime(neuJahr,neuMonat,neuTag,endStunde,endMinute).astimezone().replace(microsecond=0).isoformat()
 # print(event['start']['dateTime'])
  updatedEvent = gac.service.events().update(calendarId = gac.getId('TestKalender'), eventId= event['id'], body = event).execute()

#terminBearbeiten(2021,6,2,21,0,2021,6,3,13,0,14,0)
def terminloeschen(jahr,monat,tag,startStunde,startMinute):
  """Zum löschen eines Termin anhand des Datum und AnfangZeitpunkt (Minh) """
  events = gac.service.events().list(calendarId= gac.getId('TestKalender')).execute()
  startZeit = str(datetime.datetime(jahr, monat, tag, startStunde, startMinute)).replace(" ","T")
 # print(startZeit)
  for event in events['items']:
   # print(event['summary'])
   # print(event['start']['dateTime'])
    if startZeit in  event['start']['dateTime']:
     eventID= event['id']
     print("ID gefunden")
     gac.service.events().delete(calendarId= gac.getId('TestKalender'), eventId= eventID).execute()

#setKalender('TestKalender')
#terminAnlegen(2021,6,8,18,00,20,0,"Daans Termin","Daan hat einen Termin in seinem Kalender")
#terminloeschen(2021,6,2,13,0)
#terminBearbeiten(2021,6,2,13,0, "anderer Titel")