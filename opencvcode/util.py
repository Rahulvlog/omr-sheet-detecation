from imutils.perspective import four_point_transform
import cv2
from imutils import contours
import imutils
import numpy as np
correctAnswer = 2

def selectedBubble(q, thresh, questionRowBubbles):
    bubbled = None
    selected =  -1
    for (j, c) in enumerate(questionRowBubbles):
        mask = np.zeros(thresh.shape, dtype="uint8")
        cv2.drawContours(mask, [c], -1, 255, -1)

        # cv2.imshow(f'{j} counter found', mask)
        
        mask = cv2.bitwise_and(thresh, thresh, mask=mask)
        # cv2.imshow(f'{j} mask counter found', mask)
        total = cv2.countNonZero(mask)
        # print(f'{q} for {j} counter non zero total found {total}')

        if bubbled is None or total > bubbled[0]:
            bubbled = (total, j)
    
    if bubbled[0] > 300:
        selected = bubbled[1]       
            
    return selected

def getQuestionBubbleBox(edged):
    boxes = []
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    print(f'{len(cnts)} total found')

    blank = np.zeros(edged.shape, dtype='uint8')
    cv2.drawContours(blank, cnts, -1 , (0,0,255), 1)
    # cv2.imshow('blank', blank)

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:4]

    # docCnt = None

    # ensure that at least one contour was found
    if len(cnts) > 0:
        # sort the contours according to their size in
        # descending order
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        # loop over the sorted contours
        for c in cnts:
            # approximate the contour
            peri = cv2.arcLength(c, True)
            approx = cv2.approxPolyDP(c, 0.02 * peri, True)
            # if our approximated contour has four points,
            # then we can assume we have found the paper
            if len(approx) == 4:
                # docCnt = approx
                boxes.append(approx)
                # break
    return boxes

def getAllQuestionBubbles(cnts): 
    questionCnts = []
    # loop over the contours
    for c in cnts:    
        # compute the bounding box of the contour, then use the
        # bounding box to derive the aspect ratio
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)  
        
        # in order to label the contour as a question, region
        # should be sufficiently wide, sufficiently tall, and
        # have an aspect ratio approximately equal to 1
        if w >= 17 and h >= 17 and ar >= 0.9 and ar <= 1.3:
        # if w >= 8 and h >= 8 and ar >= 0.7 and ar <= 1.2:
            questionCnts.append(c)
            
    print("how many numbers of question", len(questionCnts))
            
    questionCnts = contours.sort_contours(questionCnts, method="top-to-bottom")[0]
    return questionCnts

def getBoxResult(image, thresh, questionBubbles):
    blank = np.zeros(image.shape, dtype='uint8')
    correct = 0
    for (q, i) in enumerate(np.arange(0, len(questionBubbles), 4)):
        questionRowBubbles = contours.sort_contours(questionBubbles[i: i+4])[0]
        selectedOptionBubble = selectedBubble(q, thresh, questionRowBubbles)
        # color = (0, 0, 255)
        if correctAnswer == selectedOptionBubble:
            # color = (0, 255, 0)
            correct += 1

        # cv2.drawContours(image, [questionRowBubbles[0]], -1, color, 3)
        cv2.drawContours(blank, questionRowBubbles, -1 , (255,255,255), 1)
        cv2.imshow('blank123', blank)
       
        cv2.waitKey()
        # break
    
    return correct; 

def processSingleBox(image, gray, docCnt):
    # blank = np.zeros(image.shape, dtype='uint8')
    # apply a four point perspective transform to both the
    # original image and grayscale image to obtain a top-down
    # birds eye view of the paper
    # paper = four_point_transform(image, docCnt.reshape(4, 2))
    val = 230
    # for val in range(250,val,-1):
    for val in reversed(range(val,255)):
        print("what is length", val)
        warped = four_point_transform(gray, docCnt.reshape(4, 2))
       # cv2.imshow('paper', paper)
        # cv2.imshow('warped', warped)
        # print(len(warped))
        # thresh = cv2.threshold(warped, 250, 255, cv2.THRESH_BINARY_INV)[1]
        # thresh = cv2.threshold(warped, 217, 255, cv2.THRESH_TOZERO)[1]
        # thresh = cv2.adaptiveThreshold(warped, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        #                                   cv2.THRESH_BINARY, 199, 2)
        
        
        
        thresh = cv2.adaptiveThreshold(warped, val, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV , 13, 3)
        threshContours = cv2.findContours(thresh.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        threshContours = imutils.grab_contours(threshContours)
        # print("what lenght thresh", threshContours)
        # print(len(warped))
        cv2.imshow(f'{val}  - thresh display', thresh)
        # color1 = (0, 255, 0)
        # cv2.drawContours(image, threshContours, -1, color1, 3)
        # cv2.waitKey()
        
        questionBubbles = getAllQuestionBubbles(threshContours)
        cv2.drawContours(image, questionBubbles, -1, (255, 0, 0), 3)
        cv2.imshow('draw question bubbles', image)
        # cv2.waitKey()
          
        if len(questionBubbles) <= 210:
        # print(f'{len(questionBubbles)} question bubbles found')  
            correct = getBoxResult(image, thresh, questionBubbles)
            return correct
        # break
        
    return 0