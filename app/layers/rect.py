import utils

class Rect(object):
  def __init__(self, elem):
    """
    Args:
      elem (dict): represents a rectangle layer from sketch to be parsed.
    """
    self.elem = self.parse_elem(elem)

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
    opt_params = [
        "stroke-color",
        "stroke-width",
        "border-radius"
    ]
    elem = utils.init_optional_params(elem, opt_params)

    params = [
        "type",
        "id",
        "fill",
        "border-radius",
        "stroke-width",
        "stroke-color",
        "title-color",
        "title",
        "font-size",
        "x",
        "y",
        "width",
        "height",
        "horizontal",
        "vertical"
    ]
    ret = {}
    for param in params:
      ret[param] = elem[param]
    return ret
