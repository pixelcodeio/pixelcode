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
    elem["text-color"] = utils.convert_hex_to_rgb(elem["fill"])
    elem["stroke-width"] = None
    elem["stroke-color"] = None
    elem["text"] = ""
    for child in elem["children"]:
      elem["text"] += child.contents[0]
    return super(Text, self).parse_elem(elem)
