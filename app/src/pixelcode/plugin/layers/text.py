from .text_span import TextSpan, params_equal
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
    t = elem["children"]

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
    if "line-spacing" in elem.attrs:
      elem["line-spacing"] = elem["line-spacing"]
    if "letter-spacing" in elem.attrs:
      elem["char-spacing"] = elem["letter-spacing"]
    elem["children"] = []
    return super().parse_elem(elem)
