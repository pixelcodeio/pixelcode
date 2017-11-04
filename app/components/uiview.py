import components.utils as utils

class UIView(object):
  def __init__(self, info):
    """
    Args:
      info: Refer to generate_view for documentation of info

    Returns: UIView object with the necessary swift code
    """
    self.swift = self.generate_view(info)
    return

  def generate_view(self, info):
    """
    Args:
      info: is a dictionary of keys:
        - id: (str) name of view
        - x: (float) x-coor of view's center as percentage of screen's width
        - y: (float) y-coor of view's center as percentage of screen's height
        - vertical: (dict) dict containing constraints for top/bottom of view
        - horizontal: (dict) dict containing constraints for left/right of view
        - fill: (optional tuple) r, g, b values for background color. Has value
                None if no value is provided
        - width: (float) width of view as percentage of screen's width
        - height: (float) height of view as percentage of screen's height

    Returns:
      Uses properties from info to generate swift code that creates a UIView.
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
    rid = info['id']
    view = 'var {} = UIView()\n'.format(rid)
    view += utils.translates_false(rid)
    if fill != None:
      r = fill[0]
      g = fill[1]
      b = fill[2]
      view += utils.set_bg(rid, r, g, b)
    view += utils.add_subview('view', rid)
    view += utils.wh_constraints(rid, width, height)
    view += utils.position_constraints(
        rid, horizontalID, horizontalDir, horizontalDist, verticalID,
        verticalDir, verticalDist, centerX, centerY)
    return view
