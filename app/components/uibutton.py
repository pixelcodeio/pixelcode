import components.utils as utils

class UIButton(object):
  def __init__(self, info):
    """
    Args:
      info: Refer to generate_button for documentation of info

    Returns: UIButton object with the necessary swift code
    """
    self.swift = self.generate_button(info)
    return

  def set_title(self, elem, title):
    """
    Returns: The swift code to set title of a elem using title
    """
    return '{}.setTitle(\"{}\", for: .normal)\n'.format(elem, title)

  def set_title_color(self, elem, color):
    """
    Returns: The swift code to set title color of elem using the r, g, b values
    """
    r = color[0]
    g = color[1]
    b = color[2]
    c = ('UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha: 1.0)'
        ).format(r, g, b)
    return '{}.setTitleColor({}, for: .normal)\n'.format(elem, c)

  def set_font_size(self, elem, size):
    """
    Returns: The swift code to set the font size of elem using size
    """
    font = 'UIFont.systemFont(ofSize: {})'.format(size)
    return '{}.titleLabel?.font = {}\n'.format(elem, font)

  def set_font_size_weight(self, elem, size, weight):
    """
    Returns: The swift code to set the font size and weight of elem.
    """
    return ("{}.titleLabel?.font = UIFont.systemFont(ofSize: {}, weight: "
            "UIFont.Weight.init(rawValue: {}))\n"
           ).format(elem, size, weight)

  def set_font_family(self, elem, font, size):
    """
    Returns: The swift code to set the font family and size of the title in elem
    """
    return ("{}.titleLabel?.font = UIFont(name: \"{}\", size: {})\n"
           ).format(elem, font, size)

  def generate_button(self, info):
    """
    Args:
      info: is a dictionary of keys:
        - id: (str) name of view
        - title: (str) title that is to be displayed on the button
        - title-color: (tuple) r, g, b values of the title color
        - font-size: (int) font-size of the title
        - font-weight: (optional int) font weight of title. Has value None if
                       no value is provided
        - font-family: (str) name of the font of title
        - x: (float) x-coor of view's center as percentage of screen's width
        - y: (float) y-coor of view's center as percentage of screen's height
        - vertical: (dict) dict containing constraints for top/bottom of view
        - horizontal: (dict) dict containing constraints for left/right of view
        - fill: (optional tuple) r, g, b values for background color. Has value
                None if no value is provided
        - width: (float) width of view as percentage of screen's width
        - height: (float) height of view as percentage of screen's height
        - stroke-color: (optional tuple) r, g, b values representing the border
                        color. Has value None if no value is provided
        - stroke-width: (optional int) the number of pixels representing the
                        border width. Has value None if no value is provided
        - border-radius: (optional int) the number of pixels representing the
                         corner radius. Has value None if no value is provided

    Returns: The swift code to generate a button
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
    fill = info['fill']
    bid = info['id']
    title = info['title']
    titleColor = info['title-color']
    fontSize = info['font-size']
    fontW = info['font-weight']
    fontFamily = info['font-family']
    borColor = info['stroke-color']
    borWidth = info['stroke-width']
    corRad = info['border-radius']
    button = 'var {} = UIButton()\n'.format(bid)
    button += utils.translates_false(bid)
    button += self.set_title(bid, title)
    button += self.set_title_color(bid, titleColor)
    if fontW != None:
      button += self.set_font_size_weight(bid, fontSize, fontW)
    else:
      button += self.set_font_size(bid, fontSize)
    button += self.set_font_family(bid, fontFamily, fontSize)
    if fill != None:
      r = fill[0]
      g = fill[1]
      b = fill[2]
      button += utils.set_bg(bid, r, g, b)
    button += utils.set_border_color(bid, borColor) if borColor != None else ""
    button += utils.set_border_width(bid, borWidth) if borWidth != None else ""
    button += utils.set_corner_radius(bid, corRad) if corRad != None else ""
    button += utils.add_subview('view', bid)
    button += utils.wh_constraints(bid, width, height)
    button += utils.position_constraints(
        bid, horizontalID, horizontalDir, horizontalDist, verticalID,
        verticalDir, verticalDist, centerX, centerY)
    return button