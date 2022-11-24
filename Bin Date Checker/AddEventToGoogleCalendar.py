import datetime
import os.path
import requests
import bs4
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Convert date function
def ConvertDate(date):
    date = date.replace("st","")
    date = date.replace("nd","")
    date = date.replace("rd","")
    date = date.replace("th","")
    date = datetime.datetime.strptime(date, '%A %d %b %Y')
    return date

# Add event to Google Calendar function
SCOPES = ['https://www.googleapis.com/auth/calendar']

def AddEvent(start,end,summary):
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'Creds.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'start': {
                'dateTime': start,
                'timeZone': 'Europe/London',
            },
        'end': {
        'dateTime': end,
        'timeZone': 'Europe/London',
        },
        'attendees': [
        {'email': '@gmail.com'},
        ],
        }
    event = service.events().insert(calendarId='primary', body=event).execute()

# Check Bin Dates and add to Google Calendar using AddEvent() function
r = requests.get("https://www.hull.gov.uk/bins-and-recycling/bin-collections/bin-collection-day-checker/checker/view/10093952819")
soup = bs4.BeautifulSoup(r.text, features="html.parser")

blackbin = soup.find(class_="region region-content")
div = blackbin.find_parent('div')
span = div.find_all('span')
spantext = str(span[1]).split(">")
date = spantext[1].split("<")
blackbindate = date[0]
blackbindate = ConvertDate(blackbindate)
start = blackbindate.strftime("%Y-%m-%d") + "T09:00:00"
end = blackbindate.strftime("%Y-%m-%d") + "T17:00:00"
summary = "Black Bin Collection"
AddEvent(start,end,summary)

bluebrown = soup.find_all(style="color:blue;font-weight:800")
bluebrownbin = str(bluebrown[1]).split(">")
bluebrownbincollection = bluebrownbin[1].split("<")
bluebrownbindate = bluebrownbincollection[0]
bluebrownbindate = ConvertDate(bluebrownbindate)
start = bluebrownbindate.strftime("%Y-%m-%d") + "T09:00:00"
end = bluebrownbindate.strftime("%Y-%m-%d") + "T17:00:00"
summary = "Blue & Brown Bin Collection"
AddEvent(start,end,summary)
