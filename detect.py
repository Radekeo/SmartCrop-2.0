import cv2
import matplotlib.pyplot as plt
import cvlib


def Detect():
    img_path = 'images/test.jpg'
    im  =  cv2.imread (img_path)
    h, w, __ = im.shape
    bbox , label , conf  =  cvlib.detect_common_objects(im)
    dimensions = (w,h)
    return bbox[0], dimensions
