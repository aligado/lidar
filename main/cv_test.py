import cv2
import numpy as np

if __name__ == '__main__':
    image_content = np.zeros((1280, 720, 3), np.uint8)
    print('frame_draw')
    cv2.imshow('cvdraw', image_content)
    for index, x in enumerate(xdata):
        y = ydata[index]
        x += 2000
        y += 1000
        x = 1280*x/4000
        y = 720*y/2000
        image_content[ y:y+1, x:x+1] = (0, 0, 255)
