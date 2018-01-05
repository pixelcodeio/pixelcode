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
        if utils.word_in_str('bound', child["id"]):
          rect = child
        else:
          child['path'] = child['id'] + '.png' # add path key
          bg_img = child
      elif child["type"] == "UILabel":
        text = child
      elif child["type"] == "UIImageView":
        bg_img = child

    if text is None and bg_img is None:
      raise Exception("Button: Nothing in button in " + elem["id"])

    elem["bg_img"] = bg_img
    elem["rect"] = rect
    elem["text"] = text
    return super().parse_elem(elem)
