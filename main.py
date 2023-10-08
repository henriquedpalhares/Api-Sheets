from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/spreadsheeets"]

SPREADSHEET_ID = "1nJxTKRuQQFKCuoFTfx4fExLIM6XIlKxISnbGrIP9zY4"

def main():
    creds  = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json","w") as token:
            token.write(creds.to_json())
    
    try:
        service = build("sheets","v4", credentials=creds)
        sheets = service.spreadsheets()
         
        result = sheets.values().get(SPREADSHEET_ID=SPREADSHEET_ID, range="Sheet1!A1:C6").execute()
        
        values = result.get("values",[])

        for row in values:
            print(values)

    except HttpError as err:
        print(err)

if __name__ == "__main__":
    main()