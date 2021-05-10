import cv2
import time
import helpers
import numpy as np
import tensorflow as tf
from tf_bodypix.api import download_model, load_model, BodyPixModelPaths


# External camera value is 0

WEB_CAM_DESCRIPTOR = 0

video = cv2.VideoCapture(WEB_CAM_DESCRIPTOR)

bodypix_model = load_model(download_model(
    BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16
))


while True: 

  check, frame = video.read()
  image_array = tf.keras.preprocessing.image.img_to_array(frame)
  result = bodypix_model.predict_single(image_array)
  mask = result.get_mask(threshold=0.75)
  fg_mask = mask.numpy().astype(np.uint8)
  fg = frame * fg_mask
  cv2.imshow("Webcam view", fg)
  key = cv2.waitKey(1)

  if key == ord('q'):
    break 

video.release()
cv2.destroyAllWindows()
