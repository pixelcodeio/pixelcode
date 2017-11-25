from . import *

class UIView(BaseComponent):
  """
  Class representing a UIView in swift
    swift: (str) the swift code to create/set properties of a UIView
  """
  def __init__(self, id_, info, in_v=False, set_p=False):
    """
    Returns: A UITableView with the swift attribute set to the generated code
    """
    super(UIView, self).__init__()
    self.swift = self.setup_component(id_, info)

  def setup_component(self, elem, info, in_v=False):
    """
    Args:
      elem: (str) id of the component
      info: (dict) see generate_component docstring for more info.

    Returns: The swift code to apply all the properties from text to elem.
    """
    fill = info.get('fill')
    border_r = info.get('border-radius')
    stroke_c = info.get('stroke-color')
    stroke_w = info.get('stroke-width')

    c = ""
    if fill is not None:
      c += utils.set_bg(elem, fill)
    if border_r is not None:
      c += utils.set_corner_radius(elem, border_r)
    if stroke_c is not None:
      c += utils.set_border_color(elem, stroke_c)
    if stroke_w is not None:
      c += utils.set_border_width(elem, stroke_w)

    return c
