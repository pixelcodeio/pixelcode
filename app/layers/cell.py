from . import *

class Cell(BaseLayer):
  """
  Class representing a Cell in Sketch
  """
  def parse_elem(self, elem):
    """
    Args:
      Refer to args in __init__
    """
    elem["text-color"] = utils.convert_hex_to_rgb(elem["fill"])
    elem["stroke-width"] = None
    elem["stroke-color"] = None
    elem["contents"] = elem.text
    return super(TextSpan, self).parse_elem(elem)

def params_equal(tspan1, tspan2):
  params = [
      "fill",
      "font-family",
      "font-size",
      "opacity",
      "text-align",
  ]
  for param in params:
    in_both = param in tspan1 and param in tspan2
    if not (in_both and tspan1[param] == tspan2[param]):
      return False
  return True
