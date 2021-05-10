"""A collection of commonly used helper functions. 

@author: <rbm@cmu.edu>
@date: 05/08/21
"""
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

def load_img(relative_path):
	"""Returns an image as a normalized numpy array.

	Args:
		relative_path (string): path to some image.

	Returns:
		ndarray: image as 2d ndarry
	"""
	if relative_path == None: 
		raise AssertionError("load_img called with a null path.")

	if not os.path.isfile(relative_path):
		raise AssertionError("load_img called on a malformed input: {}".format(relative_path))

	img = cv2.imread(relative_path)

	img = np.float32(img) / 255

	return img

def plt_img(img):
	"""Plots an image in a pyplot

	Args:
		img (ndarray): a 2d grayscale image
	"""

	plt.imshow(img)
	plt.show()

	return