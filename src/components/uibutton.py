import components.utils as utils

class UIButton(object):
  """
  Class representing a UIButton in swift
  """
  def set_title(self, elem, title):
    """
    Args:
      elem: (str) id of element
      title: (str) title to set the element

    Returns: The swift code to set title of a elem using title
    """
    return '{}.setTitle(\"{}\", for: .normal)\n'.format(elem, title)

  def set_title_color(self, elem, color, opacity):
    """
    Args:
      elem: (str) id of element
      color: (tuple) contains r, g, b values of the title color
      opacity: (float) between 0 and 1

    Returns: The swift code to set title color of elem using the r, g, b values
    """
    o = "1.0" if opacity is None else opacity
    r, g, b = color
    c = ('UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha: {})'
        ).format(r, g, b, o)
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

  def set_font_family_size(self, elem, font, size):
    """
    Returns: The swift code to set the font family and size of the title in elem
    """
    return ("{}.titleLabel?.font = UIFont(name: \"{}\", size: {})\n"
           ).format(elem, font, size)

  def setup_uibutton(self, elem, textspan, inView=False):
    """
    Args:
      elem: (str) id of the component
      textspan: (dict array) see generate_component docstring for more
                information.

    Returns: The swift code to apply all the properties from textspan to elem.
    """
    if len(textspan) == 1:
      # the contents of the textspan don't vary
      txt = textspan[0]
      contents = txt.get('contents')
      fill = txt.get('fill')
      font = txt.get('font-family')
      size = txt.get('font-size')
      opacity = txt.get('opacity')
      if inView is False:
        c = self.set_title(elem, contents) if contents != None else ""
      else:
        c = ""
      c += self.set_title_color(elem, fill, opacity) if fill != None else ""
      c += self.set_font_family_size(elem, font, size)
      return c
    #TODO: Case for varying text.
