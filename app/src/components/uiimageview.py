from . import *

class UIImageView(BaseComponent):
  """
  Class representing an UIImageView in swift
    swift: (str) the swift code to create/set properties of a UIImageView
  """
  def __init__(self, id_, info, in_v=False, set_p=False):
    """
    Returns: A UIImageView with the swift attribute set to the generated code
    """
    super(UIImageView, self).__init__()
    if set_p:
      path = info.get('path')
      self.swift = self.set_image(id_, path) if path is not None else ""
    else:
      self.swift = self.setup_component(id_, info, in_v)

  def set_image(self, elem, image_fname):
    """
    Args:
      elem: (str) id of the component
      image_fname: (str) name of the image file

    Returns: (str) The swift code to set the image of elem.
    """
    index = image_fname.index(".")
    image_name = image_fname[0:index]
    return ("{}.image = UIImage(named: \"{}\")\n").format(elem, image_name)

  def setup_component(self, elem, info, in_v=False):
    """
    Args:
      elem: (str) id of the component
      info: (dict) see generate_component docstring for more information.
      in_v: (bool) represents whether the imageview is being generated
               inside a custom view file (or not)

    Returns: (str) The swift code to apply all the properties from text to elem.
    """
    path = info.get('path')
    opacity = info.get('opacity')
    stroke_c = info.get('stroke-color')
    stroke_w = info.get('stroke-width')
    c = ""
    if not in_v:
      c += self.set_image(elem, path)
    if opacity is not None:
      c += super().set_opacity(elem, opacity)
    if stroke_c is not None:
      c += utils.set_border_color(elem, stroke_c)
    if stroke_w is not None:
      c += utils.set_border_width(elem, stroke_w)
    return c
