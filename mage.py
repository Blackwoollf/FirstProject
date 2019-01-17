import cv2


def Erode(mask):
    poisk = cv2.erode(mask, None, iterations=2)
    cv2.imshow('poisk', poisk)
    return poisk
