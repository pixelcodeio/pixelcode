from . import *

class Image(BaseLayer):
  """
  Class representing an Image layer in Sketch
  """
  def parse_elem(self, elem):
    elem["path"] = elem["id"]
    return super(Image, self).parse_elem(elem)
