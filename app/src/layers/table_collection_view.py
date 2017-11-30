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
      sort_c = sorted(cells, key=lambda c: c.get('y')) # sort by y
      if elem['type'] == 'UITableView':
        vert_sep = sort_c[1]['y'] - sort_c[0]['y'] - sort_c[0]['rheight']
        separator = [vert_sep]
      else:
        hor_sep = sort_c[1]['x'] - sort_c[0]['x'] - sort_c[0]['rwidth']
        separator = [hor_sep]
        npr = math.floor(375/sort_c[0]['rwidth']) # number of cells per row
        if len(cells) > npr: # more than one row exists
          vert_sep = sort_c[npr]['y'] - sort_c[0]['y'] - sort_c[0]['rheight']
          separator.append(vert_sep)

    elem["rect"] = rect
    elem["header"] = header
    elem["cells"] = cells
    elem["separator"] = separator

    return super().parse_elem(elem)
