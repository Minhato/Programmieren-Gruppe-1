import GoogleAPIConnection as goc
import datetime
def test(jahr, monat, tag, startStunde, startMinute):
   startZeit = str(datetime.datetime(jahr, monat, tag, startStunde, startMinute)).replace(" ","T")
   print("startzeit",startZeit)
test(2021,4,19,15,20)


terminAnlegen(2021,5,14,15,0,16,0,"nice","guter Test")
