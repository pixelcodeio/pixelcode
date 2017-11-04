import utils

class Rect(object):
  def __init__(self, elem, vertical, horizontal):
    """
    Args:
      elem (dict): represents a rectangle layer from sketch to be parsed.
      vertical (dict): represents the vertical spacing from other objects.
      horizontal (dict): represents the horizontal spacing from other objects.
    """
    self.elem = self.parse_rect(elem, vertical, horizontal)

  def parse_rect(self, elem, vertical, horizontal):
    center_x = ((int(elem["x"]) + elem["width"]) / 2)
    center_y = ((int(elem["y"]) + elem["height"]) / 2)
    return {
        "type": "UIView", "id": elem["id"],
        "fill": utils.convert_hex_to_rgb(elem["fill"]),
        "x": center_x, "y": center_y,
        "width": elem["width"], "height": elem["height"],
        "vertical": vertical, "horizontal": horizontal}
