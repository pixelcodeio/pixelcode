from . import *

class UIView(BaseComponent):
  """
  Class representing a UIView in swift
    swift: (str) the swift code to create/set properties of a UIView
  """
  def generate_swift(self):
    return self.setup_component()

  def setup_component(self):
    """
    Returns: The swift code to apply all the properties from text to elem.
    """
    info = self.info
    fill = info.get('fill')
    border_r = info.get('border-radius')
    stroke_c = info.get('stroke-color')
    stroke_w = info.get('stroke-width')

    C = ""
    if fill is not None:
      C += utils.set_bg(elem, fill)
    if border_r is not None:
      C += utils.set_corner_radius(elem, border_r)
    if stroke_c is not None:
      C += utils.set_border_color(elem, stroke_c)
    if stroke_w is not None:
      C += utils.set_border_width(elem, stroke_w)

    return C
