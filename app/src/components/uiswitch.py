from . import *

class UISwitch(BaseComponent):
  """
  Class representing a UISwitch in swift
  """
  def generate_swift(self):
    return self.setup_component()

  def setup_component(self):
    """
    Returns: swift code to setup UISlider.
    """
    return ("{}.onTintColor = {}\n"
           ).format(self.id, utils.create_uicolor(self.info['rect']['fill']))
