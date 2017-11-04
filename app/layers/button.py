import utils

class Button(object):
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
    """
    opt_params = [
        "fill",
        "stroke-color",
        "stroke-width",
        "border-radius",
        "font-weight"
    ]
    elem = utils.init_optional_params(elem, opt_params)
    return {
        "type": "UIButton", "id": elem["id"],
        "fill": elem["fill"],
        "border-radius": elem["border-radius"],
        "stroke-width": elem["stroke-width"],
        "stroke-color": elem["stroke-color"],
        "title-color": elem["title-color"],
        "title": elem["title"],
        "font-size": elem["font-size"],
        "font-weight": elem["font-weight"],
        "x": elem["x"], "y": elem["y"],
        "width": elem["width"], "height": elem["height"],
        "vertical": vertical, "horizontal": horizontal}
