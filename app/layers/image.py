import utils
from layers.base_layer import BaseLayer

class Image(BaseLayer):
  """
  Class representing an Image layer in Sketch
  """
  def parse_elem(self, elem):
    """
    Args:
      Refer to args in __init__
    """
    return self.generate_object(elem)
