import cv2
import time

# External camera value is 0

WEB_CAM_DESCRIPTOR = 0

video = cv2.VideoCapture(WEB_CAM_DESCRIPTOR)

while True: 

  check, frame = video.read()

  cv2.imshow("Webcam view", frame)

  key = cv2.waitKey(1)

  if key == ord('q'):
    break 

video.release()
cv2.destroyAllWindows()