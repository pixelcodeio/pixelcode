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
        "border-radius",
        "fill",
        "font-family",
        "font-size",
        "font-weight",
        "height",
        "horizontal",
        "id",
        "stroke-color",
        "stroke-width",
        "text",
        "text-color",
        "title",
        "title-color",
        "type",
        "vertical"
        "width",
        "x",
        "y",
    ]
    elem = utils.init_optional_params(elem, params)
    obj = {}
    for param in params:
      obj[param] = elem[param]
    return obj
