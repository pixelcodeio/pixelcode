from . import *

class UILabel(BaseComponent):
  """
  Class representing a UILabel in swift
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
    Returns (str): swift code to create an attributed string.
    """
    return ('let {}AttributedStr = NSMutableAttributedString(string: "{}")\n'
           ).format(self.id, text)

  def gen_text(self, text):
    """
    Returns: (str) swift code to set the text property
    """
    text = text.decode('utf-8')
    return '{}.text = "{}"\n'.format(self.id, text)

  def gen_attributed_text(self, str_id):
    """
    Returns (str): swift code to set the attributedText property.
    """
    if self.env["in_cell"]:
      self.id = ("cell.{}").format(self.id)
    elif self.env["in_header"]:
      self.id = ("header.{}").format(self.id)
    return ("{}.attributedText = {}\n").format(self.id, str_id)

  def gen_text_color(self, color):
    """
    Returns (str): swift code to set the text color
    """
    return ("{}.textColor = {}\n").format(self.id, utils.create_uicolor(color))

  def center_and_wrap(self, text_align):
    """
    Args:
      text_align (str): either left, center, or right

    Returns (str): swift code to center text and wrap lines
    """
    return ("{0}.textAlignment = .{1}\n{0}.numberOfLines = 0\n"
            "{0}.lineBreakMode = .byWordWrapping\n"
           ).format(self.id, text_align)

  def gen_font_family_size(self, font, size):
    """
    Returns (str): swift code to set font-family and size
    """
    return ("{}.font = {}\n").format(self.id, super().create_font(font, size))

  def gen_num_of_lines(self):
    """
    Returns: (str) swift code to set numberOfLines to 0
    """
    return "{}.numberOfLines = 0\n".format(self.id)

  def gen_add_attribute(self, str_id, attr, value, range_):
    """
    Returns (str): swift code to add attribute to a string
    """
    return ("{}.addAttribute({}, value: {}, range: NSRange(location: {}, "
            "length: {}))\n").format(str_id, attr, value, range_[0], range_[1])

  def gen_attributed_color(self, str_id, color):
    """
    Returns (str): swift code to set color
    """
    color = utils.create_uicolor(color)
    return self.gen_add_attribute(str_id, '.foregroundColor', color,
                                  [0, str_id + '.length'])

  def gen_attributed_font(self, str_id, font, size):
    """
    Returns: (str) swift code to set font
    """
    f = super().create_font(font, size)
    return self.gen_add_attribute(str_id, '.font', f, [0, str_id + '.length'])

  def gen_line_sp(self, str_id, line_sp):
    """
    Returns: (str) swift code to set line spacing
    """
    attr = self.gen_add_attribute(str_id, '.paragraphStyle',
                                  self.id + 'ParaStyle', [0, 'str_id.length'])
    return ('let {0}ParaStyle = NSMutableParagraphStyle()\n'
            '{0}ParaStyle.lineSpacing = {1}\n'
            '{2}'
           ).format(self.id, line_sp, attr)

  def gen_char_sp(self, str_id, char_sp):
    """
    Returns (str): swift code to set char-spacing
    """
    return self.gen_add_attribute(str_id, '.kern', char_sp,
                                  [0, str_id + '.length'])

  def gen_attributed_tprop(self, tspan, line_sp, char_sp):
    """
    Returns (str): swift code to setup/set the attributed text property
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
    Returns (str): The swift code to setup uilabel
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
      raise Exception("UILabel: Textspan label contains varying text.")
      #TODO: Case for varying text.
