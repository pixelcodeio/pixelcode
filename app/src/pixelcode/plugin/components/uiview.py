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

    keys = ["fill", "border-radius", "stroke-color", "stroke-width",]
    fill, border_r, stroke_c, stroke_w = utils.get_vals(keys, rect)

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
