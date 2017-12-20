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
    C = ("{}.isContinuous = true\n").format(self.id)

    if self.info.get('progress_fill'):
      C += ("{}.minimumTrackTintColor = {}\n"
           ).format(self.id, utils.create_uicolor(self.info['progress_fill']))

    return C
