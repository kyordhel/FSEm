#!/bin/python3
#
# kyosk.py
#
# Author:  Mauricio Matamoros
# Date:    2023.02.14
# License: MIT
#
# Plays a video file using VLC with the Raspberry Pi
#

import vlc
import time

player = vlc.MediaPlayer()
video = vlc.Media('/home/pi/videos/video.mp4')
player.set_media(video)
player.play()
while player.is_playing:
	time.sleep(0)
