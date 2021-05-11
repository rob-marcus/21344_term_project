"""The user-specified parameter class and associated parsing functions. 

@author: <rbm@cmu.edu>
@date: 05/07/21
"""
from constants import IMG_EXTS
import os
import glob
import time


def validate_in_path(path, param_str): 
  """Verifies that a path leads to either an image, or a non-empty image 
  folder.
  
  Args:
    path (str): path to either an existing image or a folder with at 
      least one image.
    param_str (str): the parameter being checked, e.g., "virtual".
  Returns: 
    (NoneType): None if the predicate holds. Otherwise will raise an 
      assertion error.  
  """
  # Check if is a file. 
  if os.path.isfile(path): 
    ext = os.path.splitext(path)[-1].lower()
    if ext not in IMG_EXTS: 
      err_str = ("Path error for {} argument: the file at path {} " + \
                 "is not a recognized image type. " + \
                 "Recognized extensions are {}."
                ).format(param_str, path, IMG_EXTS)

      raise AssertionError(err_str)
  elif os.path.isdir(path):
    contains_valid_ext = False

    for ext in IMG_EXTS:
      if glob.glob(path + "*" + ext) != []:
        if contains_valid_ext == True: 
          raise AssertionError("Please only have one image extension type in the in path.")
        else: 
          contains_valid_ext = True

    if not contains_valid_ext:
      err_str = ("Path error for {} argument: the folder {} has " + \
                 "no files with valid image extensions. " + \
                 "Recognized extensions are {}."
                ).format(param_str, path, IMG_EXTS)

      raise AssertionError(err_str)
  else: # path leads to nothing.
    raise AssertionError("The path {} does not exist".format(path))

  return None

def validate_out_path(path): 
  """Checks if an output path to a directory exists, otherwise creates the dir.

  Args:
    path (str): path to either an existing image or a folder with at 
      least one image.
  Returns: 
    (NoneType): None.
  """
  if not os.path.isdir(path):
    os.mkdir(path)

  return None

class Params():
  """Class for parameters (arguments) used to compile the program. 

  """

  def __init__(self, virtual, color, blur, time, debug, out_path, in_path, stitch):
    self.virtual = virtual
    self.color = color
    self.blur = blur
    self.time = time
    self.debug = debug
    self.out_path = out_path
    self.in_path = in_path
    self.stitch = stitch

    self.virtual_str = "virtual"
    self.color_str = "color"
    self.blur_str = "blur"
    self.time = "time"
    self.in_path_str = "in_path"

    self.validate_inputs()

  def validate_inputs(self): 
    """Verifies that each input is well-formed.

    Returns:
      (NoneType): None if all inputs are well-formed. Otherwise will raise an 
        assertion error for the first malformed input found. 
    """
    if self.virtual:
      validate_in_path(self.virtual, self.virtual_str)

    if self.color: 
      assert(self.color in {"white", "blue", "yellow", "random"})

    if self.blur:
      assert(self.blur % 2 == 1 and self.blur > 0)

    # Make sure we are only specifying at most one background type. 
    if (self.virtual and self.color) or (self.virtual and self.blur) or \
      (self.color and self.blur): 
      raise AssertionError("Please specify only one background type.")

    # If no background type is specified, default to a blur of 3. 
    if (self.virtual is None) and (self.color is None) and (self.blur is None):
      self.blur = 5

    if self.out_path: 
      validate_out_path(self.out_path)
    else: # make the outpath just the current systime. 
      out_path = str(time.time())[:10] + str(time.time())[11:] + "/"
      self.out_path = out_path
      os.mkdir(out_path)
      print("Out path was unspecified.")
      print(("Processed images will be stored at {} "
            + "in the program folder").format(self.out_path))

    if self.in_path: # If None we read from webcam. 
      validate_in_path(self.in_path, self.in_path_str)

    return None