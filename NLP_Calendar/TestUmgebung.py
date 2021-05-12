import GoogleAPIConnection as goc
import datetime
def test(jahr, monat, tag, startStunde, startMinute):
   startZeit = datetime.datetime(jahr, monat, tag, startStunde, startMinute)
   print(startZeit)
test(2021,4,19,15,20)

def terminAnlegen(jahr, monat, tag, startStunde, startMinute, endStunde, endMinute, summary, description):
    """ Zum Anlegen eines neuen Termin (Minh) """
    startZeit = str(datetime.datetime(jahr, monat, tag, startStunde, startMinute))
    endZeit = str(datetime.datetime(jahr,monat,tag,))
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

terminAnlegen(2021,5,11,22,0,23,0,'test eintrag', 'hat ja gut funktioniert')