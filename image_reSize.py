import cv2

image = cv2.imread('test1.jpg')
h, w, channels = image.shape

if (w > h):
    image = cv2.resize(image, (300, int(300*h/w)), interpolation=cv2.INTER_AREA)
else:
    image = cv2.resize(image, (int(300*w/h), 300), interpolation=cv2.INTER_AREA)

cv2.imwrite('test1_.jpg', image)