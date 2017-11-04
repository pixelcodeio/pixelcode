import utils

class Text(object):
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
    elem["text-color"] = utils.convert_hex_to_rgb(elem["fill"])
    elem["text"] = ""
    for child in elem.children:
      if child != "\n":
        elem["text"] += child.contents[0]

    opt_params = [
        "font-weight",
        "fill",
        "stroke-color", # TODO: remove this
        "stroke-width", # TODO: remove this
        "border-radius", # TODO: remove this
    ]
    elem = utils.init_optional_params(elem, opt_params)
    params = [
        "type",
        "id",
        "text",
        "text-color",
        "fill",
        "font-size",
        "font-weight",
        "stroke-color", # TODO: remove this
        "stroke-width", # TODO: remove this
        "border-radius", # TODO: remove this
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
