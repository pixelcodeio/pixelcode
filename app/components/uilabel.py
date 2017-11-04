import components.utils as utils

class UILabel(object):
  def __init__(self, info, bgColor):
    """
    Args:
      info: Refer to generate_label for documentation of info.
      bgColor: (tuple) Background color of label as r, g, b values

    Returns: UILabel object with the necessary swift code
    """
    self.bgColor = bgColor
    self.swift = self.generate_label(info)
    return

  def set_text(self, elem, txt):
    """
    Returns: The swift code to set the text of elem to be txt
    """
    return '{}.text = "{}"\n'.format(elem, txt)

  def set_text_color(self, elem, color):
    """
    Returns: The swift code to set the text color of elem to be color
    """
    r = color[0]
    g = color[1]
    b = color[2]
    return ("{}.textColor = UIColor(red: {}/255.0, green: {}/255.0, "
            "blue: {}/255.0, alpha: 1.0)\n"
           ).format(elem, r, g, b)

  def set_bg_color(self, elem):
    """
    Returns: The swift code to set the background color of elem.
    """
    r = self.bgColor[0]
    g = self.bgColor[1]
    b = self.bgColor[2]
    return ("{}.backgroundColor = UIColor(red: {}/255.0, green: {}/255.0, "
            "blue: {}/255.0, alpha: 1.0)\n"
           ).format(elem, r, g, b)

  def center_and_wrap(self, elem):
    """
    Returns: The swift code to center the text and wrap lines
    """
    return ("{}.textAlignment = .center\n{}.numberOfLines = 0\n"
            "{}.lineBreakMode = .byWordWrapping\n"
           ).format(elem, elem, elem)

  def set_font_size(self, elem, size):
    """
    Returns: The swift code to set the font size of elem to be size
    """
    return '{}.font = UIFont.systemFont(ofSize: {})\n'.format(elem, size)

  def generate_label(self, info):
    """
    Args:
      info: is a dictionary of keys:
        - id: (str) name of view
        - text: (str) text that is to be displayed
        - text-color: (tuple) r, g, b values of the text color
        - font-size: (int) font-size of the text
        - x: (float) x-coor of view's center as percentage of screen's width
        - y: (float) y-coor of view's center as percentage of screen's height
        - vertical: (dict) dict containing constraints for top/bottom of view
        - horizontal: (dict) dict containing constraints for left/right of view
        - width: (float) width of view as percentage of screen's width
        - height: (float) height of view as percentage of screen's height

    Returns: The swift code to generate a label with a text
    """
    vertical = info['vertical']
    horizontal = info['horizontal']
    verticalDir = vertical['direction']
    verticalID = vertical['id']
    verticalDist = vertical['distance']
    horizontalDir = horizontal['direction']
    horizontalID = horizontal['id']
    horizontalDist = horizontal['distance']
    centerX = info['x']
    centerY = info['y']
    width = info['width']
    height = info['height']
    lid = info['id']
    txt = info['text']
    txtColor = info['text-color']
    fontSize = info['font-size']
    label = 'var {} = UILabel()\n'.format(lid)
    label += utils.translates_false(lid)
    label += self.set_text(lid, txt)
    label += self.set_text_color(lid, txtColor)
    label += self.set_bg_color(lid)
    label += self.set_font_size(lid, fontSize)
    label += self.center_and_wrap(lid)
    label += utils.add_subview('view', lid)
    label += utils.wh_constraints(lid, width, height)
    label += utils.position_constraints(
        lid, horizontalID, horizontalDir, horizontalDist, verticalID,
        verticalDir, verticalDist, centerX, centerY)
    return label
