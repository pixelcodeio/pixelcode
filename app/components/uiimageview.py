import components.utils as utils

class UIImageView(object):
  """
  Class representing an UIImageView in swift
  """
  def __init__(self):
    pass

  def set_image(self, elem, image_fname):
    """
    Args:
      elem: (str) id of the component
      image_fname: (str) name of the image file

    Returns: The swift code to set the image of elem.
    """
    index = image_fname.index(".")
    image_name = image_fname[0:index]
    return ("{}.image = UIImage(named: \"{}\")\n").format(elem, image_name)

  def set_opacity(self, elem, opacity):
    """
    Args:
      elem: (str) id of the component
      opacity: (float) between 0 and 1

    Returns: The swift code to set the opacity of elem.
    """
    if opacity != None:
      return "{}.alpha = {}".format(elem, opacity)

  def setup_uiimageview(self, elem, image):
    """
    Args:
      elem: (str) id of the component
      image: (dict) see generate_component docstring for more information.

    Returns: The swift code to apply all the properties from text to elem.
    """
    path = image['path']
    opacity = image['opacity']
    stroke_c = image['stroke-color']
    stroke_w = image['stroke-width']
    c = self.set_image(elem, path)
    c += self.set_opacity(elem, opacity)
    c += utils.set_border_color(elem, stroke_c) if stroke_c != None else ""
    c += utils.set_border_width(elem, stroke_w) if stroke_w != None else ""
