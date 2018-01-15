from . import *

class Section(BaseLayer):
  """
  Class representing a Section in Sketch
  """
  def parse_elem(self, elem):
    rect = header = None
    custom_cells = {}
    cells = []

    for child in elem["children"]:
      if child["type"] == "Header":
        if header:
          raise Exception("Section: Only one header allowed per section")
        else:
          header = child
      elif child["type"] == "Cell":
        child = self.check_cell_for_hairline(child)
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

    elem["cells"] = cells
    elem["custom_cells"] = custom_cells
    elem["header"] = header
    elem["rect"] = rect
    return super().parse_elem(elem)

  def check_cell_for_hairline(self, cell):
    """
    Returns (dict): adjusts cell dictionary if hairline exists in the cell
    """
    hairline_index = -1
    for index, comp in enumerate(cell["components"]):
      if utils.word_in_str("hairline", comp["id"]):
        hairline_index = index
        break
    if hairline_index > -1:
      cell["hairline"] = cell["components"][hairline_index]
      del cell["components"][hairline_index]
    return cell
