from . import *

class UILabel(BaseComponent):
  """
  Class representing a UILabel in swift
    swift: (str) the swift code to create/set properties of a UILabel
  """
  def generate_swift(self):
    if self.env["set_prop"]:
      keys = ['textspan', 'line-spacing', 'char-spacing']
      tspan, line_sp, char_sp = utils.get_vals(keys, self.info)
      contents = tspan[0].get('contents')
      if line_sp is not None or char_sp is not None:
        ind = self.id.find('.') # id_ is in the form "cell.{}" or "header.{}"
        self.id = self.id[ind+1:] # truncated id_
        return self.gen_attributed_tprop(tspan, line_sp, char_sp)
      return self.gen_text(contents)
    return self.setup_component()

  def create_attributed_str(self, text):
    """
    Args:
      text: (str) text of the attributed string.

    Returns: (str) swift code to create an attributed string.
    """
    return ('var {}AttributedStr = NSMutableAttributedString(string: "{}")\n'
           ).format(self.id, text)

  def gen_text(self, txt):
    """
    Args:
      txt: (str) text

    Returns: (str) swift code to set the text property
    """
    txt = txt.decode('utf-8')
    return '{}.text = "{}"\n'.format(self.id, txt)

  def gen_attributed_text(self, str_id):
    """
    Args:
      str_id (str): id of attributed string

    Returns: (str) swift code to set the attributedText property.
    """
    return ("{}.attributedText = {}\n").format(self.id, str_id)

  def gen_text_color(self, color):
    """
    Args:
      color: (tuple) contains r, g, b values representing the text color

    Returns: (str) swift code to set the text color
    """
    return ("{}.textColor = {}\n").format(self.id, utils.create_uicolor(color))

  def center_and_wrap(self, text_align):
    """
    Args:
      text_align: (str) alignment of text (either left, center, or right)

    Returns: (str) swift code to center text and wrap lines
    """
    return ("{}.textAlignment = .{}\n{}.numberOfLines = 0\n"
            "{}.lineBreakMode = .byWordWrapping\n"
           ).format(self.id, text_align, self.id, self.id)

  def gen_font_family_size(self, font, size):
    """
    Args:
      font: (str) font name
      size: (int) size of the font

    Returns:
      (str) swift code to set font-family and size of the title
    """
    return ("{}.font = {}\n").format(self.id, super().create_font(font, size))

  def gen_num_of_lines(self):
    """
    Returns: (str) swift code to set numberOfLines to 0
    """
    return "{}.numberOfLines = 0\n".format(self.id)

  def gen_substring_color(self, str_id, color, start, length):
    """
    Args:
      str_id: (string) variable name of the string
      color: (tuple) r, g, b
      start: (int) index of first character to change
      length: (int) number of characters to change the color of from [start]

    Returns: (str) The swift code to set a substring of str to be [color]
    """
    return ("{}.addAttribute(.foregroundColor, value: {})"
            ", range: NSRange(location: {}, length: {}))\n"
           ).format(str_id, utils.create_uicolor(color), start, length)

  def gen_attributed_color(self, str_id, color):
    """
    Args:
      str_id: (string) variable name of the string
      color: (tuple) r, g, b

    Returns:
      (str) The swift code to set the color of an attributed string to be
      a color.
    """
    return ("{}.addAttribute(.foregroundColor, value: {}"
            ", range: NSRange(location: 0, length: {}.length))\n"
           ).format(str_id, utils.create_uicolor(color), str_id)

  def gen_substring_font(self, str_id, font, size, start, length):
    """
    Args:
      str_id: (string) variable name of the string
      font: (string) the font of the substring
      start: (int) index of first character whose font is being changed
      length: (int) number of characters to change the font of from [start]

    Returns: (str) swift code to set a substring of str to be a font.
    """
    return ("{}.addAttribute(.font, value: {}"
            ", range: NSRange(location: {}, length: {}))\n"
           ).format(str_id, super().create_font(font, size), start, length)

  def gen_attributed_font(self, str_id, font, size):
    """
    Args:
      str_id: (string) the variable name of string that is to be edited
      font: (string) the font family name
      size: (int) the font size

    Returns: (str) The swift code to set the font of an attributed string.
    """
    return ("{}.addAttribute(.font, value: {}"
            ", range: NSRange(location: 0, length: {}.length))\n"
           ).format(str_id, super().create_font(font, size), str_id)

  def gen_line_sp(self, str_id, line_sp):
    """
    Args:
      str_id: (str) variable name of the string
      line_sp: (str) line spacing, in pixels

    Returns:
      (str) The swift code to set the line spacing of an attributed string
    """
    return ('let {}ParaStyle = NSMutableParagraphStyle()\n'
            '{}ParaStyle.lineSpacing = {}\n'
            '{}.addAttribute(.paragraphStyle, value: {}ParaStyle, range: '
            'NSRange(location: 0, length: {}.length))\n'
           ).format(self.id, self.id, line_sp, str_id, self.id, str_id)

  def gen_char_sp(self, str_id, char_sp):
    """
    Args:
      str_id (str): variable name of the string
      char_sp (str): character spacing, in pixels

    Returns (str): Swift code to set the char-spacing of an attributed string
    """
    return ('{}.addAttribute(.kern, value: {}, range: '
            'NSRange(location: 0, length: {}.length))\n'
           ).format(str_id, char_sp, str_id)

  def gen_attributed_tprop(self, tspan, line_sp, char_sp):
    """
    Args:
      tspan: (dict list) see generate_component docstring for more info
      line_sp: (int) line spacing, in pixels
      char_sp: (int) character spacing, in pixels

    Returns:
      (str) swift code to setup and set the attributed text prop of a label.
      Note: Assumes that the content of the textspans do not vary.
    """
    txt = tspan[0]
    keys = ['contents', 'fill', 'font-family', 'font-size']
    contents, fill, font, size = utils.get_vals(keys, txt)
    contents = contents.decode('utf-8')

    C = self.create_attributed_str(contents)
    str_id = '{}AttributedStr'.format(self.id)
    C += self.gen_attributed_color(str_id, fill)
    C += self.gen_attributed_font(str_id, font, size)
    if line_sp is not None:
      line_sp = str(float(line_sp) / float(size))
      C += self.gen_line_sp(str_id, line_sp)
    if char_sp is not None:
      C += self.gen_char_sp(str_id, char_sp)
    C += self.gen_attributed_text(str_id)
    return C

  def setup_component(self):
    """
    Returns: (str) The swift code to apply all the properties from textspan
    """
    keys = ['textspan', 'line-spacing', 'char-spacing']
    tspan, line_sp, char_sp = [self.info.get(k) for k in keys]
    C = ""
    if len(tspan) == 1: # the contents of the textspan don't vary
      txt = tspan[0]
      contents = txt.get('contents')
      fill = txt.get('fill')
      txt_align = txt.get('text-align')
      font = txt.get('font-family')
      size = txt.get('font-size')
      in_v = self.env["in_view"]

      if (line_sp is not None or char_sp is not None) and not in_v:
        C += self.gen_attributed_tprop(tspan, line_sp, char_sp)
      elif not in_v:
        C += self.gen_text(contents) if contents != None else ""
        C += self.gen_text_color(fill) if fill != None else ""
        C += self.gen_font_family_size(font, size)
      elif (line_sp is None and char_sp is None) and in_v:
        C += self.gen_text_color(fill) if fill != None else ""
        C += self.gen_font_family_size(font, size)

      if txt_align is None:
        C += self.center_and_wrap("center")
      else:
        C += self.center_and_wrap(txt_align)
      return C

    else:
      raise Exception("Textspan in label contains varying text.")
      #TODO: Case for varying text.
