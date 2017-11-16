import components.utils as utils

class UIView(object):
  """
  Class representing a UIView in swift
  """
  def setup_uiview(self, elem, info):
    """
    Args:
      elem: (str) id of the component
      info: (dict) see generate_component docstring for more information.

    Returns: The swift code to apply all the properties from text to elem.
    """
    fill = info.get('fill')
    border_r = info.get('border-radius')
    stroke_c = info.get('stroke-color')
    stroke_w = info.get('stroke-width')
    stroke_o = info.get('stroke-opacity')
    opacity = info.get('opacity')
    c = ""
    if fill is not None:
      c += utils.set_bg(elem, fill, opacity)
    if border_r is not None:
      c += utils.set_corner_radius(elem, border_r)
    if stroke_c is not None:
      c += utils.set_border_color(elem, stroke_c, stroke_o)
    if stroke_w is not None:
      c += utils.set_border_width(elem, stroke_w)
    return c
