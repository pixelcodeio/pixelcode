from . import *

class Image(BaseLayer):
  """
  Class representing an Image layer in Sketch
  """
  def parse_elem(self, elem):
    elem["path"] = elem["id"] + ".png" # TODO: change this later
    return super().parse_elem(elem)
