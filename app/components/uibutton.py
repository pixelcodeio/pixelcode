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
    return '{}.setTitle({}, for: .normal)\n'.format(elem, title)

  def set_title_color(self, elem, r, g, b):
    """
    Returns: The swift code to set title color of elem using the r, g, b values
    """
    color = 'UIColor(red: {}, green: {}, blue: {}, alpha: 1.0)'.format(r, g, b)
    return '{}.setTitleColor({}, for: .normal)\n'.format(elem, color)

  def set_font_size(self, elem, size):
    """
    Returns: The swift code to set the font size of elem using size
    """
    font = 'UIFont.systemFont(ofSize: {})'.format(size)
    return '{}.titleLabel.font = {}\n'.format(elem, font)

  def generate_button(self, info):
    """
    Args:
      info: is a dictionary of keys:
        - id: (str) name of view
        - title: (str) title that is to be displayed on the button
        - title-color: (tuple) r, g, b values of the title color
        - font-size: (int) font-size of the title
        - x: (float) x-coor of view's center as percentage of screen's width
        - y: (float) y-coor of view's center as percentage of screen's height
        - vertical: (dict) dict containing constraints for top/bottom of view
        - horizontal: (dict) dict containing constraints for left/right of view
        - fill: (tuple) r, g, b values for background color
        - width: (float) width of view as percentage of screen's width
        - height: (float) height of view as percentage of screen's height
        - corner-radius: (float) corner radius as percentage of button's width

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
    r = fill[0]
    g = fill[1]
    b = fill[2]
    bid = info['id']
    title = info['title']
    button = 'var {} = UIButton()\n'.format(bid)
    button += utils.translates_false(bid)
    button += self.set_title(bid, title)
    button += utils.set_bg(bid, r, g, b)
    button += utils.add_subview('view', bid)
    button += utils.wh_constraints(bid, width, height)
    button += utils.position_constraints(
        bid, horizontalID, horizontalDir, horizontalDist, verticalID,
        verticalDir, verticalDist, centerX, centerY)
    return button
