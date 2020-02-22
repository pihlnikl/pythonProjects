import cv2 as cv
import numpy as np


im = cv.imread(
    "source", cv.IMREAD_GRAYSCALE)
font = cv.FONT_HERSHEY_DUPLEX


thresh = cv.threshold(im, 150, 255, cv.THRESH_BINARY)[1]
contours, _ = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)


for cnt in contours:
    approx = cv.approxPolyDP(cnt, 0.01*cv.arcLength(cnt, True), True)
    cv.drawContours(im, [approx], 0, (0), 5)
    x = approx.ravel()[0]
    y = approx.ravel()[1]
    if len(approx) == 3:
        cv.putText(im, "Triangle", (x, y), font, 1, (0))

    elif len(approx) == 4:
        (x, y, w, h) = cv.boundingRect(approx)
        ar = w / float(h)
        shape = "Square" if ar >= 0.95 and ar <= 1.05 else "Rectangle"
        cv.putText(im, shape, (x, y), font, 1, (0))

    elif len(approx) == 5:
        cv.putText(im, "Pentagon", (x, y), font, 1, (0))

    elif len(approx) == 6:
        cv.putText(im, "Hexagon", (x, y), font, 1, (0))

    else:
        cv.putText(im, "Circle", (x, y), font, 1, (0))

cv.imwrite('contours2.jpg', im)