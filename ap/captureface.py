import cv2
import face_recognition
import pickle
from tkinter import Tk, filedialog
import os
import imutils

# Acknowledgement
# This code is adapted from
# https://www.hacster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826


"""CaptureFace is a class that allows the user ot enter a phtoto of thier
face in order to allow user authentication via facial recognition. This
class only captures image data and then provides this data to the Master
Pi."""


class CaptureFace:
    HEIGHT = 640
    WIDTH = 480

    def __init__(self):
        self.image = None

    """retrieve_webcam_image allows the user to take a photo of thier face
    via webcam, sepcifically via picam for the raspberrypi. The correct
    drivers must be installed for this function to work, if PiCam available."""
    def retrieve_webcam_image(self):
        # ensure image attribute is empty 
        self.image = None
        try:
            # start the camera
            camera = cv2.VideoCapture(0)
            # set video width and height
            camera.set(3, 640)
            camera.set(4, 480)
            # load the haar cascade for frontal face detection
            face_detector = cv2.CascadeClassifier(
                            "haarcascade_frontalface_default.xml")
            print("PiCam is ready to take a photo...")
            morePhotos = True
            while morePhotos:
                key = input("Press 'p' to take a photo, or 'q' to quit")
                # Try taking a photo
                if key == "p":
                    ret, photo = camera.read()
                    gray_image = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
                    # test whether a face is detectable in photo
                    face = face_detector.detectMultiScale(
                        gray_image,               # grayscale image
                        scaleFactor=1.3,    # image reduction scale for each cascade test
                        minNeighbours=5,    # number of neighbours needed to be considered
                        minSize=(20, 20)    # minimum rectangle size to be considered a face
                    )
                    if (len(face) == 0):
                        print("face not deteced, try again")
                        continue
                    else:
                        print("Face detected!")
                        self.image = gray_image
                        morePhotos = False
                elif key == "q":
                    print("quitting PiCam ...")
                    morePhotos = False
                else:
                    print("you must enter 'p' or 'q'")
                    continue
        except Exception:
            print("Error using PiCam, try another method of logging in")
        finally:
            camera.release()
            # return image to be used for authentiaction (may be null)
            return self.image

    """retrieve_image_from_file allows the user to select an image from
    file and use this to try and authenticate themselves with system.
    If the haar cascade for fronal faces does not detect a face in the
    selected image the user will be prompted to try again."""
    def retrieve_image_from_file(self):
        self.image = None
        try:
            print("\n\n choose a JPG image of yourself:\n")
            Tk().withdraw()     # stops 'root' window appearing
            # open file dialog window - allow a .jpg file to be choosen
            filepath = filedialog.askopenfilename(filetypes=[("jpg files", "*.jpg")], initialdir=os.environ['HOME'], title="Choose a JPG image of yourself")
            print("filepath is " + str(filepath))
            image = cv2.imread(str(filepath))
            self.image = self.resize_image(image)
        except Exception as e:
            print(e.args)
        finally:
            return self.image

    """resize_image tests the original size of passed image and returns
    an image sized height = 640, width = 480, if original is larger then
    these dimensions. This function preserves aspect ratio."""
    def resize_image(self, image):
        if image is not None:
            try:
                height, width = image.shape[:2]
                if height > self.HEIGHT or width > self.WIDTH:
                    image = imutils.resize(image, width=self.WIDTH, 
                                           height=self.HEIGHT,)
            except Exception as e:
                print(e.args)
            finally:
                return image
    
    """encode_image changes a vs2 gray scale facial image into encoded
    vectors of size 128 in a numpy array, and this encodng(s) is then
    serialised (or pickled), for tranmission (via sockets) to the Master
    Pi for authentication."""
    def encode_image(self):
        p_data = None
        if (self.image is not None):
            try:
                # find any faces in image
                face_boxes = face_recognition.face_locations(self.image, model="hog")
                # encode face(s)
                encodings = face_recognition.face_encodings(self.image, face_boxes)
                # prepare encodings for transmission via sockets
                data = {"encodings": encodings}
                p_data = pickle.dumps(data)
            except Exception:
                print("""There was a problem encoding face data for 
                    tranmission, please try again""")
        return p_data