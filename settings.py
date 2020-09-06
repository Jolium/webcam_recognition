from pathlib import Path


"""
Settings of recognition.py
"""

# Global vars
folder_path = Path.cwd() / 'images'         # Path to main folder ('Path.home()' for home directory)
allowed_formats = ('.jpg', '.png')          # Allowed pictures formats
database = Path.cwd() / 'database.json'     # Database file
auto_check = 1                              # Checks each start for changes in main folder

# webcam vars
webcam = 0              # '0' is the standard webcam                    default = 0
video_size = '640 x 360 (16:9)'
width = 640             # Width of the frames in the video stream       default = 640
height = 360            # Height of the frames in the video stream      default = 480
frames = 30             # Frame rate (25, 60)                           default = 30
brightness = 0          # Brightness of the image (-64, 64)             default = 0
contrast = 4            # Contrast of the image (0, 95)                 default = 4
saturation = 67         # Saturation of the image (0, 100)              default = 67
hue = 0                 # Hue of the image (-2000, 2000)                default = 0
exposure = 0            # Exposure (-7, 0)                              default = 0
sharpness = 2           # Sharpness (1, 7)                              default = 2
auto_exposure = 3       # Auto Exposure (0, 3)                          default = 3
gamma = 100             # Gamma (100, 300)                              default = 100
temperature = 2800      # Temperature (2800, 6500)                      default = 2800
focus = 0               # Focus (0, 255) increment: 5                   default = 0
backlight = 0           # Backlight (0, 3)                              default = 0
auto_focus = 1          # Auto Focus (0, 1)                             default = 1
auto_white_balance = 1  # Auto White Balance (0, 1)                     default = 1
white_balance = 4600    # White Balance (2800, 6500)                    default = 4600
