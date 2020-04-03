import subprocess
import os

def take_picture(label):
	os.makedirs(os.path.join("images", label), exist_ok=True)
	print("Taking Picture")
	filename = _generate_pic_filename(label)
	subprocess.call(["fswebcam", "-r", "512x384", filename])
	print("Picture Taken")
	
def _generate_pic_filename(folder_name, base_filename="image"):
	image_number = 0
	filename = os.path.join("images", folder_name, base_filename + str(image_number) + ".png")
	while os.path.exists(filename):
		image_number += 1
		filename = os.path.join("images", folder_name, base_filename + str(image_number) + ".png")
	return filename
