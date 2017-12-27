from . import *

class SegmentedControl(BaseLayer):
  """
  Class representing a SegmentedControl in Sketch
  """
  def parse_elem(self, elem):
    tint_fill = None
    items = []

    for child in elem["children"]:
      if utils.word_in_str("bound", child["id"]):
        if child.get("stroke-color") is not None:
          tint_fill = child["stroke-color"]
        else:
          raise Exception("SegmentedControl: Bound missing stroke-color.")
      elif child["type"] == "Segment":
        items.append(child)

    items = sorted(items, key=lambda i: i['x'])
    items = [i["title"] for i in items]
    elem["items"] = items
    elem["tint_fill"] = tint_fill
    return super().parse_elem(elem)
