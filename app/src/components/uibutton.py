from . import *

class UIButton(BaseComponent):
  """
  Class representing a UIButton in swift
    swift: (str) the swift code to create/set properties of a UIButton
  """
  def generate_swift(self):
    if self.env["set_p"]:
      contents = self.info.get('text').get('textspan')[0].get('contents')
      return self.set_title(contents) if contents is not None else ""
    return self.setup_component(in_v=self.env["in_view"])

  def set_title(self, title):
    """
    Args:
      elem: (str) id of element
      title: (str) title to set the element

    Returns: (str) swift code to set title of a elem using title
    """
    title = title.decode('utf-8')
    return '{}.setTitle(\"{}\", for: .normal)\n'.format(self.id, title)

  def set_title_color(self, color):
    """
    Args:
      elem: (str) id of element
      color: (tuple) contains r, g, b values of the title color

    Returns:
      (str) swift code to set title color of elem using [color]
    """
    c = utils.create_uicolor(color)
    return '{}.setTitleColor({}, for: .normal)\n'.format(self.id, c)

  def set_font_family_size(self, e, f, s):
    """
    Args:
      e: (str) id of element
      f: (str) font family name
      s: (int) size of font

    Returns:
      (str) swift code to set the font family and size of the title in elem
    """
    return ("{}.titleLabel?.font = {}\n").format(e, super().create_font(f, s))

  def setup_component(self, elem, info, in_v=False):
    """
    Args:
      elem: (str) id of the component
      textspan: (dict list) see generate_component docstring for more info.
      in_v: (bool) whether the component is generated within a custom view file

    Returns:
      (str) swift code to apply all the properties from textspan to elem.
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
