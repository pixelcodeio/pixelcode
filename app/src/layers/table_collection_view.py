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
    sections = []

    for child in elem["children"]:
      if child["type"] == "Section":
        sections.append(child)
      elif utils.word_in_str("bound", child["id"]):
        if rect:
          raise Exception("TableCollectionView: Only one bound allowed")
        else:
          rect = child

    if not sections:
      raise Exception("TableCollectionView: No sections in " + elem["id"])
    elif rect is None:
      raise Exception("TableCollectionView: Missing bound in " + elem["id"])

    sections = sorted(sections, key=lambda s: s['y']) # sort by y
    type_ = elem["type"]
    sections = [self.calculate_separator(sect, type_) for sect in sections]

    separator = [] # separator between sections
    if len(sections) >= 2:
      separator = sections[1]['y'] - sections[0]['y'] - sections[0]['rheight']

    custom_headers = {}
    for section in sections:
      if section.get("header") is not None:
        header = section["header"]
        index = utils.index_of(header["id"], "header")
        header_name = utils.uppercase(header["id"][:index + 6])
        header["header_name"] = header_name
        if custom_headers.get(header_name) is None:
          custom_headers[header_name] = header

    elem["rect"] = rect
    elem["sections"] = sections
    elem["separator"] = separator
    elem["custom_headers"] = custom_headers
    return super().parse_elem(elem)

  def calculate_separator(self, section, type_):
    """
    Returns (dict): Section dictionary with separator key added.
    """
    cells = section["cells"]
    separator = []
    if len(cells) >= 2:
      if type_ == 'UITableView':
        vert_sep = cells[1]['y'] - cells[0]['y'] - cells[0]['rheight']
        separator = [vert_sep]
      else:
        hor_sep = cells[1]['x'] - cells[0]['x'] - cells[0]['rwidth']
        separator = [hor_sep]
        npr = math.floor(375/cells[0]['rwidth']) # number of cells per row
        if len(cells) > npr: # more than one row exists
          vert_sep = cells[npr]['y'] - cells[0]['y'] - cells[0]['rheight']
          separator.append(vert_sep)
    section["separator"] = separator
    return section
