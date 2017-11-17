from layers.text_span import TextSpan, params_equal
from . import *

class Text(BaseLayer):
  """
  Class representing a Text layer in Sketch
  """
  def parse_elem(self, elem):
    """
    Args:
      Refer to args in __init__
    """
    t = []

    for child in elem["children"]:
      new_tspan = TextSpan(child)
      t.append(new_tspan.elem)

    textspan = []
    i = 0
    while i < len(t):
      tspan = t[i]
      while i < len(t) - 1 and params_equal(tspan, t[i + 1]):
        tspan["contents"] += t[i + 1]["contents"]
        i += 1
      textspan.append(tspan)
      i += 1

    elem["textspan"] = textspan
    if elem["id"] == "portraitsnyc":
      print elem["textspan"]
    return super(Text, self).parse_elem(elem)
