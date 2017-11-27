from layers.rect import Rect
from layers.text import Text
from . import *

class TableCollectionView(BaseLayer):
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
          raise Exception("TableCollectionView: Only one wash allowed in "
                          + elem["id"])
        else:
          rect = child
      elif child["type"] == "Cell":
        cells.append(child)
      elif child["type"] == "Header":
        if header:
          raise Exception("TableCollectionView: Only one header allowed "
                          + elem["id"])
        else:
          header = child
      else:
        raise Exception("TableCollectionView: Unsupported elem type in "
                        + elem["id"])

    if not cells:
      raise Exception("TableCollectionView: No cells in " + elem["id"])

    separator = 0
    if len(cells) >= 2:
      separator = cells[1]["cy"] - cells[1]["cy"]

    elem["rect"] = rect
    elem["header"] = header
    elem["cells"] = cells
    elem["separator"] = separator

    return super().parse_elem(elem)
