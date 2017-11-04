import components.utils as utils

class UIImageView(object):
  def __init__(self, info):
    """
    Args:
      info: Refer to generate_img_view for documentation of info

    Returns: UIImageView object with the necessary swift code
    """
    self.swift = self.generate_img_view(info)
    return

  def set_image(self, elem):
    """
    Returns: The swift code to set the image of elem.
    """
    return ("{}.image = UIImage(named: \"{}\")\n").format(elem, elem)

  def generate_img_view(self, info):
    """
    Args:
      info: is a dictionary of keys:
        - id: (str) name of view
        - x: (float) x-coor of view's center as percentage of screen's width
        - y: (float) y-coor of view's center as percentage of screen's height
        - vertical: (dict) dict containing constraints for top/bottom of view
        - horizontal: (dict) dict containing constraints for left/right of view
        - width: (float) width of view as percentage of screen's width
        - height: (float) height of view as percentage of screen's height
        - corner-radius: (float) corner radius as percentage of view's width

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
    imgID = info['id']
    imgView = 'var {} = UIImageView()\n'.format(imgID)
    imgView += utils.translates_false(imgID)
    imgView += self.set_image(imgID)
    imgView += utils.add_subview('view', imgID)
    imgView += utils.wh_constraints(imgID, width, height)
    imgView += utils.position_constraints(
        imgID, horizontalID, horizontalDir, horizontalDist, verticalID,
        verticalDir, verticalDist, centerX, centerY)
    return imgView
