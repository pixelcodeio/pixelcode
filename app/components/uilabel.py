import components.utils as utils

class UILabel(object):
  def __init__(self, info):
    """
    Args:
      info: Refer to generate_label for documentation of info.

    Returns: UILabel object with the necessary swift code
    """
    self.swift = self.generate_label(info)
    return

  def set_text(self, elem, txt):
    """
    Returns: The swift code to set the text of elem to be txt
    """
    return '{}.text = {}'.format(elem, txt)

  def set_font_size(self, elem, size):
    """
    Returns: The swift code to set the font size of elem to be size
    """
    return '{}.font = UIFont.systemFont(ofSize: {})'.format(elem, size)

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
    info['fill'] = (0, 0, 0) # TODO: fix this
    fill = info['fill']
    r = fill[0]
    g = fill[1]
    b = fill[2]
    lid = info['id']
    txt = info['text']
    fontSize = info['font-size']
    label = 'var {} = UILabel()\n'.format(lid)
    label += utils.translates_false(lid)
    label += self.set_text(lid, txt)
    label += self.set_font_size(lid, fontSize)
    label += utils.set_bg(lid, r, g, b)
    label += utils.add_subview('view', lid)
    label += utils.wh_constraints(lid, width, height)
    label += utils.position_constraints(
        lid, horizontalID, horizontalDir, horizontalDist, verticalID,
        verticalDir, verticalDist, centerX, centerY)
    return label
