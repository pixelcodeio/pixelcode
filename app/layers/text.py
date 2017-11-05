import utils
from layers.base_layer import BaseLayer

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
    elem["text"] = ""
    for child in elem.children:
      if child != "\n":
        elem["text"] += child.contents[0]

    self.generate_object(elem)
