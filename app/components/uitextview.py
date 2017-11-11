import components.utils as utils

class UITextView(object):
  """
  Class representing a UITextView in swift
  """
  def __init__(self):
    pass

  def set_text_font_and_size(self, elem, font, size):
    """
    Args:
      elem: (str) id of element
      font: (str) font family of element
      size: (int) size of font

    Returns: The swift code to set the font and font size of element
    """
    return ('{}.font = UIFont(name: "{}", size: {})\n').format(elem, font, size)

  def set_placeholder_text_and_color(self, tid, text, r, g, b):
    color = ("UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha"
             ": 1.0)"
            ).format(r, g, b)
    return ('{}.attributedPlaceholder = NSAttributedString(string: "{}", '
            'attributes: [NSAttributedStringKey.foregroundColor: {}])\n'
           ).format(tid, text, color)

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
