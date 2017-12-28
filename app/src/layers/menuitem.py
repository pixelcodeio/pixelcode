from . import *

class MenuItem(BaseLayer):
  """
  Class representing an MenuItem layer in Sketch
  """
  def parse_elem(self, elem):
    text = None
    img = None
    rect = None

    for child in elem["children"]:
      if child["type"] == "UILabel":
        if child["textspan"]:
          text = child
        else:
          raise Exception("MenuItem: No text in MenuItem: " + elem["id"])
      elif child["type"] == "UIImageView":
        img = child
      elif utils.word_in_str("bound", child["id"]):
        rect = child

    if text is None and img is None:
      raise Exception("MenuItem: No content in MenuItem: " + elem["id"])
    elif rect is None:
      raise Exception("MenuItem: No bound in MenuItem: " + elem["id"])

    elem["text"] = text
    elem["img"] = img
    elem["rect"] = rect
    return super().parse_elem(elem)
