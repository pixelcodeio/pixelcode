import utils

class UIImageView:
  def generate_img_view(self, info):
    """
    info requires:
      - id of image view
      - image
      - centerX & centerY
      - top/bottom & left/right
      - background color
      - width & height
      - corner radius
    Returns: The swift code to generate an image view
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
    imgID = info['id']
    imgView = 'var {} = UIImageView()\n'.format(imgID)
    imgView += utils.translates_false(imgID)
    imgView += utils.set_bg(imgID, r, g, b)
    imgView += utils.add_subview('view', imgID)
    imgView += utils.wh_constraints(imgID, width, height)
    imgView += utils.position_constraints(imgID, horizontalID, horizontalDir,
      horizontalDist, verticalID, verticalDir, verticalDist, centerX, centerY)
    return imgView
