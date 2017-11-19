import components.utils as utils

class UIImageView(object):
  """
  Class representing an UIImageView in swift
  """
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
    return "{}.alpha = {}\n".format(elem, opacity)

  def setup_uiimageview(self, elem, info, inView=False):
    """
    Args:
      elem: (str) id of the component
      info: (dict) see generate_component docstring for more information.

    Returns: The swift code to apply all the properties from text to elem.
    """
    path = info.get('path')
    opacity = info.get('opacity')
    stroke_c = info.get('stroke-color')
    stroke_w = info.get('stroke-width')
    c = ""
    if inView is False:
      c += self.set_image(elem, path)
    if opacity is not None:
      c += self.set_opacity(elem, opacity)
    if stroke_c is not None:
      c += utils.set_border_color(elem, stroke_c)
    if stroke_w is not None:
      c += utils.set_border_width(elem, stroke_w)
    return c
