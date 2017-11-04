import utils

class Rect(object):
  def __init__(self, elem, vertical, horizontal):
    """
    Args:
      elem (dict): represents a rectangle layer from sketch to be parsed.
      vertical (dict): represents the vertical spacing from other objects.
      horizontal (dict): represents the horizontal spacing from other objects.
    """
    self.elem = self.parse_elem(elem, vertical, horizontal)

  def parse_elem(self, elem, vertical, horizontal):
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
    opt_params = [
        "stroke-color",
        "stroke",
        "border-radius",
        "font-weight"
    ]
    elem = utils.init_optional_params(elem, opt_params)
    return {
        "type": "UIView", "id": elem["id"],
        "fill": utils.convert_hex_to_rgb(elem["fill"]),
        "x": elem["x"], "y": elem["y"],
        "width": elem["width"], "height": elem["height"],
        "font-weight": elem["font-weight"], "stroke": elem["stroke"],
        "stroke-color": elem["stroke-color"],
        "border-radius": elem["border-radius"],
        "vertical": vertical, "horizontal": horizontal}
