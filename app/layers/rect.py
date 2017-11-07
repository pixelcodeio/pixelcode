import utils
from layers.base_layer import BaseLayer

class Rect(BaseLayer):
  """
  Class representing a Rectangle layer in Sketch
  """
  def parse_elem(self, elem):
    if elem["fill"] != "none":
      elem["fill"] = utils.convert_hex_to_rgb(elem["fill"])
    if "rx" in elem.attrs:
      elem["border-radius"] = elem["rx"]
    if "stroke" in elem.attrs:
      elem["stroke-color"] = utils.convert_hex_to_rgb(elem["stroke"])

      if "stroke-width" in elem:
        elem["stroke-width"] = elem["stroke-width"]
      else:
        elem["stroke-width"] = 1
    else:
      elem["stroke-color"] = None
      elem["stroke-width"] = None
    return super(Rect, self).parse_elem(elem)
