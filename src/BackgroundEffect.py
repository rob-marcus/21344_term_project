"""The background class and associated functions. 

@author: <rbm@cmu.edu>
@date: 05/08/21
"""
from constants import IMG_EXTS
import glob
import helpers
import os

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

  def apply_effect(self, background): 
    """


    """
class ColorEffect():
  def __init__(self, color): 
    self.color = color

class BlurEffect():
  def __init__(self, blur): 
    self.blur = blur

class BackgroundEffect():
  def __init__(self, virtual, color, blur):
    self.virtual = virtual
    self.color = color
    self.blur = blur

    self.virtual_effect = VirtualEffect(self.virtual) 
    self.color_effect = ColorEffect(self.color)
    self.blur_effect = BlurEffect(self.blur)


  def get_new_background(self, background):
    """Apply the specified effect to the background image. 
    
    Args: 
      background (ndarray): the matted background image. 
    Returns: 
      (ndarray): the matted background image with the specified effect.
    """
    new_bg = np.zeros_like(background)


    if self.virtual:
      new_bg = self.virtual_effect.apply_effect(background)
    elif self.color: 
      new_bg = self.color_effect.apply_effect(background)
    elif self.blur:
      new_bg = self.blur_effect.apply_effect(background)
    else: 
      raise AssertionError("No background effect specified.")

    assert(new_bg.shape == background.shape)

    return new_bg

  def apply_effect(self, background, foreground): 
    """Apply the effect to the background and combine with the foreground. 

    Args: 
      background (ndarray): the matted background image. 
      foreground (ndarray): the matted foreground image. 
    Returns: 
      (ndarray): the foreground image composed with the effected background. 
    """
    new_bg = self.get_new_background(background)

    




    