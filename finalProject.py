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
StatePairs = []
height = 0 
width = 0

#filename = raw_input("Please state the file you want to use: ")
filename = "TestWeb.png"
def findCircles(img):
    gray = cv2.imread(filename,0)
    circles = cv2.HoughCircles(gray,cv.CV_HOUGH_GRADIENT,1,20,param1=50,param2=50,minRadius=10,maxRadius=0)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        squarePair = []
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
        squarePair.append(i[0])
        squarePair.append(i[1])
        state = State(None, i[0], i[1], False, False, i[2], 2*i[2]*np.pi);
        #States.append(state)
        squarePair.append(i[2]*math.sqrt(2))
        print "SQUARE PAIR: ", squarePair
        #circleOCRBoundingBox.append(squarePair)
        print "BOUNDING BOX: ", circleOCRBoundingBox
        state.label = findStateLabel(img, squarePair)
        States.append(state) 
        sqaurePair = []
        #print "SQUARE PAIR: ", squarePair
        circleOCRBoundingBox.append(squarePair)
        #print "BOUNDING BOX: ", circleOCRBoundingBox
    val = float("inf")
    for circle in States:
        if circle.circumference < val:
            val = circle.circumference
    for circle in States:
        if circle.circumference == val:
            circle.final = True

def findStateLabel(baseImage, circleOCRBoundingBox):
    
    gray = cv2.imread(filename,0)
    #gray = img
                       
    idx = 0
    #for i in circleOCRBoundingBox:
    idx += 1
    point1 = []
    point2 = []
    
    x1 = math.floor(circleOCRBoundingBox[0])
    y1 = math.floor(circleOCRBoundingBox[1]-(circleOCRBoundingBox[2]/2))
    x2 = math.floor(circleOCRBoundingBox[0]+(circleOCRBoundingBox[2]/2))
    y2 = math.floor(circleOCRBoundingBox[1]+(circleOCRBoundingBox[2]/2))
    point1.append(x1)
    point1.append(y1)
    
    point2.append(x2)
    point2.append(y2)

    cv2.rectangle(baseImage,(int(x1),int(y1)),(int(x2),int(y2)),(0,0,255),1)
    #uncomment to draw rectangle
    
    roi = gray[y1:y2, x1:x2]
    cv2.imwrite('1.png', roi)
    thresher= cv2.imread('1.png')
    ret,thresh1 = cv2.threshold(thresher,128,255,cv2.THRESH_BINARY)
    cv2.imwrite( '1.png', thresh1)
        
    image_file = '1.png'


#    im = Image.open(image_file), config='-psm 10000')
    #im.filter(ImageFilter.SHARPEN)
    #print ("here is the supposed image")
    #print im
    number = 0
    number = pt.image_to_string(Image.open(image_file), config='-psm 6')
    
    print "=====Label======="
    if(number == "l"):
        number = 1
    elif(number == "S" or number == "s"):
        number = 5
    elif(number == None or number == ""):
        number = 0
    else:
        number = extract_num(number)
    print "=====Label=======\n"
    it = pt.image_to_string(Image.open(image_file), config='-psm 10000')
    #print "=====Label======="
    #print (it)
    #print "=====Label=======\n"
    
    print (number)
    return number
    
def findTriangle(img):
    localImg = cv2.imread(filename,0)
    ret,thresh = cv2.threshold(localImg,127,255,1)
    contours,h = cv2.findContours(thresh,1,2)
   
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        if len(approx)==3:
            #print "triangle"
            cv2.drawContours(img,[cnt],0,(0,255,0),-1)

            #print "1st field: ", cnt[0], "2nd field : ", cnt[1], "3rd Field: ", cnt[2], "4th field: ", cnt[3], "5th field: ", cnt[4]
            #print "Ret : ", ret
            triangleTipY = approx[1][0][1]
            triangleTipX = approx[1][0][0]
            return triangleTipY, triangleTipX
            
def findStart(img):
    localImg = cv2.imread(filename,0)
    triangleTipY, triangleTipX = findTriangle(img)
    comparisonStates = []
    for state in States:
        #print " Y COORD: ", state.coord_y, "X COORD: ", state.coord_x, "and THE JUST THE TIP Y + 2: ", triangleTipY
        if(state.coord_y <=  triangleTipY + 2 and state.coord_y >= triangleTipY - 2):
            comparisonStates.append(state)

    x = comparisonStates[0].coord_x
    initialState = ''
    for state in comparisonStates:
        if(state.coord_x >= triangleTipX):
            if(state.coord_x <= x):
                x = state.coord_x
                initialState = state
#    print initialState.coord_x, initialState.coord_y
    for state in States:
        if(initialState.coord_x == state.coord_x and initialState.coord_y == state.coord_y):
            #print state.coord_x, state.coord_y
            state.initial = True
            cv2.circle(img,(state.coord_x,state.coord_y),state.radius,(255,0,0),2)
    #for i in States:
        #print i.coord_x, i.coord_y, i.initial

def findLines(img):
    global StatePairs
    localImg = cv2.imread(filename,0)
    print "height: ", height
    print "width: ", width
    edges = cv2.Canny(localImg,50,150,apertureSize = 3)
    lines = cv2.HoughLinesP(image=edges,rho=0.50,theta=np.pi/100, threshold=50,lines=np.array([]), minLineLength=40)[0]
    state = ""
    
    print "Lines: ",lines
    for x1,y1,x2,y2 in lines:
        pair = []
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)
        lengthAB = math.sqrt(((x1-x2)**2)+((y1-y2)**2))

        newPointx1 = (x1+(x1-x2)/(lengthAB*.2))
        newPointy1 = (y1+(y1-y2)/(lengthAB*.2))

        newPointx2 = (x2+(x2-x1)/(lengthAB*.2))
        newPointy2 = (y2+(y2-y1)/(lengthAB*.2))

        
        print "checking: ",x1, y1, x2 , y2
        #print "newPointx1: ", newPointx1
        #print "newPointy1: ", newPointy1

        print "newPointx2: ", newPointx2
        print "newPointy2: ", newPointy2

        flag1 = False
        flag2 = False
        while(flag1 == False):
            print "newPointx1: ", newPointx1
            print "newPointy1: ", newPointy1
            state, flag1 = inState(newPointx1, newPointy1)
            newPointx1, newPointy1 = calculateNewPoint1(newPointx1,newPointy1, x1, y1)
            cv2.line(img,(int(newPointx1),int(newPointy1)),(x2,y2),(255,0,0),2)
            print ("newX1" , newPointx1, "newY1" , newPointy1)
            if(flag1 == True):
                pair.append(state)
                print "pair:################################## ", pair
            if( not( isInImage(width,height,newPointx1, newPointy1))):
                pair.append("")
                flag1 = True
                
        
        while(flag2 == False):
            print "Started from the bottom"
            state, flag2 = inState(newPointx2, newPointy2)
            newPointx2, newPointy2 = calculateNewPoint2(newPointx2,newPointy2, x2, y2)

            cv2.line(img,(x1,y1),(int(newPointx2),int(newPointy2)),(0,0,255),2)
            cv2.imwrite( 'lalalalala.png', img)
            if(flag2 == True):
                pair.append(state)
                print "pair: ", pair
            if( not( isInImage(width,height,newPointx2, newPointy2))):
                pair.append("")
                flag2 = True
                                #if(pair[0] == "" or pair[1] == ""):
         #   continue
        #else:
        StatePairs.append(pair)
        

def inState(x,y):
    global States
    if(isInImage(width,height,x,y)):
        for state123 in States:
            print "state coordx: " , state123.coord_x
            print "state coordy: " , state123.coord_y
            
            deltax = state123.coord_x - x
            deltax = pow(deltax, 2)
            #print "deltax_point1: " , deltax
            
            deltay = state123.coord_y - y
            deltay = pow(deltay, 2)
            #print "deltay: " , deltay

            radius = state123.radius
            sqrtdxdy = math.sqrt(deltax + deltay)
            print("sqrt: ", sqrtdxdy, "raidus: " , radius)
        
            if(sqrtdxdy <= radius):
                #if state123.label == None:
                #    state123.label = str(0)
                return state123.label, True

            #else:
             #   print ("quiting in the return of inState")
             #   return "", False
    return "" , False    

def calculateNewPoint1(newPointx, newPointy, x1, y1):
    lengthAB = math.sqrt(((x1-newPointx)**2)+((y1-newPointy)**2))
    newX = (newPointx+(newPointx-x1)/(lengthAB*.2))
    newY = (newPointy+(newPointy-y1)/(lengthAB*.2))
    return newX, newY

    
def calculateNewPoint2(newPointx, newPointy, x2, y2):
    lengthAB = math.sqrt(((x2-newPointx)**2)+((y2-newPointy)**2))
    newX = (newPointx+(newPointx-x2)/(lengthAB*.2))
    newY = (newPointy+(newPointy-y2)/(lengthAB*.2))
    return newX, newY


def isInImage(width,height,x,y):
    print( "widht: ", width, "height: ", height)
    if(x > width):
        print "not in image: out of bounds right"
        return False
    if(y > height):
        print "not in image: out of bounds bottom"
        return False
    if(x < 0):
        print "not in image: out of bounds left"
        return False
    if(y < 0):
        print "not in image: out of bounds top"
        return False
    else:
        return True


def extract_num(input_str):
    if input_str is None or input_str == '':
        return 0
    
    out_number = ''
    for ele in input_str:
        if ele.isdigit():
            out_number += ele
            return int(out_number) 

def cropLines(pairs , img):
    global States
    leftCenter, rightCenter = (0,0)
    for left, right in pairs:
        for state in States:
            if (state.label  == left):
                leftCenter = (state.coord_x , state.coord_y)
                print "leftCenter: ", leftCenter
            if (state.label  == right):
                rightCenter = (state.coord_x , state.coord_y)
                print "rightCenter: ", rightCenter
#        createLineCropping(leftCenter, rightCenter, img)
                
#def createLineCropping(leftCenter, rightCenter, img):
#    roi = img[leftCenter[0]:leftCenter[, x1:x2]
#        cv2.imwrite('1.png', roi)
                
                
def main():
    global height, width, StatePairs
    img = cv2.imread(filename)
    imgTaco = cv2.imread(filename,0)
    height, width = imgTaco.shape
    findCircles(img)
    #findStateLabels(img)
    findStart(img)
    findLines(img)
    cropLines(StatePairs , img)
    for i in States:
        print i.label, i.coord_x, i.coord_y, i.initial, i.final, i.radius
        print "hello"
    cv2.imwrite('output.png',img)
    cv2.destroyAllWindows()
    for i in range (len(StatePairs)):
        print StatePairs[i]

if __name__ == "__main__":
	main()
