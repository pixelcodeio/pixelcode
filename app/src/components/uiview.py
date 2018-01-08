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
    keys = ["fill", "border-radius", "stroke-color", "stroke-width",]
    fill, border_r, stroke_c, stroke_w = utils.get_vals(keys, self.info["rect"])
    C = ""
    if fill is not None:
      C += utils.set_bg(self.id, fill)
    if border_r is not None:
      C += utils.set_corner_radius(self.id, border_r)
    if stroke_c is not None:
      C += utils.set_border_color(self.id, stroke_c)
    if stroke_w is not None:
      C += utils.set_border_width(self.id, stroke_w)

    return C
