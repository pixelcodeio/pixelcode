from . import *

class Section(BaseLayer):
  """
  Class representing a Section in Sketch
  """
  def parse_elem(self, elem):
    rect = None
    header = None
    custom_cells = []
    custom_cell_ids = []
    cells = []

    for child in elem["children"]:
      if child["type"] == "Header":
        if header:
          raise Exception("Section: Only one header allowed per section")
        else:
          header = child
      elif child["type"] == "Cell":
        cells.append(child)
        if child["id"] not in custom_cell_ids:
          custom_cell_ids.append(child["id"])
          custom_cells.append(child)
      elif utils.word_in_str("bound", child["id"]):
        if rect:
          raise Exception("Section: Only one bound allowed per section")
        else:
          rect = child

    if not cells:
      raise Exception("Section: No cells in section " + elem["id"])
    elif rect is None:
      raise Exception("Section: Missing bound in " + elem["id"])

    cells = sorted(cells, key=lambda c: c['y']) # sort by y

    elem["rect"] = rect
    elem["header"] = header
    elem["custom_cells"] = custom_cells
    elem["cells"] = cells
    return super().parse_elem(elem)
