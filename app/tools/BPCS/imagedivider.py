import numpy as np
import cv2

def divide(img):
    height, width = img.shape[:2]
    print("%d and %d" % (width, height))
    
    x=0
    y=0
    
    if height%8!=0:
        y += 8-height%8
    if width%8!=0:
        x += 8-width%8
    
    bordered = cv2.copyMakeBorder(img, top=0, bottom=y, left=0, right=x, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])
    
    height1, width1 = bordered.shape[:2]
    print("%d and %d" % (width1, height1))
    
    p = int(width1/8)
    q = int(height1/8)
    
    crop_img = [[0 for a in range(p)] for b in range(q)]
    for i in range(q):
        for j in range(p):
            print("%d and %d" % ((i+1)*8, (j+1)*8))
            crop_img[i][j] = bordered[i*8:(i+1)*8, j*8:(j+1)*8]
            #KALAU MAU NGETES GAMBARNYA KYK GIMANA BUKA AJA UNCOMMENT LINES DI BAWAH
            #cv2.imshow("image",crop_img[i][j])
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            
            #CONTOH MANIPULASI GAMBARNYA (per pixel per warna) DI BAWAH SINI! (bikin fungsi baru aja kalau nanti ada yg mau bikin)
            for k in range(8):
                for l in range(8):
                    #crop_img.item buat ngambil nilai pixel, k,l koordinat, 0 untuk B, 1 untuk G, 2 untuk R. itemset buat set nilai pixel
                    crop_img[i][j].itemset((k,l,0),int(crop_img[i][j].item(k,l,0)/2))
                    crop_img[i][j].itemset((k,l,1),int(crop_img[i][j].item(k,l,1)/2))
                    crop_img[i][j].itemset((k,l,2),int(crop_img[i][j].item(k,l,2)/2))
                    #crop_img berisi image 8x8
            
    
    cv2.imshow("image",bordered)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return bordered
    

image = cv2.imread("../../../file/input/medium_image/test.jpeg")
cropped_image = divide(image)    