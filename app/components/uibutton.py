import components.utils as utils

class UIButton(object):
  """
  Class representing a UIButton in swift
  """
  def __init__(self):
    pass

  def set_title(self, elem, title):
    """
    Args:
      elem: (str) id of element
      title: (str) title to set the element

    Returns: The swift code to set title of a elem using title
    """
    return '{}.setTitle(\"{}\", for: .normal)\n'.format(elem, title)

  def set_title_color(self, elem, color):
    """
    Args:
      elem: (str) id of element
      color: (tuple) contains r, g, b values of the title color

    Returns: The swift code to set title color of elem using the r, g, b values
    """
    r = color[0]
    g = color[1]
    b = color[2]
    c = ('UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha: 1.0)'
        ).format(r, g, b)
    return '{}.setTitleColor({}, for: .normal)\n'.format(elem, c)

  def set_font_size(self, elem, size):
    """
    Args:
      elem: (str) id of element
      size: (int) size of font

    Returns: The swift code to set the font size of elem using size
    """
    font = 'UIFont.systemFont(ofSize: {})'.format(size)
    return '{}.titleLabel?.font = {}\n'.format(elem, font)

  def set_font_size_weight(self, elem, size, weight):
    """
    Returns: The swift code to set the font size and weight of elem.
    """
    return ("{}.titleLabel?.font = UIFont.systemFont(ofSize: {}, weight: "
            "UIFont.Weight.init(rawValue: {}))\n"
           ).format(elem, size, weight)

  def set_font_family(self, elem, font, size):
    """
    Returns: The swift code to set the font family and size of the title in elem
    """
    return ("{}.titleLabel?.font = UIFont(name: \"{}\", size: {})\n"
           ).format(elem, font, size)
