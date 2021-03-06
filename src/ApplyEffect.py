"""Loads frame(s) and applies the effect. 

@author: <rbm@cmu.edu>
@date: 05/11/21
"""
import constants
import cv2
import glob
import helpers
import os
import numpy as np

# in case in path is None, default to WebCam.
class WebCam():
  def __init__(self): 
    self.webcam_descriptor = 0

  def run(self, background_effect, write_effect): 
    """Applies the effect to the frames in the video, and writes it if 
      specified. 
      
      If the webcam cannot be accessed an assertion error will be thrown.

      The webcam will be run for a total of 60 frames. 
    Args: 
      background_effect (BackgroundEffect Class): an initialized 
        BackgroundEffect class.
      write_effect (function): the write_effect function, uses values 
        passed to ApplyEffect to determine where and if to write. 

    Returns: 
      (NoneType): None.
    """
    video = cv2.VideoCapture(self.webcam_descriptor)
    
    if video is None or not video.isOpened():
      raise AssertionError("Was unable to read from webcam.")

    curr_frame = 0
    max_frames = 9

    while True:
      check, frame = video.read()
      
      effected_frame = background_effect.apply_effect(frame)
      
      cv2.imshow("Webcam view.", effected_frame)
      cv2.waitKey(1)   # Don't wait for a keyboard input
      write_effect(effected_frame)

      curr_frame += 1
      print(curr_frame)
      if curr_frame > max_frames: 
        break

    video.release()
    cv2.destroyAllWindows()

    return

class Images(): 
  def __init__(self, in_path):
    self.in_path = in_path
    self.image_paths = self.get_imgs()

  def get_imgs(self):
    if os.path.isfile(self.in_path): 
      self.image_paths = [self.in_path]
    else: 
      # Build path list
      image_paths = []

      for ext in constants.IMG_EXTS: 
        image_paths += glob.glob(self.in_path + "*" + ext)

    return

  def run(self, background_effect, write_effect):
    """Applies the effect to the frames in the video, and writes it if 
      specified. 

    Args: 
      background_effect (BackgroundEffect Class): an initialized 
        BackgroundEffect class.
      write_effect (function): the write_effect function, uses values 
        passed to ApplyEffect to determine where and if to write. 

    Returns: 
      (NoneType): None.
    """

    for image_path in self.image_paths: 
      frame = helpers.load_img(image_path)

      effected_frame = background_effect.apply_effect(frame)

      write_effect(effected_frame)

    return

class ApplyEffect():
  def __init__(self, in_path, out_path, do_stitch, be): 
    self.in_path = in_path
    self.out_path = out_path
    self.do_stitch = do_stitch
    self.background_effect = be

    # Pointer for writing. 
    self.curr_frame = 0

  def write_effect(self, frame): 
    """Writes a given frame to the specified out_path. 
    
    Args: 
      frame (ndarray): an effected frame. 
    Returns: 
      (NoneType): None. 
    """
    cv2.imwrite(self.out_path + str(self.curr_frame) + ".jpg", frame)

    self.curr_frame += 1

    return

  def stitch_effected_frames(self, fps=20):
    """Stitches the given frames into a video. Saved at the out_path.
    
    Args:
      frames (List[ndarray]): a list of effected frames.
    Returns:
      (NoneType): None. 
    """
    paths = os.listdir(self.out_path)
    paths.sort()
    print(paths)
    if paths == []: 
      return

    # get frame shape. 
    first_frame = cv2.imread(self.out_path + paths[0])

    # TODO
    # Update fps to system setting...
    if self.do_stitch: 
      print("Attempting to stitch frames together. Will not work on every machine :<")
      vid_shape = (first_frame[0].shape[1], first_frame[0].shape[0])
      video = cv2.VideoWriter(self.out_path + "stitched_frames.avi", 
                              cv2.VideoWriter_fourcc(*'XVID'), 
                              fps,
                              vid_shape)

      for path in paths: 
        print("Looking at path {}".format(path))
        video.write(cv2.imread(self.out_path + path).astype(np.uint8))

      cv2.destroyAllWindows()
      video.release

  def apply_effect(self):
    """Applies the specified effect to the specified input mode. 

    """
    feed_src = None

    if self.in_path is None: 
      feed_src = WebCam()
    else: 
      feed_src = Images(self.in_path)

    # Bad design but let's just rely on the WebCam and Images class 
    # to check for errors and assume they won't give any 
    # unexpected behavior.
    feed_src.run(self.background_effect, self.write_effect)

    if self.do_stitch:
      self.stitch_effected_frames()

    return 

