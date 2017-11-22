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

  def set_font_family_size(self, e, f, s):
    """
    Args:
      e: (str) id of element
      f: (str) font family name
      s: (int) size of font

    Returns:
      (str) The swift code to set the font family and size of the title in elem
    """
    return ("{}.titleLabel?.font = {}\n").format(e, utils.create_font(f, s))

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
      c = ""
      if not in_view and contents is not None:
        c = self.set_title(elem, contents) 
      c += self.set_title_color(elem, fill) if fill != None else ""
      c += self.set_font_family_size(elem, font, size)
      return c
    #TODO: Case for varying text.
