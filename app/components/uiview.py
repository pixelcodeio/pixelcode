import components.utils as utils

class UIView(object):
  """
  Class representing a UIView in swift
  """
  def __init__(self):
    pass

  def setup_uiview(self, elem, info):
    """
    Args:
      elem: (str) id of the component
      info: (dict) see generate_component docstring for more information.

    Returns: The swift code to apply all the properties from text to elem.
    """
    fill = info['fill']
    border_r = info['border-radius']
    stroke_c = info['stroke-color']
    stroke_w = info['stroke-width']
    opacity = info['opacity']
    c = utils.set_bg(elem, fill, opacity) if fill != None else ""
    c += utils.set_corner_radius(elem, border_r) if border_r != None else ""
    c += utils.set_border_color(elem, stroke_c) if stroke_c != None else ""
    c += utils.set_border_width(elem, stroke_w) if stroke_w != None else ""
    return c
