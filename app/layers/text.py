import utils

class Text(object):
  def __init__(self, elem, vertical, horizontal):
    """
    Args:
      elem (dict): represents a text layer from sketch to be parsed.
      vertical (dict): represents the vertical spacing from other objects.
      horizontal (dict): represents the horizontal spacing from other objects.
    """
    self.elem = self.parse_elem(elem, vertical, horizontal)

  def parse_elem(self, elem, vertical, horizontal):
    """
    Args:
      Refer to args in __init__
    """
    opt_params = [
        "stroke-color",
        "stroke-width",
        "border-radius",
        "font-weight"
    ]
    elem = utils.init_optional_params(elem, opt_params)
    return {
        "type": "UILabel", "id": elem["id"],
        "text": elem["contents"],
        "text-color": utils.convert_hex_to_rgb(elem["fill"]),
        "font-size": elem["font-size"],
        "font-weight": elem["font-weight"],
        "stroke-color": elem["stroke-color"],
        "stroke-width": elem["stroke-width"],
        "border-radius": elem["border-radius"],
        "x": elem["x"], "y": elem["y"],
        "width": elem["width"], "height": elem["height"],
        "vertical": vertical, "horizontal": horizontal}
