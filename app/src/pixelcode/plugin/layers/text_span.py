from . import *

class TextSpan(BaseLayer):
  """
  Class representing an individual Text Component in Sketch
  """
  def parse_elem(self, elem):
    """
    Args:
      Refer to args in __init__
    """
    elem["contents"] = elem.text
    elem["stroke-color"] = None
    elem["stroke-width"] = None
    elem["text-color"] = utils.convert_hex_to_rgb(elem["fill"])
    return super().parse_elem(elem)

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
    not_in_both = param not in tspan1 and param not in tspan2
    if not (not_in_both or (in_both and tspan1[param] == tspan2[param])):
      return False
  return True
