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
    tint_fill = utils.create_uicolor(self.info["tint_fill"])
    selected_index = self.info["selected_index"]
    return ("{0}.tintColor = {1}\n"
            "{0}.selectedSegmentIndex = {2}\n"
           ).format(self.id, tint_fill, selected_index)
