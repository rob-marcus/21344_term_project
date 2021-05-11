"""The background class and associated functions. 

@author: <rbm@cmu.edu>
@date: 05/08/21
"""
from constants import IMG_EXTS, bodypix_model
import glob
import helpers
import os
import skimage.transform
import tensorflow as tf
import numpy as np
from scipy.ndimage import gaussian_filter

class VirtualEffect():
  def __init__(self, virtual_path):
    self.virtual_path = virtual_path
    
    # These values will be set by get_virtual_imgs if 
    # virtual_path is non-null.
    self.current_img_idx = None
    self.num_imgs = None
    self.virtual_imgs = None
    self.virtual_imgs_paths = None

    self.get_virtual_imgs()


  def get_virtual_imgs(self): 
    """If the path is non-null, retrieves images at that path. 
    
    If the path is a directory, images will be sorted by filename, 
    smallest to largest. Images should be named according to the following 
    pattern: 
      0.ext
      1.ext
      ...
      n.ext

    If non-null, initalizes:
      (int) self.current_img_idx, 
      (int) self.num_imgs
      (List[ndarray]) self.virtual_imgs
    If a directory, also initializes for debugging purposes: 
      (List[str]) self.virtual_imgs_paths
    Returns: 
      (NoneType): None 
    """
    if self.virtual_path is None: 
      return 

    if os.path.isfile(self.virtual_path):
      self.virtual_imgs = [helpers.load_img(virtual_path)]
      self.current_img_idx = 0
      self.num_imgs = 1
    else: # is a directory
      self.virtual_imgs_paths = []
      for img_ext in IMG_EXTS: 
        self.virtual_imgs_paths += glob.glob(self.virtual_path + "*" + img_ext)

      self.virtual_imgs_paths.sort()

      self.virtual_imgs = \
        list(map(lambda path: helpers.load_img(path), self.virtual_imgs_paths))

      self.current_img_idx = 0
      self.num_imgs = len(self.virtual_imgs_paths)
    return None

  def crop_ar(new, old): 
    """Fit the new image to the old images aspect ratio. 
    
    Args: 
      new (ndarray): the virtual background image
      old (ndarray): the camera background image
    """
    # for now, a pretty simple resizing method...
    # TODO: crop to fit, instead of just resize to fit.
    old_shape = (old.shape[0], old.shape[1])

    resized_new = skimage.transform.resize(new, old_shape, preserve_range=True)

    return resized_new

  def update_img_pointer(self): 
    """Update the current_img_idx to point to the next frame in the path. 
      Note we wrap around/treat the list in a circular manner. 
    
    Returns: 
      (NoneType): updates the pointer self.current_img_idx
    """
    if self.current_img_idx == self.num_imgs - 1: 
      self.current_img_idx = 0
    else:
      self.current_img_idx += 1

    return None

  def apply_effect(self, background): 
    """Apply the virtual background to the actual background. 

    Args:
      background (ndarray): the background matte
        TODO update this b/c it doesn't really matter if you pass
        the matted BG img or the full image. Conceptually, you're
        just pasting the foreground component to the 'effected'
        image. I suppose for programmatic clarity it may be easier 
        to see this as just the background...
    """
    curr_virtual_img = self.virtual_imgs[self.current_img_idx]
    self.update_img_pointer()
    # Crop the virtual image to the background image shape. 
    resized_virtual_img = self.crop_ar(curr_virtual_img, background)

    return resized_virtual_img

class ColorEffect():
  def __init__(self, color): 
    self.color = color

class BlurEffect():
  def __init__(self, blur): 
    self.blur = blur

  def apply_effect(self, image, bg_mask, fg_mask):
    """Apply the blur to the background of image and superimposes fg
      on the blur.

    Args: 
      image (ndarray): the image. 
      bg_mask, fg_mask (ndarray): the masks. 
    Returns: 
      (ndarray): the composition of the blurred background and the preserved fg.
    """
    fg = image * fg_mask
    bg = image - fg

    # Sigma is the parameter defining kernel size. 
    # Apply to the three color channels separately.  
    blurred_bg = gaussian_filter(bg, sigma=(self.blur, self.blur, 0))

    composition = blurred_bg + fg

    return composition

class BackgroundEffect():
  def __init__(self, virtual, color, blur):
    self.virtual = virtual
    self.color = color
    self.blur = blur

    self.virtual_effect = VirtualEffect(self.virtual) 
    self.color_effect = ColorEffect(self.color)
    self.blur_effect = BlurEffect(self.blur)

  def get_new_background(self, image, bg_mask, fg_mask):
    """Apply the specified effect to the background image. 
    
    Args: 
      background (ndarray): the matted background image.
      bg_mask, fg_mask (ndarray): the respective binary masks.  
    Returns: 
      (ndarray): the matted background image with the specified effect.
    """
    composition = np.zeros_like(image)


    if self.virtual:
      composition = self.virtual_effect.apply_effect(image, bg_mask, fg_mask)
    elif self.color: 
      composition = self.color_effect.apply_effect(image, bg_mask, fg_mask)
    elif self.blur:
      composition = self.blur_effect.apply_effect(image, bg_mask, fg_mask)
    else: 
      raise AssertionError("No background effect specified.")

    assert(composition.shape == image.shape)

    return composition

  def get_bg_fg_masks(self, image): 
    """Apply the bodypix model to an image, returning the fg/bg mask. 
    
    Args:
      image (ndarray): the given image. 
    Returns: 
      A 2-tuple of: 
        (ndarray): the background mask
        (ndarray): the foreground mask
      Both in the shape of the given image (but one dimensional.)
    """
    image_array = tf.keras.preprocessing.image.img_to_array(image)

    result = bodypix_model.predict_single(image_array)
    
    mask = result.get_mask(threshold=0.55)
    
    fg_mask = mask.numpy().astype(np.uint8)
    
    bg_mask = np.abs(fg_mask - 1)

    return bg_mask, fg_mask

  def apply_effect(self, image): 
    """Apply the effect to the image. 

    Args: 
      image (ndarray): the image to be effected. 
    Returns: 
      (ndarray): the foreground image composed with the effected background. 
    """
    bg_mask, fg_mask = self.get_bg_fg_masks(image) 
    composition = self.get_new_background(image, bg_mask, fg_mask)

    return composition





