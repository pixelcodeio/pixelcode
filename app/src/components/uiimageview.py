from . import *

class UIImageView(BaseComponent):
  """
  Class representing an UIImageView in swift
    swift: (str) the swift code to create/set properties of a UIImageView
  """
  def generate_swift(self):
    if self.env["set_prop"]:
      path = info.get('path')
      return self.set_image(path) if path is not None else ""
    return self.setup_component()

  def set_image(self, image_fname):
    """
    Args:
      image_fname: (str) name of the image file

    Returns: (str) swift code to set the image
    """
    index = image_fname.index(".")
    image_name = image_fname[0:index]
    return ("{}.image = UIImage(named: \"{}\")\n").format(self.id, image_name)

  def setup_component(self):
    """
    Returns: (str) swift code to apply all the properties from text to elem.
    """
    path = self.info.get('path')
    opacity = self.info.get('opacity')
    stroke_c = self.info.get('stroke-color')
    stroke_w = self.info.get('stroke-width')
    c = ""
    if not self.env["in_view"]:
      c += self.set_image(path)
    if opacity is not None:
      c += super().set_opacity(opacity)
    if stroke_c is not None:
      c += utils.set_border_color(self.id, stroke_c)
    if stroke_w is not None:
      c += utils.set_border_width(self.id, stroke_w)
    return c
