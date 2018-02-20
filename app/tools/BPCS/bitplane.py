import numpy as np
import cv2

def countChanges(bitplane):
    count=0
    for i in range(8):
        for j in range(8):
            if i<7 and bitplane.img.item(i,j,bitplane.color)!=bitplane.img.item(i+1,j,bitplane.color):
                count+=1
            if j<7 and bitplane.img.item(i,j,bitplane.color)!=bitplane.img.item(i,j+1,bitplane.color):
                count+=1
    return count

def isNoiseLike(bitplane, threshold):
    k=countChanges(bitplane)
    if k/112>threshold:
        return True
    else:
        return False