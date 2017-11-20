import components.utils as utils

class UILabel(object):
  def __init__(self, bgColor):
    """
    Args:
      bgColor: (tuple) Background color of label as r, g, b values
    """
    self.bgColor = bgColor

  def create_attributed_str(self, elem, text):
    """
    Args:
      elem: (str) id of element
      text: (str) text of the attributed string.

    Returns: The swift code to create an attributed string.
    """
    return ('var {}AttributedStr = NSMutableAttributedString(string: "{}")\n'
           ).format(elem, text)

  def set_text(self, elem, txt):
    """
    Args:
      elem: (str) id of element
      txt: (str) text to set elem's text property to

    Returns: The swift code to set the text of elem to be txt
    """
    return '{}.text = "{}"\n'.format(elem, txt)

  def set_attributed_text(self, elem, strID):
    """
    Args:
      elem: (str) id of element
      strID: (str) id of attributed string

    Returns: The swift code to set the attributedText property of elem.
    """
    return ("{}.attributedText = {}\n").format(elem, strID)

  def set_text_color(self, elem, color, opacity):
    """
    Args:
      elem: (str) id of element
      color: (tuple) contains r, g, b values representing the text color
      opacity: (float) between 0 and 1

    Returns: The swift code to set the text color of elem to be color
    """
    o = "1.0" if opacity is None else opacity
    r, g, b = color
    return ("{}.textColor = UIColor(red: {}/255.0, green: {}/255.0, "
            "blue: {}/255.0, alpha: {})\n"
           ).format(elem, r, g, b, o)

  def center_and_wrap(self, elem, textAlign):
    """
    Args:
      elem: (str) id of element
      textAlign: (str) alignment of text (either left, center, or right)

    Returns: The swift code to center the text and wrap lines
    """
    return ("{}.textAlignment = .{}\n{}.numberOfLines = 0\n"
            "{}.lineBreakMode = .byWordWrapping\n"
           ).format(elem, textAlign, elem, elem)

  def set_font_size(self, elem, size):
    """
    Args:
      elem: (str) id of element
      size: (int) size of the font

    Returns: The swift code to set the font size of elem to be size
    """
    return '{}.font = UIFont.systemFont(ofSize: {})\n'.format(elem, size)

  def set_font_size_weight(self, elem, size, weight):
    """
    Args:
      elem: (str) id of element
      size: (int) size of the font
      weight: (int) weight of the font

    Returns: The swift code to set the font size and weight of elem.
    """
    return ("{}.font = UIFont.systemFont(ofSize: {}, weight: "
            "UIFont.Weight.init(rawValue: {}))\n"
           ).format(elem, size, weight)

  def set_font_family_size(self, elem, font, size):
    """
    Args:
      elem: (str) id of element
      font: (str) font name
      size: (int) size of the font

    Returns: The swift code to set the font family and size of the title in elem
    """
    return ("{}.font = UIFont(name: \"{}\", size: {})\n"
           ).format(elem, font, size)

  def set_num_of_lines(self, elem):
    """
    Args:
      elem: (str) id of element

    Returns: The swift code to set numberOfLines to be 0 for elem.
    """
    return "{}.numberOfLines = 0\n".format(elem)

  def set_substring_color(self, strID, color, start, length):
    """
    Args:
      strID: (string) the variable name of string that is to be edited
      color: (tuple) contains r, g, b values representing the color of substring
      start: (int) index of first character whose color is being changed
      length: (int) number of characters from start index whose color is being
              changed.

    Returns: The swift code to set a substring of str to be a color with r,g,b
             values.
    """
    r, g, b = color
    c = ("UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha)"
         ": 1.0)"
        ).format(r, g, b)
    return ("{}.addAttribute(.foregroundColor, value: {})"
            ", range: NSRange(location: {}, length: {}))\n"
           ).format(strID, c, start, length)

  def set_attributed_color(self, strID, color, opacity):
    """
    Args:
      strID: (string) the variable name of string that is to be edited
      color: (tuple) contains r, g, b values representing the color

    Returns: The swift code to set the color of an attributed string to be a
    color.
    """
    o = "1.0"
    if opacity:
      o = '{}'.format(opacity)
    r, g, b = color
    c = ("UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha"
         ": {})"
        ).format(r, g, b, o)
    return ("{}.addAttribute(.foregroundColor, value: {}"
            ", range: NSRange(location: 0, length: {}.length))\n"
           ).format(strID, c, strID)

  def set_substring_font(self, strID, font, size, start, length):
    """
    Args:
      strID: (string) the variable name of string that is to be edited
      font: (string) the font of the substring
      start: (int) index of first character whose font is being changed
      length: (int) number of characters from start index whose font is being
              changed.

    Returns: The swift code to set a substring of str to be a font.
    """
    f = ('UIFont(name: "{}", size: {})').format(font, size)
    return ("{}.addAttribute(.font, value: {}"
            ", range: NSRange(location: {}, length: {}))\n"
           ).format(strID, f, start, length)

  def set_attributed_font(self, strID, font, size):
    """
    Args:
      strID: (string) the variable name of string that is to be edited
      font: (string) the font family name
      size: (int) the font size

    Returns: The swift code to set the font of an attributed string.
    """
    f = ('UIFont(name: "{}", size: {})').format(font, size)
    return ("{}.addAttribute(.font, value: {}"
            ", range: NSRange(location: 0, length: {}.length))\n"
           ).format(strID, f, strID)

  def set_line_sp(self, elem, strID, line_sp):
    """
    Returns: The swift code to set the line spacing of an
    attributed string
    """
    return ('let {}ParaStyle = NSMutableParagraphStyle()\n'
            '{}ParaStyle.lineSpacing = {}\n'
            '{}.addAttribute(.paragraphStyle, value: {}ParaStyle, range: '
            'NSRange(location: 0, length: {}.length))\n'
           ).format(elem, elem, line_sp, strID, elem, strID)

  def set_char_sp(self, elem, strID, char_sp):
    """
    Returns: The swift code to set the character spacing of an
    attributed string
    """
    return ('{}.addAttribute(.kern, value: {}, range: '
            'NSRange(location: 0, length: {}.length))\n'
           ).format(strID, char_sp, strID)

  def setup_cell_or_header_attr_text(self, elem, textspan, line_sp, char_sp):
    """
    Returns: The swift code to set the attributed text of a label when called
    from a UITableView's cellForRowAt function.
    """
    if len(textspan) == 1:
      # the contents of the textspan don't vary
      txt = textspan[0]
      contents = txt.get('contents')
      fill = txt.get('fill')
      txt_align = txt.get('text-align')
      font = txt.get('font-family')
      size = txt.get('font-size')
      opacity = txt.get('opacity')

      c = self.create_attributed_str(elem, contents)
      strID = '{}AttributedStr'.format(elem)
      c += self.set_attributed_color(strID, fill, opacity)
      c += self.set_attributed_font(strID, font, size)
      if line_sp:
        ls = str(float(line_sp) / float(size))
        c += self.set_line_sp(elem, strID, ls)
      if char_sp:
        c += self.set_char_sp(elem, strID, char_sp)
      cellComp = 'cell.{}'.format(elem)
      c += self.set_attributed_text(cellComp, strID)
      return c
    else:
      raise Exception("Textspan in label contains varying text.")
      #TODO: Case for varying text.

  def setup_uilabel(self, elem, textspan, line_sp, char_sp, inView=False):
    """
    Args:
      elem: (str) id of the component
      textspan: (dict array) see generate_component docstring for more
                information.
      line_sp: (int) the value representing the line spacing
      char_sp: (int) the value representing the character spacing

    Returns: The swift code to apply all the properties from textspan to elem.
    """
    if len(textspan) == 1:
      # the contents of the textspan don't vary
      txt = textspan[0]
      contents = txt.get('contents')
      fill = txt.get('fill')
      txt_align = txt.get('text-align')
      font = txt.get('font-family')
      size = txt.get('font-size')
      opacity = txt.get('opacity')

      c = ""
      if (line_sp or char_sp) and not inView:
        c += self.create_attributed_str(elem, contents)
        strID = '{}AttributedStr'.format(elem)
        c += self.set_attributed_color(strID, fill, opacity)
        c += self.set_attributed_font(strID, font, size)
        if line_sp:
          ls = str(float(line_sp) / float(size))
          c += self.set_line_sp(elem, strID, ls)
        if char_sp:
          c += self.set_char_sp(elem, strID, char_sp)
        c += self.set_attributed_text(elem, strID)
      elif not inView:
        c += self.set_text(elem, contents) if contents != None else ""
        c += self.set_text_color(elem, fill, opacity) if fill != None else ""
        c += self.set_font_family_size(elem, font, size)
      elif (line_sp is None and char_sp is None) and inView:
        c += self.set_text_color(elem, fill, opacity) if fill != None else ""
        c += self.set_font_family_size(elem, font, size)

      if txt_align is None:
        c += self.center_and_wrap(elem, "center")
      else:
        c += self.center_and_wrap(elem, txt_align)
      return c

    else:
      raise Exception("Textspan in label contains varying text.")
      #TODO: Case for varying text.
