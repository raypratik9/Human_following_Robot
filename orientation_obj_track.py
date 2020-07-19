import numpy as np
import cv2
import socket
import sys
import math
try:
    s = socket.socket()#socket.AF_INET, socket.SOCK_STREAM)
    print ("Socket successfully created")
except socket.error as err:
    print ("Socket creation failed %s" %(err))
port = 2000

try:
    host_ip = socket.gethostbyname(socket.gethostname())
except socket.gaierror:
    print("There was a erroe")
    sys.exit();
s.bind((host_ip,port))
print(host_ip);

s.listen(5)
print("listening")
Server, addr = s.accept()      
print ('Got connection from', addr)

cap = cv2.VideoCapture(0)
cap2 = cv2.VideoCapture(1)
def nothing(x):
    pass

# Create a black image, a window
cv2.namedWindow('image')

# create trackbars for color change
cv2.createTrackbar('Rl','image',77,255,nothing)
cv2.createTrackbar('Gl','image',92,255,nothing)
cv2.createTrackbar('Bl','image',71,255,nothing)
cv2.createTrackbar('Rh','image',110,255,nothing)
cv2.createTrackbar('Gh','image',254,255,nothing)
cv2.createTrackbar('Bh','image',255,255,nothing)
cv2.createTrackbar('i','image',0,1000,nothing)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret2, frame2 = cap2.read()
    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rl = cv2.getTrackbarPos('Rl','image')
    gl = cv2.getTrackbarPos('Gl','image')
    bl = cv2.getTrackbarPos('Bl','image')
    rh = cv2.getTrackbarPos('Rh','image')
    gh = cv2.getTrackbarPos('Gh','image')
    bh = cv2.getTrackbarPos('Bh','image')
    i = cv2.getTrackbarPos('contour','image')
    # Display the resulting frame
    blur3 = cv2.medianBlur(frame,5)
    blur2 = cv2.medianBlur(frame2,5)
    #ret,thresh=cv2.findContours(blur3,127,255,0)
    lower=np.array([rl, gl, bl])
    upper=np.array([rh,gh, bh])
    frame_HSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    frame_HSV2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2HSV)
    #for blue color detection
   # Low=np.array([100,50,50])
   # High=np.array([140,255,255])
   # Image=cv2.inrange(frame_HSV,low,high) #check for range of low and high
    #ret,thresh1 = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
    #ret,thresh2 = cv2.threshold(frame,127,255,cv2.THRESH_BINARY_INV)
    #ret,thresh3 = cv2.threshold(frame,127,255,cv2.THRESH_TRUNC)
    #ret,thresh4 = cv2.threshold(frame,127,255,cv2.THRESH_TOZERO)
    #ret,thresh5 = cv2.threshold(frame,127,255,cv2.THRESH_TOZERO_INV)
    frame_threshold = cv2.inRange(frame_HSV, lower, upper)
    frame_threshold2 = cv2.inRange(frame_HSV2, lower, upper)
    contours,hierarchy=cv2.findContours(frame_threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    contours2,hierarchy2=cv2.findContours(frame_threshold2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    #cv2.drawContours(frame,contours,-1,(0,255,0),3)
    cv2.drawContours(frame_threshold,contours,-1,(0,255,0),3)
    
    if len(contours)>0:   #to return number of contours detected
        lencontour=len(contours[0])
        cn=contours[0]
        lencontour2=len(contours2[0])
        cn2=contours2[0]
        for cnt in contours:
            if(lencontour<len(cnt)):
                lencontour=len(cnt)
                cn=cnt
        for cnt2 in contours2:
            if(lencontour2<len(cnt2)):
                lencontour2=len(cnt2)
                cn2=cnt2
        M = cv2.moments(cn)
        M2 = cv2.moments(cn2)
        a,b,c,d = cv2.boundingRect(cn)
        if M['m00']>0:
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            cx2 = int(M2['m10']/M2['m00'])
            cy2 = int(M2['m01']/M2['m00'])
            y_new=((cx-cx2-70))
            #print((y_new),cx-cx2)
            if(y_new<-500 or y_new>500):
                y_new=0
            #x_new=cal(cx,0,600,-300,300)
            x_new = -0.5*(cx - (frame.shape[1] / 2))
           
            #y_new=cal(cy,0,460,-300,300)
            x_new=int(x_new)
            #y_new=2*(int(y_new))
            #print ("cx= "+)
            #print(contours)
            #print ("cy")
            #print(cy)
            #cv2.putText(frame,str(x_new),(cx,cy),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1, cv2.LINE_AA)
            #cv2.putText(frame,",",(cx+55,cy),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1, cv2.LINE_AA)
            #cv2.putText(frame,str(y_new),(cx+57,cy),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1, cv2.LINE_AA)
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            #cv2.putText(frame,str(W),(CX,CY),cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 1, cv2.LINE_AA)
            #cv2.line(frame,(a,b),(a,b+d),(0,255,0),8)
            #cv2.line(frame,(a+c,b),(a+c,b+d),(0,255,0),8)
            #cv2.circle(frame,center,radius,(0,255,0),2)
            cv2.circle(frame,(cx,cy), 5, (255,0,0), -1)
            cv2.rectangle(frame,(a,b),(a+c,b+d),(0,0,255),1)
    sf = 1
    sf1=0.8
    s2 = sf * (-0.33 * x_new + 0.58 * y_new + 0.33 * W)
    s3 = sf1 * (-0.33 * x_new - 0.58 * y_new + 0.33 * W)
    s1 = sf * (0.67 * x_new + 0 * y_new + 0.33 * W)
    #area = cv2.contourArea(cn)     #area
    #perimeter = cv2.arcLength(cn,True)     #perimeter
    #epsilon = 0.1*cv2.arcLength(cn,True)
    #approx = cv2.approxPolyDP(cn,epsilon,True)
    #hull = cv2.convexHull(points[, hull[, clockwise[, returnPoints]]
    #hull = cv2.convexHull(cn)
    #k = cv2.isContourConvex(cn)
    mystring=str(s1)+","+str(s2)+','+str(s3)+'*'
    b = bytes(mystring, 'utf-8')
    Server.send(b)
    cv2.imshow('frame',frame)
    #cv2.imshow('thresh1',thresh1)
    #cv2.imshow('thresh2',thresh2)
    #cv2.imshow('thresh3',thresh3)
    #cv2.imshow('thresh4',thresh4)
    #cv2.imshow('blur3',blur3)
    #cv2.circle(frame,(, 5, (0,255,0), -1)
    cv2.imshow('frame_threshold',frame_threshold)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
exit(0)
