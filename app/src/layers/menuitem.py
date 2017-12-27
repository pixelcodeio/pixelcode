from . import *

class MenuItem(BaseLayer):
  """
  Class representing an MenuItem layer in Sketch
  """
  def parse_elem(self, elem):
    title = None
    path = None
    rect = None

    for child in elem["children"]:
      if child["type"] == "UILabel":
        if child["textspan"]:
          title = child["textspan"][0]["contents"]
        else:
          raise Exception("MenuItem: No title in menuitem: " + elem["id"])
      elif child["type"] == "UIImageView":
        path = child["id"] + ".png"
      elif utils.word_in_str("bound", child["id"]):
        rect = child

    if title is None and path is None:
      raise Exception("MenuItem: No content in menuitem: " + elem["id"])

    elem["title"] = title
    elem["path"] = path
    elem["rect"] = rect
    return super().parse_elem(elem)
