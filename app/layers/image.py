from . import *

class Image(BaseLayer):
  """
  Class representing an Image layer in Sketch
  """
  def parse_elem(self, elem):
    elem["stroke-color"] = None
    elem["stroke-width"] = None
    return super(Image, self).parse_elem(elem)
