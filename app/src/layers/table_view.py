from layers.rect import Rect
from layers.text import Text
from . import *

class TableView(BaseLayer):
  """
  Class representing a TableView layer in Sketch
  """
  def parse_elem(self, elem):
    rect = None
    header = None
    cells = []
    for child in elem["children"]:
      if child["type"] == "UIView":
        if rect:
          raise Exception("TableView: Only one wash allowed per TableView")
        else:
          rect = child
      elif child["type"] == "Cell":
        cells.append(child)
      elif child["type"] == "Header":
        if header:
          raise Exception("TableView: Only one header allowed.")
        else:
          header = child
      else:
        raise Exception("TableView: Unsupported elem type for TableView")

    if not cells:
      raise Exception("TableView: Must have one cell in a TableView")

    separator = 0
    if len(cells) >= 2:
      separator = cells[1]["cy"] - cells[1]["cy"]

    elem["rect"] = rect
    elem["header"] = header
    elem["cells"] = cells
    elem["separator"] = separator

    return super().parse_elem(elem)
