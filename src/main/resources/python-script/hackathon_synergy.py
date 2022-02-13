#!sudo apt install tesseract-ocr
#!pip install pytesseract

import cv2
import pytesseract
import numpy as np
import os
import argparse
import sys

# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'



# parser = argparse.ArgumentParser()
# parser.add_argument('--imgpath', type=str, default='')
# args = parser.parse_args()
imgpath = sys.argv[1]


###################### please load your aadhar image system path here inside imread ######################################
# im = cv2.imread("/home/nikunj/Documents/spring projects/hackathon/target/classes/static/image/WhatsApp Image 2022-02-12 at 8.44.01 PM.jpeg")
im = cv2.imread(imgpath)
im = cv2.resize(im, (540,400))

BKG_THRESH = 40
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(1,1),0)
img_h, img_w = np.shape(im)[:2]
bkg_level = gray[int(img_h/100)][int(img_w/2)]
#thresh_level = bkg_level + BKG_THRESH
thresh_level = 115

retval, thresh = cv2.threshold(blur,thresh_level,255,cv2.THRESH_BINARY)
#cv2_imshow(thresh)

CARD_MAX_AREA = 0.81 * img_h * img_w
CARD_MIN_AREA = 0.25 * img_h * img_w


def find_cards(thresh_image):
    """Finds all card-sized contours in a thresholded camera image.
    Returns the number of cards, and a list of card contours sorted
    from largest to smallest."""

    # Find contours and sort their indices by contour size
    cnts,hier = cv2.findContours(thresh_image,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    index_sort = sorted(range(len(cnts)), key=lambda i : cv2.contourArea(cnts[i]),reverse=True)

    # If there are no contours, do nothing
    if len(cnts) == 0:
        return [], []
    
    # Otherwise, initialize empty sorted contour and hierarchy lists
    cnts_sort = []
    hier_sort = []
    cnt_is_card = np.zeros(len(cnts),dtype=int)

    # Fill empty lists with sorted contour and sorted hierarchy. Now,
    # the indices of the contour list still correspond with those of
    # the hierarchy list. The hierarchy array can be used to check if
    # the contours have parents or not.
    for i in index_sort:
        cnts_sort.append(cnts[i])
        hier_sort.append(hier[0][i])

    # Determine which of the contours are cards by applying the
    # following criteria: 1) Smaller area than the maximum card size,
    # 2), bigger area than the minimum card size, 3) have no parents,
    # and 4) have four corners

    for i in range(len(cnts_sort)):
        size = cv2.contourArea(cnts_sort[i])
        peri = cv2.arcLength(cnts_sort[i],True)
        approx = cv2.approxPolyDP(cnts_sort[i],0.01*peri,True)
        
        if ((size < CARD_MAX_AREA) and (size > CARD_MIN_AREA) and (hier_sort[i][3] == -1) and (len(approx) == 4)):
            cnt_is_card[i] = 1

    return cnts_sort, cnt_is_card

cnts_sort, cnt_is_card = find_cards(thresh)


temp = im.copy()
temp = cv2.drawContours(temp, cnts_sort, 0, (0,255,0), 1)

def flattener(image, pts, w, h):
    """Flattens an image of a card into a top-down 200x300 perspective.
    Returns the flattened, re-sized, grayed image.
    See www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/"""
    temp_rect = np.zeros((4,2), dtype = "float32")
    
    s = np.sum(pts, axis = 2)

    tl = pts[np.argmin(s)]
    br = pts[np.argmax(s)]

    diff = np.diff(pts, axis = -1)
    tr = pts[np.argmin(diff)]
    bl = pts[np.argmax(diff)]

    # Need to create an array listing points in order of
    # [top left, top right, bottom right, bottom left]
    # before doing the perspective transform

    if w >= 1.2*h: # If card is vertically oriented
        temp_rect[0] = tl
        temp_rect[1] = tr
        temp_rect[2] = br
        temp_rect[3] = bl

    if w <= 0.8*h: # If card is horizontally oriented
        temp_rect[0] = bl
        temp_rect[1] = tl
        temp_rect[2] = tr
        temp_rect[3] = br

    # If the card is 'diamond' oriented, a different algorithm
    # has to be used to identify which point is top left, top right
    # bottom left, and bottom right.
    
    if w > 0.8*h and w < 1.2*h: #If card is diamond oriented
        # If furthest left point is higher than furthest right point,
        # card is tilted to the left.
        if pts[1][0][1] <= pts[3][0][1]:
            # If card is titled to the left, approxPolyDP returns points
            # in this order: top right, top left, bottom left, bottom right
            temp_rect[0] = pts[1][0] # Top left
            temp_rect[1] = pts[0][0] # Top right
            temp_rect[2] = pts[3][0] # Bottom right
            temp_rect[3] = pts[2][0] # Bottom left

        # If furthest left point is lower than furthest right point,
        # card is tilted to the right
        if pts[1][0][1] > pts[3][0][1]:
            # If card is titled to the right, approxPolyDP returns points
            # in this order: top left, bottom left, bottom right, top right
            temp_rect[0] = pts[0][0] # Top left
            temp_rect[1] = pts[3][0] # Top right
            temp_rect[2] = pts[2][0] # Bottom right
            temp_rect[3] = pts[1][0] # Bottom left
            
        
    maxWidth = img_w
    maxHeight = img_h

    # Create destination array, calculate perspective transform matrix,
    # and warp card image
    dst = np.array([[0,0],[maxWidth-1,0],[maxWidth-1,maxHeight-1],[0, maxHeight-1]], np.float32)
    M = cv2.getPerspectiveTransform(temp_rect,dst)
    warp = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    warp = cv2.cvtColor(warp,cv2.COLOR_BGR2GRAY)

        

    return warp

def preprocess_card(contour, image):
    peri = cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour,0.01*peri,True)
    pts = np.float32(approx)
    corner_pts = pts

    # Find width and height of card's bounding rectangle
    x,y,w,h = cv2.boundingRect(contour)
    width, height = w, h

    # Find center point of card by taking x and y average of the four corners.
    average = np.sum(pts, axis=0)/len(pts)
    cent_x = int(average[0][0])
    cent_y = int(average[0][1])
    center = [cent_x, cent_y]

    # Warp card into 200x300 flattened image using perspective transform
    warp = flattener(image, pts, w, h)

    return warp


warp = preprocess_card(cnts_sort[0],im)

#from google.colab.patches import cv2_imshow
#cv2_imshow(im)
#cv2_imshow(gray)
#cv2_imshow(blur)
#cv2_imshow(thresh)
#cv2_imshow(temp)
#cv2_imshow(warp)


start = (int(0.31*img_w),int(0.28*img_h))
end = (int(0.5*img_w),int(0.37*img_h))
name = warp.copy()
name = cv2.rectangle(name, start, end, (255,0,0), 1)

start = (int(0.56*img_w),int(0.36*img_h))
end = (int(0.75*img_w),int(0.45*img_h))
name = cv2.rectangle(name, start, end, (255,0,0), 1)

start = (int(0.39*img_w),int(0.43*img_h))
end = (int(0.47*img_w),int(0.52*img_h))
name = cv2.rectangle(name, start, end, (255,0,0), 1)

start = (int(0.29*img_w),int(0.75*img_h))
end = (int(0.71*img_w),int(0.86*img_h))
name = cv2.rectangle(name, start, end, (255,0,0), 1)

#cv2_imshow(name)
cropped = warp[int(0.28*img_h):int(0.37*img_h),(int(0.31*img_w)):(int(0.5*img_w))]
#cv2_imshow(cropped)
text = pytesseract.image_to_string(warp)
meta_data = text.split("\n")
#print(text)

import re
A_ID = "None"
regex = ("[0-9]{3,}[\\s]+[0-9]{4}[\\s]+[0-9]{2,}")
p = re.compile(regex)
for i in meta_data:
  z=re.findall(p,i)
  if(len(z)):
    z=sorted(z)
    #print(z[-1])
    A_ID = z[-1]
print(A_ID)

dob="None"
dob_in = 0
regex = ("[0-9]+[/][0-9]+[/][0-9]+")
p = re.compile(regex)
for idx,i in enumerate(meta_data):
  z = re.findall(p,i)
  if(len(z)):
    z=sorted(z)
    #print(z[-1])
    dob = z[-1]
    dob_in=idx
print(dob)


regex = ("[A-Za-z]+[\\s][A-Za-z]+")
p = re.compile(regex)
name = "None"
for idx,i in enumerate(meta_data):
  z = re.findall(p,i)
  if(len(z)):
    if idx == dob_in - 1:
      z=sorted(z)
      #print(z[-1])
      name = z[-1]
print(name)

gender = "None"
for idx,i in enumerate(meta_data):
  i = i.lower()
  if idx == dob_in + 1:
    if "female" in i:
      gender = "female"
    elif "male" in i:
      gender = "male"
print(gender)


# print(A_ID, dob, name, gender)
#return A_ID, dob, name, gender

'''
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--imgpath', type=str, default='')
    args = parser.parse_args()
    #args.imgpath
'''
