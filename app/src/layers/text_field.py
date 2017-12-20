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
      if utils.word_in_str("bound", child["id"]):
        rect = child
      elif child["type"] == "UILabel":
        text = child
      else:
        raise Exception("TextField: Unsupported elem type in " + elem["id"])

    if text is None:
      raise Exception("TextField: Text is empty in " + elem["id"])
    elif rect is None:
      raise Exception("TextField: Rect is empty in " + elem["id"])

    elem["rect"] = rect
    elem["text"] = text
    elem["left-inset"] = float(text["x"]) - float(rect["x"])

    return super().parse_elem(elem)
