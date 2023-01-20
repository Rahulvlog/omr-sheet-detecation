import cv2
from util import getQuestionBubbleBox, processSingleBox
import os

def processImage(path):
	images = cv2.imread(path)
	image = cv2.resize(images, (827, 1170))

	cv2.imshow('image', image)	
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		# cv2.imshow('gray', gray)
	blurred = cv2.GaussianBlur(gray, (5,5), 0)
		# cv2.imshow('blurred', blurred)	
	edged = cv2.Canny(blurred, 75, 200)
 
	# cv2.imshow('edged', edged)	
		# blank = np.zeros(image.shape, dtype='uint8')

	cv2.waitKey()
		
	boxes = getQuestionBubbleBox(edged)
		# print(f'{len(boxes)} boxes found')

	totalCorrect = 0
	cnt = 1
	for box in boxes:   
		correct = processSingleBox(image, gray, box)
			# score = (correct / 25.0) * 100
			# print("Box value " +  str(cnt) + "INFO Score for score is : {:.2f}%".format(score))
		totalCorrect = totalCorrect + correct
		
	totalScore = (totalCorrect / 100.0) * 100
		# print("Overall Score: {:.2f}%".format(totalScore))
	cv2.putText(image, "{:.2f}%".format(totalScore), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
	cv2.imshow('image', image)
		# cv2.imshow('paper', paper)

		
		# cv2.drawContours(blank, bubblesCnts, -1 , (255,255,255), 1)
		# cv2.imshow('blank', blank)

		# cv2.waitKey(0)
	return totalScore
 

# path = "D://testing23//omr//imgs//" 
# for x in os.listdir(path):
#     url = 'imgs/' + x
#     totalScore = processImage(url)s
#     print(f'{x} : ' + "{:.2f}%".format(totalScore))

# totalScore = processImage('imgs/tmp_5ccfb5a1-c515-4a54-9d28-ff054a46f797.jpeg')
# totalScore = processImage('imgs/tmp_495ae83e-9448-4b5f-9976-5750c6a89f90.jpeg')
# totalScore = processImage('imgs/image.png')
# totalScore = processImage('imgs/paper.jpeg')
totalScore = processImage('imgs/paper10.jpeg')
print(f'paper.jpeg : ' + "{:.2f}%".format(totalScore))
cv2.waitKey()
cv2.destroyAllWindows()
