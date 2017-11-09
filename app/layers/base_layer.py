import utils

class BaseLayer(object):
  """
  Base class for layers
  """
  def __init__(self, elem):
    """
    Args:
      elem (dict): represents a high-level layer of from sketch to be parsed.
    """
    self.elem = self.parse_elem(elem)

  def init_optional_params(self, elem, params):
    """
    Returns: elem with params initialized to None, except for fill
    """
    for param in params:
      if param == "fill":
        if "fill" in elem.attrs and elem["fill"] != "none":
          elem["fill"] = utils.convert_hex_to_rgb(elem["fill"])
        else:
          elem["fill"] = None
      elif param == "font-family":
        if "font-family" in elem.attrs:
          elem["font-family"] = elem["font-family"].split(",")[0]
        else:
          elem["font-family"] = None
      elif param == "text-align":
        if "text_align" in elem.attrs:
          elem["text-align"] = elem["text_align"]
        else:
          elem["text-align"] = None
      else:
        if param not in elem.attrs:
          elem[param] = None
    return elem

  def generate_object(self, elem):
    """
    Args:
      elem (dict): represents a high-level layer of from sketch to be parsed.

    Returns: object to be sent to the interpreter class
    """
    params = [
        "border-radius",
        "fill",
        "font-family",
        "font-size",
        "font-weight",
        "height",
        "horizontal",
        "id",
        "left-inset",
        "placeholder",
        "stroke-color",
        "stroke-width",
        "text",
        "text-align",
        "text-color",
        "title",
        "title-color",
        "type",
        "vertical",
        "width",
        "x",
        "y",
    ]
    elem = self.init_optional_params(elem, params)
    obj = {}
    for param in params:
      obj[param] = elem[param]
    return obj

  def parse_elem(self, elem):
    """
    Args:
      elem (dict): represents a high-level layer of from sketch to be parsed.

    Returns: object to be sent to the interpreter class
    """
    return self.generate_object(elem)
