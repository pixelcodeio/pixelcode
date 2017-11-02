import utils

class UIButton:
  def __init__(self):
    pass

  def set_title(self, elem, title):
    """
    Returns: The swift code to set title of a button
    """
    return '{}.setTitle({}, for: .normal)'.format(elem, title)

  def set_title_color(self, elem, r, g, b):
    """
    Returns: The swift code to set title color of a button
    """
    color = 'UIColor(red: {}, green: {}, blue: {}, alpha: 1.0)'.format(r, g, b)
    return '{}.setTitleColor({}, for: .normal)'.format(elem, color)

  def set_font_size(self, elem, size):
    """
    Returns: The swift code to set the font size of a button
    """
    font = 'UIFont.systemFont(ofSize: {})'.format(size)
    return '{}.titleLabel.font = {}'.format(elem, font)

  def generate_button(self, info):
    """
    info requires:
      - id of button
      - button title & fontsize & title color
      - centerX & centerY
      - top/bottom & left/right
      - background color
      - width & height
      - corner radius
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
    button += utils.position_constraints(bid, horizontalID, horizontalDir,
      horizontalDist, verticalID, verticalDir, verticalDist, centerX, centerY)
    return button
