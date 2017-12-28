from . import *

class MenuBar(BaseLayer):
  """
  Class representing an MenuBar layer in Sketch
  """
  def parse_elem(self, elem):
    items = []
    rect = None

    for child in elem["children"]:
      if child["type"] == "MenuItem":
        items.append(child)
      elif utils.word_in_str("bound", child["id"]):
        rect = child

    if not items:
      raise Exception("MenuBar: No items in MenuBar: " + elem["id"])
    elif rect is None:
      raise Exception("MenuBar: No bound in MenuBar: " + elem["id"])

    items = sorted(items, key=lambda i: i["x"])
    selected_index = 0
    for index, i in enumerate(items):
      if utils.word_in_str("active", i["id"]):
        selected_index = index
        break

    if items[selected_index]["rect"].get("filter") is None:
      raise Exception("MenuBar: Selected item missing inner shadow (slider).")

    elem["items"] = items
    elem["selected_index"] = selected_index
    elem["rect"] = rect
    return super().parse_elem(elem)
