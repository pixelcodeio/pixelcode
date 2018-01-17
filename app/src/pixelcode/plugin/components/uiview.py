from . import *

class UIView(BaseComponent):
  """
  Class representing a UIView in swift
  """
  def generate_swift(self):
    return self.setup_component()

  def setup_component(self):
    """
    Returns: swift code to setup uiview.
    """
    if self.info.get("components") is not None: # container
      rect = self.info.get("rect")
    else: # rect
      rect = self.info

    C = ""
    return C
