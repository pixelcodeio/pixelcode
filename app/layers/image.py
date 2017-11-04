import utils

class Image(object):
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
    return {
        "type": "UIImageView", "id": elem["id"],
        "x": elem["x"], "y": elem["y"],
        "width": elem["width"], "height": elem["height"],
        "vertical": vertical, "horizontal": horizontal}
