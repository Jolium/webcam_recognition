# coding:utf-8
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivy.uix.image import Image
from kivy.clock import Clock
from kivy.graphics.texture import Texture
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
# from kivy.uix.button import Button
# from kivy.uix.dropdown import DropDown
# from kivy.uix.floatlayout import FloatLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.camera import Camera
# from kivy.uix.label import Label
# from kivy.uix.popup import Popup
# from kivy.uix.textinput import TextInput
# from kivy.uix.widget import Widget
# from kivy.utils import platform

import face_recognition
import cv2
import numpy as np
from pathlib import Path
import os.path

import encoder
import hash_sha1
import settings as sets


# webcam vars
width = sets.width                              # Width of the frames in the video stream       default = 640
height = sets.height                            # Height of the frames in the video stream      default = 480
frames = sets.frames                            # Frame rate                                    default = 30
brightness = sets.brightness                    # Brightness of the image (-64, 64)             default = 0
contrast = sets.contrast                        # Contrast of the image (0, 92)                 default = 4
saturation = sets.saturation                    # Saturation of the image (0, 67)               default = 67
hue = sets.hue                                  # Hue of the image (-2000, 2000)                default = 0
exposure = sets.exposure                        # Exposure (-7, 0)                              default = 0
sharpness = sets.sharpness                      # Sharpness (1, 7)                              default = 2
auto_exposure = sets.auto_exposure              # Auto Exposure (0, 3)                          default = 3
gamma = sets.gamma                              # Gamma (100, 300)                              default = 100
temperature = sets.temperature                  # Temperature (2800, 6500)                      default = 2800
focus = sets.focus                              # Focus (0, 255) increment: 5                   default = 0
backlight = sets.backlight                       # Backlight (0, 3)                              default = 0
auto_focus = sets.auto_focus                    # Auto Focus (0, 1)                             default = 1
auto_white_balance = sets.auto_white_balance    # Auto White Balance (0, 1)                     default = 0
white_balance = sets.white_balance              # White Balance (4000, 7000)                    default = 5000


Window.size = (width*1.5, height*1.5 + 48)
Window.clearcolor = (.1, .1, .1, 1)

# Auto check for new pictures and if needed folder/database already exist on start up
auto_check = sets.auto_check  # 1=True, 0=False  ('0' starts up faster)

# Add face recognition to camera
process_this_frame = False

# Start video capture
capture = cv2.VideoCapture(sets.webcam)


class MySettings(Screen):
    """Class for creating a Slider widget."""
    isShownMenu = BooleanProperty(False)

    def __init__(self, **kwargs):
        super(MySettings, self).__init__(**kwargs)

    def myframe(self):
        global process_this_frame

        if process_this_frame:
            process_this_frame = False
        else:
            process_this_frame = True

    def up_width(self, *args):
        global width, capture
        width = int(args[1])
        capture.set(3, width)  # Width of the frames in the video stream
        # print(width)

    def up_height(self, *args):
        global height, capture
        height = int(args[1])
        capture.set(4, height)  # Height of the frames in the video stream
        # print(height)

    def up_video_size(self, *args):
        global width, height, capture
        size = str(args[1])

        if size == '640 x 480 (4:3)':
            self.up_width(self, 640)
            self.up_height(self, 480)
        elif size == '800 x 600 (4:3)':
            self.up_width(self, 800)
            self.up_height(self, 600)
        elif size == '960 x 720 (4:3)':
            self.up_width(self, 960)
            self.up_height(self, 720)
        elif size == '1280 x 960 (4:3)':
            self.up_width(self, 1280)
            self.up_height(self, 960)
        elif size == '960 x 540 (16:9)':
            self.up_width(self, 960)
            self.up_height(self, 540)
        elif size == '1280 x 720 (16:9)':
            self.up_width(self, 1280)
            self.up_height(self, 720)
        elif size == '1920 x 1080 (16:9)':
            self.up_width(self, 1280)
            self.up_height(self, 720)
        else:
            self.up_width(self, 640)
            self.up_height(self, 360)
        # print(size)

    def up_frames(self, *args):
        global frames, capture
        frames = int(args[1])
        capture.set(5, frames)  # Frame rate (frames per second)
        # print(frames)

    def up_check(self, *args):
        global auto_check, capture
        auto_check = int(args[1])  # Auto check on start up
        # print(auto_check)

    def up_brightness(self, *args):
        global brightness, capture
        brightness = int(args[1])
        capture.set(10, brightness)  # Brightness of the image
        # print(brightness)

    def up_contrast(self, *args):
        global contrast, capture
        contrast = int(args[1])
        capture.set(11, contrast)  # Contrast of the image
        # print(contrast)

    def up_saturation(self, *args):
        global saturation, capture
        saturation = int(args[1])
        capture.set(12, saturation)  # Saturation of the image
        # print(saturation)

    def up_hue(self, *args):
        global hue, capture
        hue = int(args[1])
        capture.set(13, hue)  # Hue of the image
        # print(hue)

    def up_exposure(self, *args):
        global exposure, capture
        exposure = float((args[1])/50)
        capture.set(15, exposure)  # Exposure
        # print(exposure)

    def up_sharpness(self, *args):
        global sharpness, capture
        sharpness = int(args[1])
        capture.set(20, sharpness)  # Sharpness of the image
        # print(sharpness)

    def up_auto_exposure(self, *args):
        global auto_exposure, capture
        auto_exposure = int(args[1])
        capture.set(21, auto_exposure)  # Auto Exposure of the image
        # print(auto_exposure)

    def up_gamma(self, *args):
        global gamma, capture
        gamma = int(args[1])
        capture.set(22, gamma)  # Gamma of the image
        # print(gamma)

    def up_temperature(self, *args):
        global temperature, capture
        temperature = int(args[1])
        capture.set(23, temperature)  # Temperature of the image
        # print(temperature)

    def up_focus(self, *args):
        global focus, capture
        focus = float(args[1])
        capture.set(28, focus)  # Focus
        # print(focus)

    def up_backlight(self, *args):
        global backlight, capture
        backlight = int(args[1])
        capture.set(32, backlight)  # Backlight of the image
        # print(backlight)

    def up_auto_focus(self, *args):
        global auto_focus, capture
        auto_focus = int(args[1])
        capture.set(39, auto_focus)  # Auto Focus of the image
        # print(auto_focus)

    def up_auto_white_balance(self, *args):
        global auto_white_balance, capture
        auto_white_balance = int(args[1])
        capture.set(44, auto_white_balance)  # Auto White Balance of the image
        # print(auto_white_balance)

    def up_white_balance(self, *args):
        global white_balance, capture
        white_balance = int(args[1])
        capture.set(45, white_balance)  # White Balance
        # print(white_balance)


class MyManager(ScreenManager):
    pass


class KivyCamera(Image):

    def __init__(self, **kwargs):
        super(KivyCamera, self).__init__(**kwargs)
        global capture
        if not capture.isOpened():
            print("Cannot open camera")
            exit()
        self.cam_settings()
        Clock.schedule_interval(self.update, 1.0 / frames)

    def cam_settings(self):
        capture.set(3, width)
        capture.set(4, height)
        capture.set(5, frames)
        capture.set(10, brightness)
        capture.set(11, contrast)
        capture.set(12, saturation)
        capture.set(13, hue)
        capture.set(15, exposure)
        capture.set(20, sharpness)
        capture.set(21, auto_exposure)
        capture.set(22, gamma)
        capture.set(23, temperature)
        capture.set(28, focus)
        capture.set(32, backlight)
        capture.set(39, auto_focus)
        capture.set(44, auto_white_balance)
        capture.set(45, white_balance)

        # # Check if property id is supported
        # print(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

    def update(self, dt):
        # Import encodings and names from json files
        known_face_encodings, known_face_names = encoder.import_from_database()  # ==========

        # Initialize some variables
        face_locations = []  # =================
        # face_encodings = []
        face_names = []  # ===================

        # Grab a single frame of video
        ret, frame = capture.read()

        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            exit(1)

        # Resize frame of video to 1/4 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]  # =================

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                name = "Unknown"
                frame_color = (0, 0, 255)  # Red

                # Check if database is not empty
                if len(known_face_encodings) != 0:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

                    # # If a match was found in known_face_encodings, just use the first one.
                    # if True in matches:
                    #     first_match_index = matches.id(True)
                    #     name = known_face_names[first_match_index]

                    # Or instead, use the known face with the smallest distance to the new face
                    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                        frame_color = (0, 255, 0)  # Green

                face_names.append(name)

        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), frame_color, 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 30), (right, bottom), frame_color, cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.8, (255, 255, 255), 1)

        if ret:
            # convert it to texture
            buf1 = cv2.flip(frame, 0)
            buf = buf1.tostring()
            image_texture = Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='bgr')
            image_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')

            # display image from the texture
            self.texture = image_texture


Builder.load_file('mycam.kv')

# Create the screen manager
sm = ScreenManager()
sm.add_widget(MySettings(name='settings'))

# By default, the first screen added into the ScreenManager will be
# displayed. You can then change to another screen.
sm.current = 'settings'


class MyCamApp(App):
    def build(self):
        return sm

    def on_stop(self):
        # Release handle to the webcam
        global capture
        capture.release()
        cv2.destroyAllWindows()
        print("Closed")


if __name__ == '__main__':
    # Auto check for new pictures and if needed folder/database already exist on start up
    if auto_check:

        path_folder = sets.folder_path

        # Create main folder if it does not exist
        if not Path.is_dir(path_folder):
            path_folder.mkdir()

        # Create database if it does not exist
        if not Path.is_file(sets.database):
            encoder.create_database()

        # Check if are changes in the main folder
        hash_sha1.compare_hashes()

    MyCamApp().run()
