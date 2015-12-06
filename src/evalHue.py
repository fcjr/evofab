import numpy as np
import argparse
import cv2
import sys

#CLASS FOR USE AS A MODULE

#Creates a camera object to generate inputs for the
#neural network
#Takes an integer for the camera value, and then number of
#segments width-wise and height-wise in integers as well.
#Optional: crop (Boolean), crops camera to square before processing
#		   iff crop == True (Defaults to True)
class EvoCamera:
	def __init__(self, camera, w, h, crop=True):
		self.camera = cv2.VideoCapture(camera)
		self.crop = crop
		self.w = w
		self.h = h

	#Returns an array of the decimal(percent) fill
	#of each segment of the camera  (as floats).
	def getVals(self):
		#grab static image
		junk,image = self.camera.read()

		#crop the image to a square if requested
		if self.crop:
			image = Crop(image)

		#Process Image to create black white image
		processedImage = HueProcess(image)

		#generate output numbers based on griding
		#and return
		return ProcessGrid(processedImage,self.w,self.h)

	#Releases the camera from OpenCV for use elsewhere.
	#**Object is no longer functional once this is called**
	def closeCamera(self):
		self.camera.release()


#MAIN PROCESSING CODE

#crops given image into a square
#uses the shortest edge length as the boundary
def Crop(cv_img):
	height, width, junk = cv_img.shape
	if height < width:
		pad = (width - height) / 2
		cropped = cv_img[0:height,pad:pad+height]
	else:
		pad = (height - width) / 2
		cropped = cv_img[pad:pad+width,0:width]
	return cropped


#Takes a colored image, returns a black and white image
#where the white is where a desired color appears
#(Currently Blue)
def HueProcess(cv_img):

	#apply a 5x5 Gaussian Blur to the source
	#image to remove some noise.
	blur = cv2.GaussianBlur(cv_img,(5,5),0)

	#convert the source image to HSV
	hsv_img = cv2.cvtColor(blur,cv2.COLOR_BGR2HSV)

	# define range of blue color in HSV
	lower_blue = np.array([110,50,50])
	upper_blue = np.array([130,255,255])

	# Threshold the HSV image to get only blue colors
	mask = cv2.inRange(hsv_img, lower_blue, upper_blue)

	return mask

#returns the percentage of a black and white image
#that is white in decimal form as a float.
def PercentColored(bw_image):
	nonZero = cv2.countNonZero(bw_image)
	total = bw_image.size
	decimal = float(nonZero)/float(total)
	return decimal

#Crops the black and white mask into sections
#and calls PercentColored on each section
#returns an array of the results from PercentColored (of floats)
def ProcessGrid(bw_image,w_seg,h_seg):
	ret = []
	height, width = bw_image.shape

	#PROCESS IMAGES
	# Define the window size
	windowsize_h = height/h_seg
	windowsize_w = width/w_seg

	for h in range(h_seg):
		for w in range(w_seg):
			window = bw_image[h*windowsize_h:h*windowsize_h+windowsize_h,w*windowsize_w:w*windowsize_w+windowsize_w]

			#PROCESS IMAGE "window" HERE
			ret.append(PercentColored(window))
	return ret


#Displays a visual represntation of detection
#displays a green transparency over the sections where the
#color is more than 50% present
def Display(image,valArray,w_seg,h_seg):
	height, width, junk = image.shape
	windowsize_h = height/h_seg
	windowsize_w = width/w_seg
	count = 0
	for h in range(h_seg):
		for w in range(w_seg):
			if valArray[count] > 0.5:
				overlay = image.copy()
				x,y = (h*windowsize_h,w*windowsize_w)
				cv2.rectangle(overlay,(y,x),(y+windowsize_w,x+windowsize_h),(0, 255, 0), thickness = -1)
				opacity = 0.4
				cv2.addWeighted(overlay, opacity, image, 1 - opacity, 0, image)
			count = count + 1
	cv2.imshow('EvoFab: Color Detection',image)
	return image


#MAIN LOOP
if __name__ == '__main__':
	try:
		# construct the argument parser and parse the arguments
		ap = argparse.ArgumentParser()
		ap.add_argument("-c", "--camera", required = True, help = "Camera Input Number (Integer. Starts at 0)")
		ap.add_argument("-v", "--visual",action='store_true', help = "Display visual feedback.")
		ap.add_argument("-p", "--print",action='store_true', help = "Print output values to console.")
		ap.add_argument("-s", "--square",action='store_true', help = "Crops camera input to a square.")
		ap.add_argument("-f", "--flip",action='store_true', help = "Inverts camera vertically.")
		args = vars(ap.parse_args())

		#Setup Video Capture
		cap = cv2.VideoCapture(int(args["camera"]))

		#Adjust these values to change the size of the
		#detection griding.
		h, w = (3, 3)

		#Main Run Loop
		while cap.isOpened():
			#grab static image
			junk,image = cap.read()

			#crop if requested
			if args["square"]:
				image = Crop(image)

			#flip the source frame vertically if requested
			if args["flip"]:
				image = cv2.flip(image,1)

			#Process Image to create black white image
			processedImage = HueProcess(image)

			#generate output numbers based on griding
			ret = ProcessGrid(processedImage,w,h)

			#Display a visual represntation of detection if requested
			if args["visual"]:
				Display(image,ret,w,h)

			#return color percentages
			if args["print"]:
				print ret

			#quit the program if "q" is pressed while the visualization
			#window is active
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
	except KeyboardInterrupt:
		pass

	# When everything done or user quits, release the capture
	cap.release()
	cv2.destroyAllWindows()
	sys.exit()
