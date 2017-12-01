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
      raise Exception("Button: Text is empty in " + elem["id"])

    elem["rect"] = rect
    elem["text"] = text

    return super().parse_elem(elem)
