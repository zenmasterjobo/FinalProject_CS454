#!/usr/bin/python
import cv2
import cv2.cv as cv
import numpy as np
import math

#each element contains x,y,radius
circleCoordVect = []
circleOCRBoundingBox = []

def findCircles(img, cimg):
    circles = cv2.HoughCircles(img,cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=50,minRadius=10,maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        circPair = []
        squarePair = []
        cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
        circPair.append(i[0])
        squarePair.append(i[0])
        circPair.append(i[1])
        squarePair.append(i[1])
        circPair.append(i[2])
        circleCoordVect.append(circPair)
        squarePair.append(i[2]*math.sqrt(2))
        circleOCRBoundingBox.append(squarePair)

#def ocr(originaImage,x1,y1,x2,y2)
# somehow do OCR on the bounding box and return that integer found
        
def findStateLabels(cimg):
    for i in circleOCRBoundingBox:
        point1 = []
        point2 = []
        
        x1 = math.floor(i[0]-(i[2]/2))
        y1 = math.floor(i[1]-(i[2]/2))
        x2 = math.floor(i[0]+(i[2]/2))
        y2 = math.floor(i[1]+(i[2]/2))
        point1.append(x1)
        point1.append(y1)
        
        point2.append(x2)
        point2.append(y2)
               
        cv2.rectangle(cimg,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,255),1)
        #ocr (some black and white image, x1,y1,x2,y2)
        #take what ocr returns and relate those coordinates to the
        #circle coord vector so the circle get an integer label

        
def main():
    img = cv2.imread('Test1.png',0)
    img = cv2.medianBlur(img,5)
    cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

    findCircles(img, cimg)
    findStateLabels(cimg)
            
    cv2.imwrite('output.png',cimg)
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
	main()
