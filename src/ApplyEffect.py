"""Loads frame(s) and applies the effect. 

@author: <rbm@cmu.edu>
@date: 05/11/21
"""

# in case in path is None, default to WebCam.
class WebCam():
  def __init__(self): 
    self.webcam_descriptor = 0


class Images(): 
  def __init__(self):
    pass

class ApplyEffect():
  def __init__(self, in_path, out_path, do_stitch, be): 
    self.in_path = in_path
    self.out_path = out_path
    self.do_stitch = do_stitch
    self.background_effect = be

    #self.apply_effect()
  
  def write_effect(self, frame): 
    """Writes a given frame to the specified out_path. 
    
    Args: 
      frame (ndarray): an effected frame. 
    Returns: 
      (NoneType): None. 
    """
    pass

  def apply_effect(self):
    """Applies the specified effect to the specified input mode. 

    """
    feed_src = None
    if in_path is None: 
      feed_src = WebCam()
    else: 
      feed_src = Images()

    # Bad design but let's just rely on the WebCam and Images class 
    # to check for errors and assume they won't give any 
    # unexpected behavior.
    feed_src.apply_effect(self.background_effect, self.write_result)



