import datetime
import GoogleAPIConnection as gac
gac.googleConnection()

#Alle Termine werden im TestKalender gespeichert, aus organisatorische Sicht, um schnell alle Termine löschen zu können.

def kalenderAnlegen(kalenderName):
  """Zum erstellen eines neuen Kalender (Minh)"""
  calendar = {
    'summary': kalenderName,
    'timeZone': 'Europe/Berlin' 
    }
  created_calendar = gac.service.calendars().insert(body=calendar).execute()
  return "Kalender wurde angelegt!"

def kalenderLoeschen(kalender):
  """Zum löschen eines erstellten Kalender (Minh)  """
  id = gac.getId(kalender)
  gac.service.calendars().delete(calendarId= id).execute()
  return "Kalender wurde gelöscht!"

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
    print ('Termin wurde erstellt: %s' % (event.get('htmlLink')))
    nachricht = "Termin erstellt"
    return nachricht

def terminanzeigen(jahr, monat, tag,):
  """Zum anzeigen aller Termine an dem jeweiligen Tag (Minh) """
  events = gac.service.events().list(calendarId= gac.getId('TestKalender')).execute()
  datum = str(datetime.date(jahr,monat,tag))
  listeDerEvents = []
  listeAlsString = ""
  for event in events['items']:
    if datum in event.get('start')['dateTime']:
      variable = event.get('start')['dateTime']
      listeDerEvents.append( event.get('summary')+ " am " + str(datetime.datetime.strptime(variable,("%Y-%m-%d" "T" "%H:%M:%S" "%z")).strftime("%d.%m.%Y" " um " "%H:%M" "Uhr")))
      variable = datetime.datetime.strptime(variable,("%Y-%m-%d" "T" "%H:%M:%S" "%z")).strftime("%d.%m.%Y" "um" "%H:%M" "Uhr") #2021-06-15T03:00:00+02:00
  for werte in listeDerEvents:
    listeAlsString += str(werte) + "\n"
  if listeAlsString == "":
    return "es wurden keine Termine für den Tag gefunden! Glück gehabt"

  return listeAlsString

def terminTitelBearbeiten(jahr,monat,tag,stunde,minute,titel):
  """Zum Termin Bearbeiten  """
  event = gac.service.events().get(calendarId=gac.getId('TestKalender'), eventId=gac.getEventId(jahr,monat,tag,stunde,minute)).execute()
  event['summary'] = titel
  updatedEvent = gac.service.events().update(calendarId = gac.getId('TestKalender'), eventId= event['id'], body = event).execute()
  return "Titel vom Termin geändert"

def terminVerschiebenNeueUhrzeit(jahr,monat,tag,stunde,minute,neueStunde,neueMinute,endStunde,endMinute):
  """Zum Termin Bearbeiten nur mit neue Uhrzeit """
  event = gac.service.events().get(calendarId=gac.getId('TestKalender'), eventId=gac.getEventId(jahr,monat,tag,stunde,minute)).execute()
  event['start'] ['dateTime'] = datetime.datetime(jahr,monat,tag,neueStunde,neueMinute).astimezone().replace(microsecond=0).isoformat()
  event['end'] ['dateTime'] = datetime.datetime(jahr,monat,tag,endStunde,endMinute).astimezone().replace(microsecond=0).isoformat()
  updatedEvent = gac.service.events().update(calendarId = gac.getId('TestKalender'), eventId= event['id'], body = event).execute()
  return "Termin wurde um 2 Stunden verschoben"

def terminVerschieben(jahr,monat,tag,stunde,minute,neuJahr,neuMonat,neuTag,neueStunde,neueMinute,endStunde,endMinute):
  """Zum Termin Bearbeiten nur mit neuen Datum """
  event = gac.service.events().get(calendarId=gac.getId('TestKalender'), eventId=gac.getEventId(jahr,monat,tag,stunde,minute)).execute()
  event['start'] ['dateTime'] = datetime.datetime(neuJahr,neuMonat,neuTag,neueStunde,neueMinute).astimezone().replace(microsecond=0).isoformat()
  event['end'] ['dateTime'] = datetime.datetime(neuJahr,neuMonat,neuTag,endStunde,endMinute).astimezone().replace(microsecond=0).isoformat()
  updatedEvent = gac.service.events().update(calendarId = gac.getId('TestKalender'), eventId= event['id'], body = event).execute()

def terminloeschen(jahr,monat,tag,startStunde,startMinute):
  """Zum löschen eines Termin anhand des Datum und AnfangZeitpunkt (Minh) """
  events = gac.service.events().list(calendarId= gac.getId('TestKalender')).execute()
  startZeit = str(datetime.datetime(jahr, monat, tag, startStunde, startMinute)).replace(" ","T")
  for event in events['items']:
    if startZeit in  event['start']['dateTime']:
     eventID= event['id']
     gac.service.events().delete(calendarId= gac.getId('TestKalender'), eventId= eventID).execute()
  return "Termin wurde erfolgreich gelöscht"
  
