from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime

# 1. Authenticate
SCOPES = ["https://www.googleapis.com/auth/calendar"]
SERVICE_ACCOUNT_FILE = "calender-service.json"   # path to your JSON

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("calendar", "v3", credentials=credentials)

# 2. Prepare event
now = datetime.datetime.now()
event = {
    "summary": "🔔 Test Reminder from jamal",
    "description": "This is a test event created by API",
    "start": {
        "dateTime": (now + datetime.timedelta(minutes=2)).isoformat(),
        "timeZone": "Asia/Kolkata",
    },
    "end": {
        "dateTime": (now + datetime.timedelta(minutes=32)).isoformat(),
        "timeZone": "Asia/Kolkata",
    },
}

# 3. Insert into calendar
event_result = service.events().insert(
    calendarId="abhijith251324@gmail.com", body=event
).execute()

print("✅ Event created:", event_result["htmlLink"])
