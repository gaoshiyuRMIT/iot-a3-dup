import os
from datetime import datetime, timedelta
import pickle
from googleapiclient.discovery import build
from flask import session, current_app
from dateutil.tz import tzlocal
import cv2
import face_recognition
from tkinter import Tk, filedialog
import os
import imutils
import pathlib
from PIL import Image
import numpy as np

class CalendarUtil:
    def __init__(self, google_crendetial):
        '''initializes with a google API credential object
        '''
        self.creds = google_crendetial

    @property
    def service(self):
        '''builds the google calendar service
        '''
        return build("calendar", "v3", credentials=self.creds)

    def getSummary(self, booking):
        '''generate event summary from a booking

        :param dict booking: a dictionary representing the booking
        :return: event summary of this booking
        :rtype: str
        '''
        return f"CSS Booking #{booking['booking_id']} Car #{booking['car_id']}"

    def _addEvent(self, summary, desc, start: datetime, end: datetime) -> dict:
        '''
        add an event to google calendar with supplied parameters

        :param str summary: summary of the event
        :param str desc: description of the event
        :param datetime start: start date & time of the event
        :param datetime end: end date & time of this event
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
        '''create a calendar event based on this booking

        :param dict booking: a dictionary representing a booking
        :return: an event object, with format as detailed here https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html#insert
        :rtype: dict
        '''
        return self._addEvent(
            self.getSummary(booking),
            f"You have a car booking at Car Share System. Booking ID: {booking['booking_id']}; Car ID: {booking['car_id']}.",
            datetime.fromisoformat(f"{booking['date_booking']}T{booking['time_booking']}"),
            datetime.fromisoformat(f"{booking['date_return']}T{booking['time_return']}")
        )

    def _findEvent(self, booking):
        '''find the event created when the provided booking was created

        :param dict booking: a dictionary representing the booking
        :return: a dictionary representing the event, as detailed here https://developers.google.com/resources/api-libraries/documentation/calendar/v3/python/latest/calendar_v3.events.html#insert
        :rtype: dict
        '''
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
        '''delete an event given a booking dictionary

        :param dict booking: a dictionary representing a booking
        :return: whether an event is deleted
        :rtype: bool
        '''
        event = self._findEvent(booking)
        if event is None:
            return False
        self.service.events().delete(calendarId="primary", eventId=event["id"]).execute()
        return True


class GAuthUtil:
    def getCredential(self):
        '''get google API credential object from session if user is signed in,
        otherwise returns None
        '''
        if "tokenByte" not in session:
            return None
        cred_b = session["tokenByte"]
        cred = pickle.loads(cred_b)
        return cred

    def setCredential(self, cred):
        '''store google API credential object in session
        '''
        session["tokenByte"] = pickle.dumps(cred)

class PhotoUtil:
    def __init__(self):
        self.rootdir = current_app.config["PHOTO_FOLDER"]

    @staticmethod
    def getExt(filename):
        i = filename.rfind(".")
        return filename[i:]

    def storePhotos(self, files, username):
        folder = os.path.join(self.rootdir, username)
        if not os.path.isdir(folder):
            os.makedirs(folder)
        i = 1
        for f in files:
            ext = self.getExt(f.filename)
            f.save(os.path.join(folder, f"image{i}{ext}"))
            i += 1
        


class FaceEncodeUtil:
    HEIGHT = 640
    WIDTH = 480
    CASCADE = "haarcascade_frontalface_default.xml"
    CWD = str(pathlib.Path.cwd())
    IMAGEFOLDER = "./iot/admin-app/app/dataset/{}"
    ENCODEFOLDER = "./iot/admin-app/app/dataset/{}/encoding"
    ENCODEFILEPATH = CWD + "/iot/admin-app/app/dataset/{}/encoding/face_encoding.pickle"

    def __init__(self, username):
        self.name = username
        self.folder = IMAGEFOLDER.format(self.name)
        self.encode_folder = ENCODEFOLDER.format(self.name)
        self.encode_file_path = ENCODEFILEPATH.format(self.name)
        self.encodings = []


    def encode_user_images(self):
        #examine each saved image
        for path in pathlib.Path(self.folder).iterdir():
            if path.is_file():
                #establish filepath for current image
                image_path = CWD + "/" + str(path)
                # read image into opencv - returns numpy array
                bgr_img = cv2.imread(image_path)
                # convert from rgb to bgr
                img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
                
                # resize image (if necessary) to reduce computing time 
                height, width = img.shape[:2]
                if height > HEIGHT or width > WIDTH:
                    img = imutils.resize(img, width = WIDTH, height=HEIGHT)

                #convert image to grayscale for more effective face detection
                gray_image = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                # load the haar cascade for frontal face detection
                face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + CASCADE)
                # confirm there is a detectable face in image 
                # 'face' will contain the border locations of found face in order: top, right, bottom, left 
                face = face_detector.detectMultiScale(gray_image, 1.3, 5)
                if len(face) > 4 or len(face) == 0:
                    # photo has more then one face dected in it or no (recognisable) face 
                    # therefore reject photo (delete)
                    os.remove(image_path)
                else:
                    # find location of face
                    # NOTE: hog is faster then cnn, slightly less accurate 
                    # (boxes are not necessary to face_encoding function, but improves speed)
                    boxes = face_recognition.face_locations(img, model="hog") 
                    # encode face - returns 128 vetor numpy darray
                    one_encoding = face_recognition.face_encodings(img, boxes)
                    #add encoding to list
                    self.encodings.append(one_encoding)
        return len(self.encodings)
        
    

                
