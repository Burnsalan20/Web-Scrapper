import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SHEETS_READ_WRITE_SCOPE = 'https://www.googleapis.com/auth/spreadsheets'
SCOPES = [SHEETS_READ_WRITE_SCOPE]


def main():
    spreadsheet_id = '1avy4rjsrkub1bpRlgeNGyQ9aCsqkSwV002T0yiKe4jg'  # this is part of the url of google
    rows = [
        ["", "", ""],
        [""],
        [""]
    ]

    # -----------

    credentials = get_or_create_credentials(scopes=SCOPES)  # or use GoogleCredentials.get_application_default()
    service = build('sheets', 'v4', credentials=credentials)
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="Sheet1!A:Z",
        body={
            "majorDimension": "ROWS",
            "values": rows
        },
        valueInputOption="USER_ENTERED"
    ).execute()


# Source: https://developers.google.com/sheets/api/quickstart/python
def get_or_create_credentials(scopes):
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
            credentials = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)
    return credentials


if __name__ == '__main__':
    main()