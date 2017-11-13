from . import *

class Rect(BaseLayer):
  """
  Class representing a Rectangle layer in Sketch
  """
  def parse_elem(self, elem):
    if "rx" in elem.attrs:
      elem["border-radius"] = elem["rx"]
    if "stroke" in elem.attrs and elem["stroke"] != "none":
      elem["stroke-color"] = utils.convert_hex_to_rgb(elem["stroke"])

      if "stroke-width" in elem.attrs:
        elem["stroke-width"] = elem["stroke-width"]
      else:
        elem["stroke-width"] = 1
    else:
      elem["stroke-color"] = None
      elem["stroke-width"] = None
    return super(Rect, self).parse_elem(elem)
