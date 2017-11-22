from layers.rect import Rect
from layers.text import Text
from . import *

class Button(BaseLayer):
  """
  Class representing a Button in Sketch
  """
  def parse_elem(self, elem):
    rect = None
    text = None
    for child in elem["children"]:
      if child["type"] == "UIView":
        rect = child
      elif child["type"] == "UILabel":
        text = child

    if text is None:
      raise Exception("Button: Text cannot be empty in a button.")

    elem["rect"] = rect
    elem["text"] = text

    return super(Button, self).parse_elem(elem)
