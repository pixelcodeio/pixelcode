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
    bg_img = None
    for child in elem["children"]:
      if child["type"] == "UIView":
        rect = child
      elif child["type"] == "UILabel":
        text = child
      elif child["type"] == "UIImageView":
        bg_img = child

    if text is None and bg_img is None:
      raise Exception("Button: Nothing in button in " + elem["id"])

    elem["rect"] = rect
    elem["text"] = text
    elem["bg_img"] = bg_img

    return super().parse_elem(elem)
