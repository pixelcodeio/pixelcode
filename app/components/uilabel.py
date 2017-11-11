import components.utils as utils

class UILabel(object):
  def __init__(self, bgColor):
    """
    Args:
      bgColor: (tuple) Background color of label as r, g, b values
    """
    self.bgColor = bgColor

  def create_attributed_str(self, elem, text):
    """
    Args:
      elem: (str) id of element
      text: (str) text of the attributed string.

    Returns: The swift code to create an attributed string.
    """
    return ("{}AttributedStr = NSMutableAttributedString(string: {})\n"
           ).format(elem, text)

  def set_text(self, elem, txt):
    """
    Returns: The swift code to set the text of elem to be txt
    """
    return '{}.text = "{}"\n'.format(elem, txt)

  def set_attributed_text(self, elem, strID):
    """
    Args:
      elem: (str) id of element
      strID: (str) id of attributed string

    Returns: The swift code to set the attributedText property of elem.
    """
    return ("{}.attributedText = {}\n").format(elem, strID)

  def set_text_color(self, elem, color):
    """
    Returns: The swift code to set the text color of elem to be color
    """
    r = color[0]
    g = color[1]
    b = color[2]
    return ("{}.textColor = UIColor(red: {}/255.0, green: {}/255.0, "
            "blue: {}/255.0, alpha: 1.0)\n"
           ).format(elem, r, g, b)

  def set_bg_color(self, elem):
    """
    Returns: The swift code to set the background color of elem.
    """
    r = self.bgColor[0]
    g = self.bgColor[1]
    b = self.bgColor[2]
    return ("{}.backgroundColor = UIColor(red: {}/255.0, green: {}/255.0, "
            "blue: {}/255.0, alpha: 1.0)\n"
           ).format(elem, r, g, b)

  def center_and_wrap(self, elem, textAlign):
    """
    Returns: The swift code to center the text and wrap lines
    """
    return ("{}.textAlignment = .{}\n{}.numberOfLines = 0\n"
            "{}.lineBreakMode = .byWordWrapping\n"
           ).format(elem, textAlign, elem, elem)

  def set_font_size(self, elem, size):
    """
    Returns: The swift code to set the font size of elem to be size
    """
    return '{}.font = UIFont.systemFont(ofSize: {})\n'.format(elem, size)

  def set_font_size_weight(self, elem, size, weight):
    """
    Returns: The swift code to set the font size and weight of elem.
    """
    return ("{}.font = UIFont.systemFont(ofSize: {}, weight: "
            "UIFont.Weight.init(rawValue: {}))\n"
           ).format(elem, size, weight)

  def set_font_family(self, elem, font, size):
    """
    Returns: The swift code to set the font family and size of the title in elem
    """
    return ("{}.font = UIFont(name: \"{}\", size: {})\n"
           ).format(elem, font, size)

  def set_num_of_lines(self, elem):
    """
    Returns: The swift code to set numberOfLines to be 0 for elem.
    """
    return "{}.numberOfLines = 0\n".format(elem)

  def set_substring_color(self, strID, r, g, b, start, length):
    """
    Args:
      strID: (string) the variable name of string that is to be edited
      r: (int) red rgb value
      g: (int) green rgb value
      b: (int) blue rgb value
      start: (int) index of first character whose color is being changed
      length: (int) number of characters from start index whose color is being
              changed.

    Returns: The swift code to set a substring of str to be a color with r,g,b
             values.
    """
    color = ("UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha)"
             ": 1.0)"
            ).format(r, g, b)
    return ("{}.addAttribute(NSForegroundColorAttributeName, value: {})"
            ", range: NSRange(location: {}, length: {}))\n"
           ).format(strID, color, start, length)

  def set_substring_font(self, strID, font, size, start, length):
    """
    Args:
      strID: (string) the variable name of string that is to be edited
      font: (string) the font of the substring
      start: (int) index of first character whose font is being changed
      length: (int) number of characters from start index whose font is being
              changed.

    Returns: The swift code to set a substring of str to be a font.
    """
    font = ('UIFont(name: "{}", size: {})').format(font, size)
    return ("{}.addAttribute(NSFontAttributeName, value: {}"
            ", range: NSRange(location: {}, length: {}))\n"
           ).format(strID, color, start, length)
