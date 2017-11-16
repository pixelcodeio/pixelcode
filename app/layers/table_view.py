from layers.rect import Rect
from layers.text import Text
from . import *

class TableView(BaseLayer):
  """
  Class representing a TableView layer in Sketch
  """
  def parse_elem(self, elem):
    rect = None
    cells = []
    for child in elem["children"]:
      if child["type"] == "UIView":
        if rect is None:
          rect = child
        else:
          raise Exception("Only one wash allowed per TableView")
      elif child["type"] == "Cell":
        cells.append(child)
      else:
        raise Exception("Unsupported type for TableView")

    if not cells:
      raise Exception("Must have one component in a TableView")

    separator = 0
    if len(cells) >= 2:
      separator = cells[1]["y"] - cells[1]["y"]

    elem["rect"] = rect
    elem["cells"] = cells
    elem["separator"] = separator

    return super(TableView, self).parse_elem(elem)
