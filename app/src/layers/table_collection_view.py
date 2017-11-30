import math
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

    separator = []
    if len(cells) >= 2:
      cells = sorted(cells, key=lambda c: c.get('y')) # sort by y
      if elem['type'] == 'UITableView':
        vert_sep = cells[1]['y'] - cells[0]['y'] - cells[0]['rheight']
        separator = [vert_sep]
      else:
        hor_sep = cells[1]['x'] - cells[0]['x'] - cells[0]['rwidth']
        separator = [hor_sep]
        npr = math.floor(375/cells[0]['rwidth']) # number of cells per row
        if len(cells) > npr: # more than one row exists
          vert_sep = cells[npr]['y'] - cells[0]['y'] - cells[0]['rheight']
          separator.append(vert_sep)

    elem["rect"] = rect
    elem["header"] = header
    elem["cells"] = cells
    elem["separator"] = separator

    return super().parse_elem(elem)
