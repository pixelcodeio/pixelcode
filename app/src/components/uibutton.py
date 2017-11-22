import utils

class UIButton(object):
  """
  Class representing a UIButton in swift
  """
  def set_title(self, elem, title):
    """
    Args:
      elem: (str) id of element
      title: (str) title to set the element

    Returns: (str) The swift code to set title of a elem using title
    """
    return '{}.setTitle(\"{}\", for: .normal)\n'.format(elem, title)

  def set_title_color(self, elem, color):
    """
    Args:
      elem: (str) id of element
      color: (tuple) contains r, g, b values of the title color

    Returns:
      (str) The swift code to set title color of elem using the r, g,
      b values
    """
    c = utils.create_uicolor(color)
    return '{}.setTitleColor({}, for: .normal)\n'.format(elem, c)

  def set_font_size(self, elem, size):
    """
    Args:
      elem: (str) id of element
      size: (int) size of font

    Returns: (str) The swift code to set the font size of elem using size
    """
    font = 'UIFont.systemFont(ofSize: {})'.format(size)
    return '{}.titleLabel?.font = {}\n'.format(elem, font)

  def set_font_family_size(self, elem, font, size):
    """
    Args:
      elem: (str) id of element
      font: (str) font family name
      size: (int) size of font

    Returns:
      (str) The swift code to set the font family and size of the title in elem
    """
    return ("{}.titleLabel?.font = {}\n"
           ).format(elem, utils.create_font(font, size))

  def setup_uibutton(self, elem, textspan, in_view=False):
    """
    Args:
      elem: (str) id of the component
      textspan: (dict array) see generate_component docstring for more
                information.
      in_view: (bool) represents whether the button is being generated
               inside a custom view file (or not)

    Returns:
      (str) The swift code to apply all the properties from textspan to elem.
    """
    if len(textspan) == 1:
      # the contents of the textspan don't vary
      txt = textspan[0]
      contents = txt.get('contents')
      fill = txt.get('fill')
      font = txt.get('font-family')
      size = txt.get('font-size')
      if not in_view:
        c = self.set_title(elem, contents) if contents != None else ""
      else:
        c = ""
      c += self.set_title_color(elem, fill) if fill != None else ""
      c += self.set_font_family_size(elem, font, size)
      return c
    #TODO: Case for varying text.
