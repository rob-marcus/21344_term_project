import cv2
import time
import helpers
import numpy as np
from math import ceil, pi
import tensorflow as tf
from tf_bodypix.api import download_model, load_model, BodyPixModelPaths
from scipy import signal    # For signal.gaussian function
from scipy.ndimage import gaussian_filter
def gaussian(sigma):
  """Returns a proper sq. gaussian with length 2 * ceil(3 * sigma) + 1

  Args:
      sigma (float): A positive scalar value, typically between 0.5 and 2 

  Returns:
      a 2d ndarray that has been averaged out (i.e., the maximum value is 
      not normalized to 1.)
  """
  h = 2 * ceil(3 * sigma) + 1
  gaussian_row = signal.gaussian(h, sigma)

  #3d_gaussian = np.zeros_like((2d_gaussian.shape[0], 2d_gaussian.shape[1], 3))

  #3d_gaussian[:, :, 0]
  return np.outer(gaussian_row, gaussian_row.T)/(2*pi*(sigma**2))

def convolve2d(img0, h, debug=False):
  """q3.1. Convolves an image with a given convolution filter. 

  Args:
      img0 (np.ndarray): a greyscale image imported as a numpy array
      h (np.ndarray): a kernel with odd length/width
      debug (bool): optional parameter that will enable debug printing
                     if any prints are made.    
  Returns: 
      g as specified by the definition of filtering as convolution: 
      `(f * g)(x, y) = Sum_{i, j} f(i, j)I(x - i, y - j)`
      where g is the filtered image, and I is the input image. 
  """
  assert(type(img0) == np.ndarray)
  assert(type(h) == np.ndarray)

  # First must pad the image so we can apply the kernel in edges. 
  # I'm not sure if the filter is a square, so just to be safe, we will say
  # that the minimum padding is defined by maximum(h.shape)//2.
  pad_width = max(h.shape)//2
  padded_img = np.pad(img0, pad_width, mode="edge")

  # This is a helpful numpy function I discovered which iterates a sliding window
  # for you. I implemented this by hand initially in a repl, but discovered this 
  # while playing around with ndenumerate and np.fromiter/vectorize. It's a lot 
  # cleaner, so I'm going with it instead. 
  windows = np.lib.stride_tricks.sliding_window_view(padded_img, h.shape)

  # This yields a 4d list of windows
  res = windows * h
  # We want a 2d list however. 
  res_3d = np.sum(res, 3)
  res_2d = np.sum(res_3d, 2)

  if debug: 
      dbg_helpers.cmp_imgs_h(img0, res_2d)
      dbg_helpers.plt_img(res_2d)

  return res_2d



# External camera value is 0

WEB_CAM_DESCRIPTOR = 0

video = cv2.VideoCapture(WEB_CAM_DESCRIPTOR)

bodypix_model = load_model(download_model(
    BodyPixModelPaths.MOBILENET_FLOAT_50_STRIDE_16
))


kernel = gaussian(2.5)

while True: 

  check, frame = video.read()
  image_array = tf.keras.preprocessing.image.img_to_array(frame)
  result = bodypix_model.predict_single(image_array)
  mask = result.get_mask(threshold=0.5)
  fg_mask = mask.numpy().astype(np.uint8)
  fg = frame * fg_mask
  bg = frame - fg

  #blurred_bg = signal.fftconvolve(bg, kernel[:, :, np.newaxis], mode="same")
  blurred_bg = gaussian_filter(bg, sigma=(5, 5, 0))
  cv2.imshow("Webcam view", blurred_bg + fg)

  key = cv2.waitKey(1)

  if key == ord('q'):
    break 

video.release()
cv2.destroyAllWindows()
