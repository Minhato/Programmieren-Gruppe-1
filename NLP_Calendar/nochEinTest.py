print("hi")
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pickle
SCOPES = ['https://www.googleapis.com/auth/calendar']
"""
flow = InstalledAppFlow.from_client_secrets_file(
    'C:\\Program Files (x86)\\credentials.json', SCOPES) 

credentials = flow.run_console
credentials
"""
print(credentials)
   if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request6())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'C:\\Program Files (x86)\\credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
