import components.utils as utils

class UITextField(object):
  """
  Class representing a UITextField in swift
  """
  def set_placeholder_tc(self, tid, text, color):
    """
    Returns: The swift code to set placeholder's text and color.
    """
    return ('{}.attributedPlaceholder = NSAttributedString(string: "{}", '
            'attributes: [NSAttributedStringKey.foregroundColor: {}])\n'
           ).format(tid, text, utils.create_uicolor(color))

  def set_left_inset(self, tid, left):
    return ('{}.layer.sublayerTransform = CATransform3DMakeTranslation({}'
            ', 0, 0)\n'
           ).format(tid, left)

  def set_cb(self, elem):
    """
    Args:
      elem: (str) id of element

    Returns: The swift code to set the clipsToBounds property of elem to true.
    """
    return "{}.clipsToBounds = true\n".format(elem)

  def set_font_family_size(self, e, f, s):
    """
    Args:
      e: (str) id of element
      f: (str) font name
      s: (int) size of the font

    Returns: The swift code to set the font-family and size of the title in e
    """
    return ("{}.font = {}\n").format(e, utils.create_font(f, s))

  def setup_uitextfield(self, elem, textspan, left_inset, in_view=False):
    """
    Args:
      elem: (str) id of the component
      textspan: (dict array) see generate_component docstring for more
                information.
      left_inset: (int) pixels representing the number of left-inset

    Returns: The swift code to apply all the properties from textspan and
    left_inset to elem.
    """
    txt = textspan[0]
    placeholder = txt.get('contents')
    p_color = txt.get('fill')
    font = txt.get('font-family')
    size = txt.get('font-size')
    c = ""
    if not in_view:
      c += self.set_placeholder_tc(elem, placeholder, p_color)
    c += self.set_font_family_size(elem, font, size)
    c += self.set_left_inset(elem, left_inset)
    c += self.set_cb(elem)
    return c
