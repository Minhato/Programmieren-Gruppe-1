import GoogleAPIConnection as gac
import datetime
def test(jahr, monat, tag, startStunde, startMinute):
   startZeit = str(datetime.datetime(jahr, monat, tag, startStunde, startMinute)).replace(" ","T")
   print("startzeit",startZeit)

#Termin löschen funktioniert iwie nicht mehr, nur ein Eintrag wird angezeigt
def terminloeschen(jahr,monat,tag,startStunde,startMinute):
  """Zum löschen eines Termin anhand des Datum und AnfangZeitpunkt (Minh) """
  events = gac.service.events().list(calendarId= gac.getId('TestKalender')).execute()
  startZeit = str(datetime.datetime(jahr, monat, tag, startStunde, startMinute)).replace(" ","T")
  print(startZeit)
  for event in events['items']:
    print("Die Evente", event['start'])
    if startZeit in event.get('start')['dateTime']:
      terminId = event.get('id')
      print("TerminID: ",terminId)
      gac.service.events().delete(calendarId= gac.getId('TestKalender'), eventId= terminId).execute()
      print("Termin wurde gelöscht!")
    else: 
      print("Etwas ist schief gelaufen, Termin nicht vorhanden/gefunden")
      break

#terminAnlegen(2021,5,14,16,0,18,0,'es geht','ez')
#terminloeschen(2021,5,14,16,0)


testen(2021,5,14,15,00)

