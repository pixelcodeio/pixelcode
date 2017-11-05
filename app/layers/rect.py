import utils
from layers.base_layer import BaseLayer

class Rect(BaseLayer):
  """
  Class representing a Rectangle layer in Sketch
  """
  def parse_elem(self, elem):
    """
    Args:
      Refer to args in __init__

    Returns: dictionary with keys
      - type (str): "UIView"
      - id (str): id of the element
      - fill (tuple): (r, g, b) triple representing the color
      - x (float): x coordinate with respect to global width
      - y (float): y coordinate with respect to global height
      - vertical (dict): refer to __init__ args for description
      - horizontal (dict): refer to __init__ args for description
    """
    elem["fill"] = utils.convert_hex_to_rgb(elem["fill"])

    return self.generate_object(elem)
