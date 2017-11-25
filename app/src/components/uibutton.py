from . import *

class UIButton(BaseComponent):
  """
  Class representing a UIButton in swift
  """
  def __init__(self, id_, info, in_v=False, set_p=False):
    """
    Args:
      swift: (str) the swift code to create/set properties of a UIButton
    """
    super(UIButton, self).__init__()
    if set_p:
      contents = info.get('text').get('textspan')[0].get('contents')
      self.swift = self.set_title(id_, contents) if contents is not None else ""
    else:
      self.swift = self.setup_component(id_, info, in_v=in_v)

  def set_title(self, elem, title):
    """
    Args:
      elem: (str) id of element
      title: (str) title to set the element

    Returns: (str) The swift code to set title of a elem using title
    """
    title = title.decode('utf-8')
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
    return ("{}.titleLabel?.font = {}\n").format(e, super().create_font(f, s))

  def setup_component(self, elem, info, in_v=False):
    """
    Args:
      elem: (str) id of the component
      textspan: (dict array) see generate_component docstring for more
                information.
      in_v: (bool) represents whether the button is being generated
               inside a custom view file (or not)

    Returns:
      (str) The swift code to apply all the properties from textspan to elem.
    """
    tspan = info.get('text').get('textspan')
    if len(tspan) == 1:
      # the contents of the textspan don't vary
      txt = tspan[0]
      contents = txt.get('contents')
      fill = txt.get('fill')
      font = txt.get('font-family')
      size = txt.get('font-size')
      c = ""
      if not in_v and contents is not None:
        c = self.set_title(elem, contents)
      c += self.set_title_color(elem, fill) if fill != None else ""
      c += self.set_font_family_size(elem, font, size)
      return c
    #TODO: Case for varying text.
