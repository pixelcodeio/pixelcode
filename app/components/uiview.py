import utils

class UIView:
  def generate_view(self, info):
    """
    info requires:
      - id of view
      - centerX & centerY
      - top/bottom & left/right
      - background color
      - width & height
    Returns: Uses properties from info to generate swift code
    that creates a UIView.
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
    rid = info['id']
    view = 'var {} = UIView()\n'.format(rid)
    view += utils.translates_false(rid)
    view += utils.set_bg(rid, r, g, b)
    view += utils.add_subview('view', rid)
    view += utils.wh_constraints(rid, width, height)
    view += utils.position_constraints(rid, horizontalID, horizontalDir,
      horizontalDist, verticalID, verticalDir, verticalDist, centerX, centerY)
    return view
