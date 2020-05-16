from datetime import datetime, timedelta
import pickle
from googleapiclient.discovery import build
from flask import session
from dateutil.tz import tzlocal


class CalendarUtil:
    def __init__(self, google_crendetial):
        self.creds = google_crendetial

    @property
    def service(self):
        return build("calendar", "v3", credentials=self.creds)

    def getSummary(self, booking):
        return f"CSS Booking #{booking['booking_id']} Car #{booking['car_id']}"

    def _addEvent(self, summary, desc, start: datetime, end: datetime) -> dict:
        '''
        :returns: an event object as detailed here: https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html#insert
        :rtype: dict
        '''
        start = start.astimezone(tzlocal())
        end = end.astimezone(tzlocal())
        event = self.service.events().insert(calendarId="primary", body={
            "summary": summary, "description": desc, "start": {"dateTime": start.isoformat()},
            "end": {"dateTime": end.isoformat()}
        }).execute()
        return event

    def addEvent(self, booking) -> dict:
        return self._addEvent(
            self.getSummary(booking),
            f"You have a car booking at Car Share System. Booking ID: {booking['booking_id']}; Car ID: {booking['car_id']}.",
            datetime.fromisoformat(f"{booking['date_booking']}T{booking['time_booking']}"),
            datetime.fromisoformat(f"{booking['date_return']}T{booking['time_return']}")
        )

    def _findEvent(self, booking):
        real_start_datetime = datetime(
            *([int(s) for s in booking['date_booking'].split('-') + booking['time_booking'].split(":")])
        ).astimezone(tzlocal())
        real_end_datetime = datetime(
            *([int(s) for s in booking['date_return'].split('-') + booking['time_return'].split(":")])
        ).astimezone(tzlocal())
        term = self.getSummary(booking)
        result = self.service.events().list(calendarId="primary", q=term).execute()
        for event in result.get("items", []):
            # if start date & end date are the same, return event id
            if datetime.fromisoformat(event["start"]["dateTime"]) == real_start_datetime \
                    and datetime.fromisoformat(event["end"]["dateTime"]) == real_end_datetime:
                return event
        return None

    def deleteEvent(self, booking) -> bool:
        event = self._findEvent(booking)
        if event is None:
            return False
        self.service.events().delete(calendarId="primary", eventId=event["id"]).execute()
        return True


class GAuthUtil:
    def getCredential(self):
        if "tokenByte" not in session:
            return None
        cred_b = session["tokenByte"]
        cred = pickle.loads(cred_b)
        return cred

    def setCredential(self, cred):
        session["tokenByte"] = pickle.dumps(cred)