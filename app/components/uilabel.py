import utils

class UILabel:
  def set_text(self, elem, txt):
    """
    Returns: The swift code to set the text of a label
    """
    return '{}.text = {}'.format(elem, txt)

  def set_font_size(self, elem, size):
    """
    Returns: The swift code to set the font size of a label
    """
    return '{}.font = UIFont.systemFont(ofSize: {})'.format(elem, size)

  def generate_label(self, info):
    """
    info requires:
      - id of label
      - text & fontsize & text color
      - centerX & centerY
      - top/bottom & left/right
      - background color
      - width & height
      - corner radius
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
    fill = info['fill']
    r = fill[0]
    g = fill[1]
    b = fill[2]
    lid = info['id']
    txt = info['text']
    fontSize = info['fontSize']
    label = 'var {} = UILabel()\n'.format(lid)
    label += utils.translates_false(lid)
    label += self.set_text(lid, txt)
    label += self.set_font_size(lid, fontSize)
    label += utils.set_bg(lid, r, g, b)
    label += utils.add_subview('view', lid)
    label += utils.wh_constraints(lid, width, height)
    label += utils.position_constraints(lid, horizontalID, horizontalDir,
      horizontalDist, verticalID, verticalDir, verticalDist, centerX, centerY)
    return label
