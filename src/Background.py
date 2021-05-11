"""The background class and associated functions. 

@author: <rbm@cmu.edu>
@date: 05/08/21
"""

class BackgroundEffect():
  def __init__(self, virtual, color, blur):
    self.virtual = virtual
    self.color = color
    self.blur = blur

  def apply_effect(self, background): 
    """Apply the specified effect to the background image. 

    """