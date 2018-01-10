from . import *

class Segment(BaseLayer):
  """
  Class representing a Segment (part of a SegmentedControl) in Sketch
  """
  def parse_elem(self, elem):
    title = None
    title_fill = None

    for child in elem["children"]:
      if child["type"] == "UILabel":
        if child["textspan"]:
          title = child["textspan"][0]["contents"]
          title_fill = child["textspan"][0]["fill"]
        else:
          raise Exception("Segment: No title in segment: " + child["id"])

    elem["title"] = title
    elem["title_fill"] = title_fill
    return super().parse_elem(elem)
