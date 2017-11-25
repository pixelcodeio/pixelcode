from . import *

class UITextField(BaseComponent):
  """
  Class representing a UITextField in swift
    swift: (str) the swift code to create/set properties of a UITextField
  """
  def __init__(self, id_, info, in_v=False, set_p=False):
    """
    Returns: A UITableView with the swift attribute set to the generated code
    """
    super(UITextField, self).__init__()
    if set_p:
      tspan = info.get('text').get('textspan')
      pl = tspan[0]['contents']
      plc = tspan[0]['fill']
      self.swift = self.set_placeholder_tc(id_, pl, plc)
    else:
      self.swift = self.setup_component(id_, info, in_v=in_v)

  def set_placeholder_tc(self, tid, text, color):
    """
    Args:
      tid: (str) id of the UITextField
      text: (str) placeholder text
      color: (tuple) color to set the placeholder

    Returns: (str) The swift code to set placeholder's text and color.
    """
    return ('{}.attributedPlaceholder = NSAttributedString(string: "{}", '
            'attributes: [NSAttributedStringKey.foregroundColor: {}])\n'
           ).format(tid, text, utils.create_uicolor(color))

  def set_left_inset(self, tid, left):
    """
    Args:
      tid: (str) id of the UITextField
      left: (int) the number of pixels to set the left-inset

    Returns: (str) The swift code to set the left-inset of a UITextField
    """
    return ('{}.layer.sublayerTransform = CATransform3DMakeTranslation({}'
            ', 0, 0)\n'
           ).format(tid, left)

  def set_font_family_size(self, elem, font, size):
    """
    Args:
      elem: (str) id of element
      font: (str) font name
      size: (int) size of the font

    Returns:
      (str) The swift code to set the font-family and size of the title in e
    """
    return ("{}.font = {}\n").format(elem, super().create_font(font, size))

  def setup_component(self, elem, info, in_v=False):
    """
    Args:
      elem: (str) id of the component
      textspan: (dict array) see generate_component docstring for more
                information.
      left_inset: (int) pixels representing the number of left-inset

    Returns:
       (str) The swift code to apply all the properties from textspan and
       left_inset to elem.
    """
    tspan = info.get('text').get('textspan')
    left_inset = info.get('left-inset')
    txt = tspan[0]
    placeholder = txt.get('contents')
    p_color = txt.get('fill')
    font = txt.get('font-family')
    size = txt.get('font-size')
    c = ""
    if not in_v:
      c += self.set_placeholder_tc(elem, placeholder, p_color)
    c += self.set_font_family_size(elem, font, size)
    c += self.set_left_inset(elem, left_inset)
    c += super().clips_to_bounds(elem)
    return c
