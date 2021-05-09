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


def terminAnlegen():
  pass

def terminAnzeigen():
  pass

def terminBearbeiten():
  pass
def terminloeschen():
  pass

#deleteKalender("jaEndlich")