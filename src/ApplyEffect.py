"""Loads frame(s) and applies the effect. 

@author: <rbm@cmu.edu>
@date: 05/11/21
"""
import constants
import cv2
import glob
import helpers
import os

# in case in path is None, default to WebCam.
class WebCam():
  def __init__(self): 
    self.webcam_descriptor = 0

  def run(self, background_effect, write_effect): 
    """Applies the effect to the frames in the video, and writes it if 
      specified. 
      
      If the webcam cannot be accessed an assertion error will be thrown.
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

    while True:
      check, frame = video.read()
      
      effected_frame = background_effect.apply_effect(frame)
      
      write_effect(effected_frame)

      key = cv2.waitKey(1)

      if key == ord('q'): # Only break if user presses 'q'
        break 

    video.release()
    cv2.destroyAllWindows()

    return

class Images(): 
  def __init__(self, in_path):
    self.in_path = in_path
    self.image_paths = 

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
    cv2.imwrite(self.out_path + str(curr_frame) + ".png")

    self.curr_frame += 1

    return

  def stitch_effected_frames(self, frames):
    """Stitches the given frames into a video. Saved at the out_path.
    
    Args:
      frames (List[ndarray]): a list of effected frames.
    Returns:
      (NoneType): None. 
    """
    paths = os.listdir(self.out_path)
    paths.sort()

    # FPS
    # Default to 20...
    if do_stitch: 
      fps = 20
      vid_shape = (frames[0].shape[0], frames[0].shape[1])
      video = cv2.VideoWriter("stitched_frames.avi", 
                              cv2.VideoWriter_fourcc(*'MJPG'), 
                              fps,
                              vid_shape)

      for frame in frames: 
        video.write(cv2.imread(frame))

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
    effected_frames = \
      feed_src.run(self.background_effect, self.write_result)

    if self.do_stitch:
      self.stitch_effected_frames(effected_frames)

    return 

