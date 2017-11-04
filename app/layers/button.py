import utils

class Button(object):
  def __init__(self, elem):
    """
    Args:
      elem (dict): represents a rectangle layer from sketch to be parsed.
      vertical (dict): represents the vertical spacing from other objects.
      horizontal (dict): represents the horizontal spacing from other objects.
    """
    self.elem = self.parse_elem(elem)

  def parse_elem(self, elem):
    """
    Args:
      Refer to args in __init__
    """
    rect = elem.rect
    if "rx" in rect.attrs:
      elem["border-radius"] = rect["rx"]
    if "stroke" in rect.attrs:
      elem["stroke-color"] = utils.convert_hex_to_rgb(rect["stroke"])
      if "stroke-width" in rect:
        elem["stroke-width"] = rect["stroke-width"]
      else:
        elem["stroke-width"] = 1

    text = elem.find('text')
    elem["title"] = ""
    for child in text.children:
      if child != "\n":
        elem["title"] += child.contents[0]
    for key in text.attrs:
      if key == "fill":
        elem["title-color"] = utils.convert_hex_to_rgb(text["fill"])
      else:
        elem[key] = text[key]

    opt_params = [
        "fill",
        "stroke-color",
        "stroke-width",
        "border-radius",
        "font-weight",
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
        "font-family",
        "font-size",
        "font-weight",
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
