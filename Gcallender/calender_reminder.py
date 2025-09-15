from google.oauth2 import service_account
from googleapiclient.discovery import build
import datetime
import streamlit as st
SERVICE_ACCOUNT = st.secrets["gcp"]
SCOPES = ["https://www.googleapis.com/auth/calendar"]

credentials = service_account.Credentials.from_service_account_info(
    dict(SERVICE_ACCOUNT), scopes=SCOPES
)

service = build("calendar", "v3", credentials=credentials)

def shedule_reminders(task_name: str, intervals: list[int]) -> list[str]:
    scheduled_dates = []
    now = datetime.datetime.now()

    for days in intervals:
        reminder_date = now + datetime.timedelta(days=days)
        event = {
            "summary": f"Review: {task_name}",
            "start": {"dateTime": reminder_date.isoformat(), "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": (reminder_date + datetime.timedelta(hours=1)).isoformat(),
                    "timeZone": "Asia/Kolkata"},
        }

        service.events().insert(
            calendarId="abhijith251324@gmail.com", body=event
        ).execute()

        scheduled_dates.append(reminder_date.strftime("%Y-%m-%d %H:%M"))

    return scheduled_dates
