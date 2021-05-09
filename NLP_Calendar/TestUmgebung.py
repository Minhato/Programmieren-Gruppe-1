import GoogleAPIConnection as goc

def terminAnlegen():
    """ Zum Anlegen eines neuen Termin (Minh) """
    event = {
    'summary': 'Was ist los',
    'location': '800 Howard St., San Francisco, CA 94103',
    'description': 'A chance to hear more about Google\'s developer products.',
    'start': {
    'dateTime': '2021-05-09T21:00:00',
    'timeZone': 'Europe/Berlin',
  },
    'end': {
    'dateTime': '2021-05-09T22:00:00',
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
#TO:DO parameter 
terminAnlegen()
