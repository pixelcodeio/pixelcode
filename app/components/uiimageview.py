import components.utils as utils

class UIImageView(object):
  """
  Class representing an UIImageView in swift
  """
  def __init__(self):
    pass

  def set_image(self, elem):
    """
    Returns: The swift code to set the image of elem.
    """
    return ("{}.image = UIImage(named: \"{}\")\n").format(elem, elem)
