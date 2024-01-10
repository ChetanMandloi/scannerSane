import numpy as np
import matplotlib.pyplot as plt
import cv2

img = cv2.imread("150DPI.png")


def find_shape(approx):
    x, y, w, h = cv2.boundingRect(approx)
    if len(approx) == 3:
        s = "Triangle"

    elif len(approx) == 4:
        calculation = w / float(h)
        if calculation >= 0.95:
            s = "Square"
        else:
            s = "Rectangle"

    elif len(approx) == 5:
        s = "Pentagon"
    elif len(approx) == 6:
        s = "Hexagon"
    elif len(approx) == 8:
        s = "Octagon"

    else:
        s = "Circle"

    return s, x, y, w, h
def get_contours(img, img_contour):
  contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

  for cnt in contours:
    area = cv2.contourArea(cnt)
    if area > 9000:
      cv2.drawContours(img_contour, cnt, -1, (255, 0, 255), 1)

      # Find length of contours
      param = cv2.arcLength(cnt, True)

      # Approximate what type of shape this is
      approx = cv2.approxPolyDP(cnt, 0.01 * param, True)
      shape, x, y, w, h = find_shape(approx)
      cv2.putText(img_contour, shape, (x+78, y+200), cv2.FONT_HERSHEY_COMPLEX, .7, (255, 0, 255), 1)
      cv2.rectangle(img_contour, (x-10, y-10), (x + w + 10, y + h + 10), (255, 0, 0), 2)

  return approx, param, img_contour, contours, cnt

img_contour = img.copy()

img_blur = cv2.GaussianBlur(img, (7, 7), 1)
img_gray = cv2.cvtColor(img_blur, cv2.COLOR_BGR2GRAY)
img_canny = cv2.Canny(img_gray, 70, 270)
kernel = np.ones((3))
img_dilated = cv2.dilate(img_canny, kernel, iterations=1)
black = np.zeros((img.shape[0], img.shape[1]))
get_contours(img_dilated, black)

cv2.namedWindow("img", cv2.WINDOW_NORMAL)
cv2.resizeWindow("img", 900, 900)
cv2.imshow("img", black)
cv2.waitKey()