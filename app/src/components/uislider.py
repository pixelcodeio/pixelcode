from . import *

class UISlider(BaseComponent):
  """
  Class representing a UISlider in swift
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

    if self.info.get('thumb_fill'):
      C += ("{}.thumbTintColor = {}\n"
           ).format(self.id, utils.create_uicolor(self.info['thumb_fill']))

    return C
