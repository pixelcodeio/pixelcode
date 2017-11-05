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

  def generate_object(self, elem):
    """
    Generates object to be sent to the interpreter class
    """
    params = [
        "type",
        "id",
        "fill",
        "border-radius",
        "stroke-width",
        "stroke-color",
        "text",
        "text-color",
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
    elem = utils.init_optional_params(elem, params)
    obj = {}
    for param in params:
      obj[param] = elem[param]
    return obj
