import components.utils as utils

class UITextView(object):
  """
  Class representing a UITextView in swift
  """
  def set_placeholder_text_and_color(self, tid, text, color, opacity):
    r, g, b = color
    o = "1.0" if opacity is None else opacity
    c = ("UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha"
         ": {})"
        ).format(r, g, b, o)
    return ('{}.attributedPlaceholder = NSAttributedString(string: "{}", '
            'attributes: [NSAttributedStringKey.foregroundColor: {}])\n'
           ).format(tid, text, c)

  def set_left_inset(self, tid, left):
    return ('{}.layer.sublayerTransform = CATransform3DMakeTranslation({}'
            ', 0, 0)\n'
           ).format(tid, left)

  def set_clips_to_bounds(self, elem):
    """
    Args:
      elem: (str) id of element

    Returns: The swift code to set the clipsToBounds property of elem to true.
    """
    return "{}.clipsToBounds = true\n".format(elem)

  def set_font_family_size(self, elem, font, size):
    """
    Args:
      elem: (str) id of element
      font: (str) font name
      size: (int) size of the font

    Returns: The swift code to set the font family and size of the title in elem
    """
    return ("{}.font = UIFont(name: \"{}\", size: {})\n"
           ).format(elem, font, size)

  def setup_uitextview(self, elem, textspan, left_inset, inView=False):
    """
    Args:
      elem: (str) id of the component
      textspan: (dict array) see generate_component docstring for more info
      left_inset: (int) pixels representing the number of left-inset

    Returns: The swift code to apply all the properties from textspan and
    left_inset to elem.
    """
    txt = textspan[0]
    placeholder = txt['contents']
    placeholder_c = txt['fill']
    font = txt['font-family']
    size = txt['font-size']
    opacity = txt['opacity']
    if inView is False:
      c = self.set_placeholder_text_and_color(elem, placeholder,
                                              placeholder_c, opacity)
    else:
      c = ""
    c += self.set_font_family_size(elem, font, size)
    c += self.set_left_inset(elem, left_inset)
    c += self.set_clips_to_bounds(elem)
    return c
