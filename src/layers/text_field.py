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
      if child.name == "rect":
        rect = child
      elif child.name == "text":
        text = child

    if text is None:
      raise Exception("Text cannot be empty in a button.")

    elem["rect"] = Rect(rect).elem if rect is not None else None
    elem["text"] = Text(text).elem if text is not None else None

    if text is not None and rect is not None:
      elem["left-inset"] = float(text["x"]) - float(rect["x"])
    else:
      raise Exception("Text and Rect must be defined for a TextField")

    return super(TextField, self).parse_elem(elem)
