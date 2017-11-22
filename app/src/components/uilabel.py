import utils

class UILabel(object):
  def __init__(self, bgc):
    """
    Args:
      bgc: (tuple) Background color of label as r, g, b values
    """
    self.bgc = bgc

  def create_attributed_str(self, elem, text):
    """
    Args:
      elem: (str) id of element
      text: (str) text of the attributed string.

    Returns: (str) The swift code to create an attributed string.
    """
    return ('var {}AttributedStr = NSMutableAttributedString(string: "{}")\n'
           ).format(elem, text)

  def set_text(self, elem, txt):
    """
    Args:
      elem: (str) id of element
      txt: (str) text to set elem's text property to

    Returns: (str) The swift code to set the text of elem to be txt
    """
    return '{}.text = "{}"\n'.format(elem, txt)

  def set_attributed_text(self, elem, str_id):
    """
    Args:
      elem: (str) id of element
      str_id: (str) id of attributed string

    Returns: (str) The swift code to set the attributedText property of elem.
    """
    return ("{}.attributedText = {}\n").format(elem, str_id)

  def set_text_color(self, elem, color):
    """
    Args:
      elem: (str) id of element
      color: (tuple) contains r, g, b values representing the text color

    Returns: (str) The swift code to set the text color of elem to be color
    """
    return ("{}.textColor = {}\n").format(elem, utils.create_uicolor(color))

  def center_and_wrap(self, elem, text_align):
    """
    Args:
      elem: (str) id of element
      text_align: (str) alignment of text (either left, center, or right)

    Returns: (str) The swift code to center the text and wrap lines
    """
    return ("{}.textAlignment = .{}\n{}.numberOfLines = 0\n"
            "{}.lineBreakMode = .byWordWrapping\n"
           ).format(elem, text_align, elem, elem)

  def set_font_family_size(self, elem, font, size):
    """
    Args:
      elem: (str) id of element
      font: (str) font name
      size: (int) size of the font

    Returns:
      (str) The swift code to set the font family and size of the
      title in elem
    """
    return ("{}.font = {}\n"
           ).format(elem, utils.create_font(font, size))

  def set_num_of_lines(self, elem):
    """
    Args:
      elem: (str) id of element

    Returns: (str) The swift code to set numberOfLines to be 0 for elem.
    """
    return "{}.numberOfLines = 0\n".format(elem)

  def set_substring_color(self, str_id, color, start, length):
    """
    Args:
      str_id: (string) the variable name of string that is to be edited
      color: (tuple) contains r, g, b values representing the color of substring
      start: (int) index of first character whose color is being changed
      length: (int) number of characters from start index whose color is being
              changed.

    Returns:
      (str) The swift code to set a substring of str to be a color with
      r,g,b values.
    """
    return ("{}.addAttribute(.foregroundColor, value: {})"
            ", range: NSRange(location: {}, length: {}))\n"
           ).format(str_id, utils.create_uicolor(color), start, length)

  def set_attributed_color(self, str_id, color):
    """
    Args:
      str_id: (string) the variable name of string that is to be edited
      color: (tuple) contains r, g, b values representing the color

    Returns:
      (str) The swift code to set the color of an attributed string to be
      a color.
    """
    return ("{}.addAttribute(.foregroundColor, value: {}"
            ", range: NSRange(location: 0, length: {}.length))\n"
           ).format(str_id, utils.create_uicolor(color), str_id)

  def set_substring_font(self, str_id, font, size, start, length):
    """
    Args:
      str_id: (string) the variable name of string that is to be edited
      font: (string) the font of the substring
      start: (int) index of first character whose font is being changed
      length: (int) number of characters from start index whose font is being
              changed.

    Returns: (str) The swift code to set a substring of str to be a font.
    """
    return ("{}.addAttribute(.font, value: {}"
            ", range: NSRange(location: {}, length: {}))\n"
           ).format(str_id, utils.create_font(font, size), start, length)

  def set_attributed_font(self, str_id, font, size):
    """
    Args:
      str_id: (string) the variable name of string that is to be edited
      font: (string) the font family name
      size: (int) the font size

    Returns: (str) The swift code to set the font of an attributed string.
    """
    return ("{}.addAttribute(.font, value: {}"
            ", range: NSRange(location: 0, length: {}.length))\n"
           ).format(str_id, utils.create_font(font, size), str_id)

  def set_line_sp(self, elem, str_id, line_sp):
    """
    Args:
      elem: (str) id of the element
      str_id: (str) the variable name of string that is to be edited
      line_sp: (str) the number of pixels representing the line spacing

    Returns:
      (str) The swift code to set the line spacing of an attributed string
    """
    return ('let {}ParaStyle = NSMutableParagraphStyle()\n'
            '{}ParaStyle.lineSpacing = {}\n'
            '{}.addAttribute(.paragraphStyle, value: {}ParaStyle, range: '
            'NSRange(location: 0, length: {}.length))\n'
           ).format(elem, elem, line_sp, str_id, elem, str_id)

  def set_char_sp(self, elem, str_id, char_sp):
    """
    Args:
      elem: (str) id of the element
      str_id: (str) the variable name of string that is to be edited
      char_sp: (str) the number of pixels representing the character spacing

    Returns:
      (str) The swift code to set the character spacing of an
      attributed string
    """
    return ('{}.addAttribute(.kern, value: {}, range: '
            'NSRange(location: 0, length: {}.length))\n'
           ).format(str_id, char_sp, str_id)

  def setup_attr_text(self, elem, textspan, ls, cs, in_c=False, in_h=False):
    """
    Args:
      elem: (str) id of the element
      textspan: (dict list) see generate_component docstring for more
                information.
      line_sp: (int) the value representing the line spacing
      char_sp: (int) the value representing the character spacing
      in_c: (bool) represents whether text is being set in tableview cell file
      in_h: (bool) represents whether text is being set in tableview header file

    Returns:
      (str) The swift code to set the attributed text of a label.
      Note: Assumes that the content of the textspans do not vary.
    """
    txt = textspan[0]
    contents = txt.get('contents')
    fill = txt.get('fill')
    font = txt.get('font-family')
    size = txt.get('font-size')

    c = self.create_attributed_str(elem, contents)
    str_id = '{}AttributedStr'.format(elem)
    c += self.set_attributed_color(str_id, fill)
    c += self.set_attributed_font(str_id, font, size)
    if ls is not None:
      ls = str(float(ls) / float(size))
      c += self.set_line_sp(elem, str_id, ls)
    if cs is not None:
      c += self.set_char_sp(elem, str_id, cs)
    if in_c:
      e = 'cell.{}'.format(elem)
    elif in_h:
      e = 'header.{}'.format(elem)
    else:
      e = elem
    c += self.set_attributed_text(e, str_id)
    return c

  def setup_uilabel(self, elem, textspan, line_sp, char_sp, in_view=False):
    """
    Args:
      elem: (str) id of the component
      textspan: (dict list) see generate_component docstring for more
                information.
      line_sp: (int) the value representing the line spacing
      char_sp: (int) the value representing the character spacing

    Returns:
      (str) The swift code to apply all the properties from textspan to elem.
    """
    if len(textspan) == 1:
      # the contents of the textspan don't vary
      txt = textspan[0]
      contents = txt.get('contents')
      fill = txt.get('fill')
      txt_align = txt.get('text-align')
      font = txt.get('font-family')
      size = txt.get('font-size')

      c = ""
      if (line_sp is not None or char_sp is not None) and not in_view:
        c += self.setup_attr_text(elem, textspan, line_sp, char_sp)
      elif not in_view:
        c += self.set_text(elem, contents) if contents != None else ""
        c += self.set_text_color(elem, fill) if fill != None else ""
        c += self.set_font_family_size(elem, font, size)
      elif (line_sp is None and char_sp is None) and in_view:
        c += self.set_text_color(elem, fill) if fill != None else ""
        c += self.set_font_family_size(elem, font, size)

      if txt_align is None:
        c += self.center_and_wrap(elem, "center")
      else:
        c += self.center_and_wrap(elem, txt_align)
      return c

    else:
      raise Exception("Textspan in label contains varying text.")
      #TODO: Case for varying text.
