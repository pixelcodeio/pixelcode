from layers.rect import Rect
from layers.text import Text
from . import *

class TextField(BaseLayer):
  """
  Class representing an TextField layer in Sketch
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
      raise Exception("TextField: Text cannot be empty in a button.")
    elif rect is None:
      raise Exception("TextField: Rect cannot be empty in a button.")

    elem["rect"] = rect
    elem["text"] = text
    elem["left-inset"] = float(text["x"]) - float(rect["x"])

    return super().parse_elem(elem)
