from . import *

class UIButton(BaseComponent):
  """
  Class representing a UIButton in swift
    swift: (str) the swift code to create/set properties of a UIButton
  """
  def generate_swift(self):
    if self.env["set_prop"]:
      contents = self.info.get('text').get('textspan')[0].get('contents')
      return self.set_title(contents) if contents is not None else ""
    return self.setup_component()

  def set_title(self, title):
    """
    Returns: (str) swift code to set title
    """
    title = title.decode('utf-8')
    return '{}.setTitle(\"{}\", for: .normal)\n'.format(self.id, title)

  def set_title_color(self, color):
    """
    Args:
      color: (tuple) contains r, g, b values of the title color

    Returns:
      (str) swift code to set title color
    """
    c = utils.create_uicolor(color)
    return '{}.setTitleColor({}, for: .normal)\n'.format(self.id, c)

  def set_font_family_size(self, font, size):
    """
    Args:
      font: (str) font family name
      size: (int) size of font

    Returns:
      (str) swift code to set the font family and size of title
    """
    return ("{}.titleLabel?.font = {}\n"
           ).format(self.id, super().create_font(font, size))

  def setup_component(self):
    """
    Returns:
      (str) swift code to setup uibutton
    """
    tspan = self.info.get('text').get('textspan')
    if len(tspan) == 1:
      # the contents of the textspan don't vary
      txt = tspan[0]
      contents = txt.get('contents')
      fill = txt.get('fill')
      font = txt.get('font-family')
      size = txt.get('font-size')
      C = ""
      if not self.env["in_view"] and contents is not None:
        C = self.set_title(contents)
      C += self.set_title_color(fill) if fill != None else ""
      C += self.set_font_family_size(font, size)
      return C
    #TODO: Case for varying text.
