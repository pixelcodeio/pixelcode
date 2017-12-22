from . import *

class Image(BaseLayer):
  """
  Class representing an Image layer in Sketch
  """
  def parse_elem(self, elem):
    img_fill = None

    if elem.attrs.get("fill"):
      img_fill = elem.attrs["fill"]

    elem["img_fill"] = img_fill
    elem["path"] = elem["id"] + ".png" # TODO: change this later
    return super().parse_elem(elem)
