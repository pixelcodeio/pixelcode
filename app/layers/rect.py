import utils
from layers.base_layer import BaseLayer

class Rect(BaseLayer):
  """
  Class representing a Rectangle layer in Sketch
  """
  def parse_elem(self, elem):
    elem["fill"] = utils.convert_hex_to_rgb(elem["fill"])
    return super(Rect, self).parse_elem(elem)
