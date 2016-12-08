#!/usr/bin/python
import cv2
import cv2.cv as cv
import numpy as np
import math
import pytesser as pt
from PIL import Image
from PIL import ImageFilter

# you can use this like s = State(label, coord, etc) 
class State:
    def __init__(self, label, coord_x, coord_y, initial, final, radius, circumference):
        self.label = label
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.initial = initial
        self.final = final
        self.radius = radius
        self.circumference = circumference

#each element contains x,y,radius
circleOCRBoundingBox = []
States = []
#filename = raw_input("Please state the file you want to use: ")
filename = "Test1.png"
def findCircles(img):
    gray = cv2.imread(filename,0)
    circles = cv2.HoughCircles(gray,cv.CV_HOUGH_GRADIENT,1,\
                               20,param1=50,param2=50,minRadius=10,maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        squarePair = []
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
        squarePair.append(i[0])
        squarePair.append(i[1])
        state = State(None, i[0], i[1], False, False, i[2], 2*i[2]*np.pi);
        States.append(state)
        squarePair.append(i[2]*math.sqrt(2))
        print "SQUARE PAIR: ", squarePair
        circleOCRBoundingBox.append(squarePair)
        print "BOUNDING BOX: ", circleOCRBoundingBox
    val = float("inf")
    for circle in States:
        if circle.circumference < val:
            val = circle.circumference
    for circle in States:
        if circle.circumference == val:
            circle.final = True;
        
        #def ocr(originaImage,x1,y1,x2,y2)
# somehow do OCR on the bounding box and return that integer found
        
def findStateLabels(img):
    gray = cv2.imread(filename,0)
    blur = cv2.GaussianBlur(gray,(5,5),3)
    idx = 0
    for i in circleOCRBoundingBox:
        idx += 1
        point1 = []
        point2 = []
        
        x1 = math.floor(i[0])
        y1 = math.floor(i[1]-(i[2]/2))
        x2 = math.floor(i[0]+(i[2]/2))
        y2 = math.floor(i[1]+(i[2]/2))
        point1.append(x1)
        point1.append(y1)
        
        point2.append(x2)
        point2.append(y2)

        cv2.rectangle(img,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,255),1)
        #uncomment to draw rectangle
        
        #roi = blur[y1:y2, x1:x2]
        #cv2.imwrite(str(idx) + '.png', roi)
        #thresher = cv2.imread("3.png")
        #ret,thresh1 = cv2.threshold(thresher,178,255,cv2.THRESH_BINARY)
        #cv2.imwrite( '3h.png', thresh1)
        
        # roi is region of interest.
        # it is a matrix of pixels i think

    #image_file = "3h.png"
    #im = Image.open(image_file)
    #im.filter(ImageFilter.SHARPEN)
    #print ("here is the supposed image")
    #print im
    #i = pt.image_to_string(im)
    #print "=====Label======="
    #print i
    #print "=====Label=======\n"
    
def findTriangle(img):
    localImg = cv2.imread(filename,0)
    ret,thresh = cv2.threshold(localImg,127,255,1)
    contours,h = cv2.findContours(thresh,1,2)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        if len(approx)==3:
            print "triangle"
            cv2.drawContours(img,[cnt],0,(0,255,0),-1)

            print "1st field: ", cnt[0], "2nd field : ", cnt[1],\
                "3rd Field: ", cnt[2],\
                "4th field: ", cnt[3], "5th field: ", cnt[4]
            #print "Ret : ", ret
            triangleTipY = approx[1][0][1]
            triangleTipX = approx[1][0][0]
            return triangleTipY, triangleTipX
            
def findStart(img):
    localImg = cv2.imread(filename,0)
    triangleTipY, triangleTipX = findTriangle(img)
    comparisonStates = []
    for state in States:
        print " Y COORD: ", state.coord_y, "X COORD: ",\

        \ and "THE JUST THE TIP Y + 2: ", triangleTipY
        if(state.coord_y <= triangleTipY + 2
           \and state.coord_y >= triangleTipY - 2):
            comparisonStates.append(state)

    x = comparisonStates[0].coord_x
    initialState = ''
    for state in comparisonStates:
        if(state.coord_x >= triangleTipX):
            if(statw.coord_x <= x):
                x = state.coord_x
                initialState = state
#    print initialState.coord_x, initialState.coord_y
    for state in States:
        if(initialState.coord_x == state.coord_x and initialState.coord_y == state.coord_y):
            print state.coord_x, state.coord_y
            state.initial = True
            cv2.circle(img,(state.coord_x,state.coord_y),state.radius,(255,0,0),2)
    for i in States:
        print "x coordinate: ",i.coord_x
        print "y coodinate: ",i.coord_y
        print "Intial: ",i.initial
        print "Circumference: ",i.circumference
        print "Final: ",i.final
        if i.final == True:
            cv2.circle(img,(i.coord_x,i.coord_y),i.radius,(0,0,255),2)
        print "===================="
def findLines(img):
    localImg = cv2.imread(filename,0)
    #edges = cv2.Canny(localImg,50,150,apertureSize = 3)
    #lines = cv2.HoughLinesP(image=edges,rho=0.50,theta=np.pi/100, threshold=50,lines=np.array([]), minLineLength=40)[0]
    edges = cv2.Canny(localImg,10,10,apertureSize = 3)
    lines = cv2.HoughLinesP(edges,rho=2,theta=np.pi/100,threshold=10,\
                            minLineLength=60,maxLineGap=0)
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        print "X1: ", x1
        print "Y1: ", y1
        print "X2: ", x2
        print "Y2: ", y2
        print "-------------------"
        #for i in States:
        #    if(x1 - i.coord_x  < 50):
        #        print "State x Coord: ", i.coord_x
        #        print" WE TOUCHIN TIPS"
        #        print "-------------------"
                    
        
def main():
    img = cv2.imread(filename)
        
    findCircles(img)
    findStateLabels(img)
    findStart(img)
    findLines(img)
    
    cv2.imwrite('output.png',img)
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
	main()
