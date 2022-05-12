from picamera import PiCamera
from time import sleep
from subprocess import call
import subprocess
from utils import createDirectoryIfNotExists, upload_files_to_S3, post_call
import threading
import os
from datetime import datetime
import time

resolution = (1024, 768)

photos_base_path = '/home/pi/tapan-pi/Photos'
videos_base_path = '/home/pi/tapan-pi/Videos'

createDirectoryIfNotExists(photos_base_path)
createDirectoryIfNotExists(videos_base_path)

camera = PiCamera()
camera.resolution = resolution
camera.hflip = True
camera.brightness = 55 

def upload_to_s3(filename):
	mp4_filename = filename.split(".")[0].split("/")[-1] + ".mp4"
	mp4_filepath = filename.split(".")[0] + ".mp4"
	command = "MP4Box -add " + filename + ":fps=32" + " -new " + mp4_filepath
	call([command], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	upload_files_to_S3(mp4_filepath, mp4_filename)

def fn(filename, no):
	framepath = f'{photos_base_path}/image-{no}.jpeg'
	command = f"ffmpeg -i {filename} -ss 00:00:00.250 -s 160x160 -vframes 1 -y {framepath}"
	call([command], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
	post_call(framepath, no)
	upload_to_s3(filename)


def record_video():
	threads = []
	filename = f'{videos_base_path}/clip01.h264'
	print('Recording Started!!!')
	for i in range(600):
		file_no = ""
		if i < 9:
			file_no = f"00{i + 1}"
		elif i < 99:
			file_no = f"0{i + 1}"
		else:
			file_no = str(i + 1)
		filename = f'{videos_base_path}/clip-{file_no}.h264'
		camera.start_recording(filename)
		camera.wait_recording(0.5)
		camera.stop_recording()
		t = threading.Thread(target=fn, args=(filename, i + 1), daemon=True)
		t.start()
		threads.append(t)
	for t in threads:
		t.join()
	
	print('Recording Done!!!')


def merge_videos():
	f = open("mylist.txt", "w")
	for i in range(600):
		file_no = ""
		if i < 9:
			file_no = f"00{i + 1}"
		elif i < 99:
			file_no = f"0{i + 1}"
		else:
			file_no = str(i + 1)
		filename = f'{videos_base_path}/clip-{file_no}.h264'
		print(f"file {filename}", file=f)
	f.close()
	command = f"ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.h264"
	os.system(command)
	upload_to_s3("output.h264")


if __name__ == '__main__':
	camera.start_preview()
	sleep(2)

	record_video()
	camera.stop_preview()
	for f in os.listdir(videos_base_path):
		os.remove(os.path.join(videos_base_path, f))
	for f in os.listdir(photos_base_path):
		os.remove(os.path.join(photos_base_path, f))

