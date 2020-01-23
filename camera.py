import subprocess
import os

def take_picture():
	filename = _generate_pic_filename()
	subprocess.call(["fswebcam", filename])
	
def _generate_pic_filename(base_filename="image"):
	image_number = 0
	filename = "./" + base_filename + str(image_number) + ".jpg"
	while os.path.exists(filename):
		image_number += 1
		filename = "./" + base_filename + str(image_number) + ".jpg"
	return filename

