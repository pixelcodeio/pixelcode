from . import *

class Section(BaseLayer):
  """
  Class representing a Section in Sketch
  """
  def parse_elem(self, elem):
    rect = None
    header = None
    custom_cells = {}
    cells = []

    for child in elem["children"]:
      if child["type"] == "Header":
        if header:
          raise Exception("Section: Only one header allowed per section")
        else:
          header = child
      elif child["type"] == "Cell":
        cells.append(child)
        index = utils.index_of(child["id"], "cell")
        cell_name = utils.uppercase(child["id"][:index + 4])
        child["cell_name"] = cell_name
        if custom_cells.get(cell_name) is None:
          custom_cells[cell_name] = child
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
