from pytesseract import Output
import pytesseract
import cv2
import numpy as np
import re
import imutils
from transform import four_point_transform
from skimage.filters import threshold_local


image = cv2.imread('test.jpg')
ratio = image.shape[0] / 500.0
orig = image.copy()
#image = imutils.resize(image, height = 500)
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 75, 200)
# show the original image and the edge detected image
print("STEP 1: Edge Detection")
cv2.imwrite("Image.jpg", image)
cv2.imwrite("Edged.jpg", edged)

edge = False
if edge:
    # find the contours in the edged image, keeping only the
    # largest ones, and initialize the screen contour
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
    # loop over the contours
    for c in cnts:
        # approximate the contour
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        # if our approximated contour has four points, then we
        # can assume that we have found our screen
        if len(approx) == 4:
            screenCnt = approx
            break
    # show the contour (outline) of the piece of paper
    print("STEP 2: Find contours of paper")
    cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    cv2.imwrite("Outline.jpg", image)

    # apply the four point transform to obtain a top-down
    # view of the original image
    warped = four_point_transform(orig, screenCnt.reshape(4, 2) * ratio)
    # convert the warped image to grayscale, then threshold it
    # to give it that 'black and white' paper effect
    warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped, 11, offset = 10, method = "gaussian")
    warped = (warped > T).astype("uint8") * 255
    # show the original and scanned images
    print("STEP 3: Apply perspective transform")
    #cv2.imwrite("Original.jpg", imutils.resize(orig, height = 650))
    #cv2.imwrite("Scanned.jpg", imutils.resize(warped, height = 650))
else:
    test = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    T = threshold_local(test, 11, offset = 9, method = "gaussian")
    warped = (test > T).astype("uint8") * 255
    # show the original and scanned images
    print("STEP 3: Apply perspective transform")
    cv2.imwrite("Original.jpg",image)#, imutils.resize(image, height = 650))
    cv2.imwrite("Scanned.jpg",warped)#, imutils.resize(test, height = 650))

results = pytesseract.image_to_data(warped, output_type=Output.DICT)
rgb = cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)
open('test.txt', 'w').write(pytesseract.image_to_string(rgb))

# loop over each of the individual text localizations
for i in range(0, len(results["text"])):
	# extract the bounding box coordinates of the text region from
	# the current result
	x = results["left"][i]
	y = results["top"][i]
	w = results["width"][i]
	h = results["height"][i]
	# extract the OCR text itself along with the confidence of the
	# text localization
	text = results["text"][i]
	conf = int(results["conf"][i])
        
# filter out weak confidence text localizations
	if conf > 50:
		# display the confidence and text to our terminal
		print("Confidence: {}".format(conf))
		print("Text: {}".format(text))
		print("")
		# strip out non-ASCII text so we can draw the text on the image
		# using OpenCV, then draw a bounding box around the text along
		# with the text itself
		text = "".join([c if ord(c) < 128 else "" for c in text]).strip()
		cv2.rectangle(rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)
		cv2.putText(rgb, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
			1.2, (0, 0, 255), 3)
# show the output image
cv2.imwrite("Result.jpg", rgb)