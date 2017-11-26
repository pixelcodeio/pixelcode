from . import *

class UIImageView(BaseComponent):
  """
  Class representing an UIImageView in swift
  """
  def generate_swift(self):
    if self.env["set_prop"]:
      path = info.get('path')
      return self.set_image(path) if path is not None else ""
    return self.setup_component()

  def set_image(self, image_fname):
    """
    Args:
      image_fname (str): name of the image file

    Returns (str): swift code to set the image
    """
    index = image_fname.index(".")
    image_name = image_fname[0:index]
    return ("{}.image = UIImage(named: \"{}\")\n").format(self.id, image_name)

  def setup_component(self):
    """
    Returns (str): swift code to setup uiimageview 
    """
    keys = ['path', 'opacity', 'stroke-color', 'stroke-width']
    path, opacity, stroke_c, stroke_w = utils.get_vals(keys, self.info)
    C = ""
    if not self.env["in_view"]:
      C += self.set_image(path)
    if opacity is not None:
      C += super().set_opacity(opacity)
    if stroke_c is not None:
      C += utils.set_border_color(self.id, stroke_c)
    if stroke_w is not None:
      C += utils.set_border_width(self.id, stroke_w)
    return C
