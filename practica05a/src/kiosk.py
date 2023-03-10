#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# kyosk.py
#
# Author:  Mauricio Matamoros
# Date:    2023.02.14
# License: MIT
#
# Plays a set of files using VLC with the Raspberry Pi
#

import vlc
import time

home = '/home/pi'

def create_media():
	video = vlc.Media(f'{home}/videos/video.mp4')
	pics = []
	for i in range(1,5):
		pics.append(vlc.Media(f'{home}/pictures/pic0{i}.jpg'))
	return video, pics
# end def



def play_video(player, video):
	# Load the media into the player
	player.set_media(video)

	# Play the video
	player.play()

	# Slowly increase volume
	for i in range(101):
		player.audio_set_volume(i)
		time.sleep(0.1)
	# Let the video play for 10 secs
	time.sleep(10)
	# Slowly decrease volume
	for i in range(100, -1, -1):
		player.audio_set_volume(i)
		time.sleep(0.1)
# end def



def loop_pics(player, pics):
	i = 0
	while(True):
		player.set_media(pics[i])
		player.play()
		time.sleep(3)
		i = (i + 1) % len(pics)
# end def



def main():
	# Create the player
	player = vlc.MediaPlayer()
	player.set_fullscreen(True)

	# Create the media objects
	video, pics = create_media()

	# Play video
	play_video(player, video)

	# Play pictures in loop
	loop_pics(player, pics)
# end def



if __name__ == '__main__':
	main()