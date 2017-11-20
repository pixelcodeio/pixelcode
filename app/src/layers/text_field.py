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
      raise Exception("TextField: Text cannot be empty in a button.")

    elem["rect"] = Rect(rect).elem if rect else None
    elem["text"] = Text(text).elem if text else None

    if text and rect:
      elem["left-inset"] = float(text["x"]) - float(rect["x"])
    else:
      raise Exception("TextField: Text and Rect must be defined in a TextField")

    return super(TextField, self).parse_elem(elem)
