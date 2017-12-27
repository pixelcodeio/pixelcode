from . import *

class UISegmentedControl(BaseComponent):
  """
  Class representing a UISegmentedControl in swift
  """
  def generate_swift(self):
    return self.setup_component()

  def setup_component(self):
    """
    Returns: swift code to setup UISlider.
    """
    
