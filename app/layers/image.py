import utils

class Image(object):
  def __init__(self, elem):
    """
    Args:
      elem (dict): represents a text layer from sketch to be parsed.
      vertical (dict): represents the vertical spacing from other objects.
      horizontal (dict): represents the horizontal spacing from other objects.
    """
    self.elem = self.parse_elem(elem)

  def parse_elem(self, elem):
    """
    Args:
      Refer to args in __init__
    """
    params = [
        "type",
        "id",
        "fill",
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
