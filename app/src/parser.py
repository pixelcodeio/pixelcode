# library imports
import json
from operator import itemgetter
from bs4 import BeautifulSoup
# custom imports
from layers._all import *
import parser_h as ph
import utils

class Parser(object):
  """
  Parses a SVG file and outputs a dictionary with necessary attributes
    artboard: name of artboard
    elements: list of elements in svg
    filepath: path to file
    globals: dictionary with keys
      - width (int)
      - height (int)
      - background_color (tuple)
      - pagename (str)
      - artboard (str)
  """
  def __init__(self, path, artboard):
    """
    Returns: Parser object for parsing the file located at filepath
    """
    self.artboard = artboard
    self.elements = []
    self.json = {}
    self.globals = {}
    self.scale = 1.0
    self.path = path

  def parse_artboard(self):
    """
    Parses artboard with name [self.artboard]
    """
    # initializes self.json
    f = open(self.path + self.artboard + ".json", "r+")
    self.json = json.loads(f.read())

    # parses svg and sets instance variables appropriately
    f = open(self.path + self.artboard + ".svg", "r+")
    soup = BeautifulSoup(f, "lxml")
    f.close()

    self.globals = self.parse_globals(soup.svg)
    self.scale = float(self.globals["width"]) / 375
    page = soup.svg.g
    artboard = soup.svg.g.g
    artboard = ph.inherit_from(page, artboard, init=True)

    # init rwidth and rheight for inheritance
    artboard["rwidth"] = self.globals["width"]
    artboard["rheight"] = self.globals["height"]

    self.elements = self.parse_elements(
        [c for c in artboard.children],
        artboard,
        init=True
    )

  def parse_globals(self, svg):
    """
    Returns: dict of globals taken from parsing svg element
    """
    bg_color = svg["style"][:-1].split(" ")[1] # parse hexcode
    height = svg["height"][:-2]
    width = svg["width"][:-2]
    pagename = svg.g["id"]
    artboard = svg.g.g["id"]
    return {"background_color": utils.convert_hex_to_rgb(bg_color),
            "width": float(width),
            "height": float(height),
            "pagename": pagename,
            "artboard": artboard}

  def parse_elements(self, children, parent, init=False):
    """
    Returns: list of parsed elements
    """
    # grab elements, append attributes, sort by bottom-right coordinate
    elements = []
    for elem in [c for c in children if c != "\n"]:
      if init:
        elem = ph.inherit_from(parent, elem)
        elem = ph.create_children(elem, self.json)

      if elem.name == "g":
        elem = ph.parse_fake_group(elem)

      elem["x"] = float(elem["x"])
      elem["y"] = float(elem["y"])
      elem["width"] = float(elem["width"])
      elem["height"] = float(elem["height"])
      elements.append(elem)
    elements.sort(key=lambda e: (e["x"] + e["y"] + e["width"] + e["height"]))

    parsed_elements = []
    while elements:
      elem = elements.pop(0)
      elem = ph.calculate_spacing(elem, parsed_elements)
      elem = ph.convert_coords(elem, parent)

      # parse elements into their layers
      if elem.name == "rect":
        elem["type"] = "UIView"
        parsed_elem = Rect(elem)

      elif elem.name == "text":
        elem["type"] = "UILabel"
        parsed_elem = Text(elem)

      elif elem.name == "image":
        elem["type"] = "UIImageView"
        parsed_elem = Image(elem)

      elif elem.name == "g":
        if "Button" in elem["id"] or "button" in elem["id"]:
          elem["type"] = "UIButton"
          parsed_elem = Button(elem)

        elif "TextField" in elem["id"]:
          elem["type"] = "UITextField"
          parsed_elem = TextField(elem)

        elif "ListView" in elem["id"]:
          elem["type"] = "UITableView"
          elem["children"] = self.parse_elements(elem["children"], elem)
          parsed_elem = TableView(elem)

        elif "Cell" in elem["id"] or "cell" in elem["id"]:
          elem["type"] = "Cell"
          elem["children"] = self.parse_elements(elem["children"], elem)
          parsed_elem = Cell(elem)

        elif "Header" in elem["id"] or "header" in elem["id"]:
          elem["type"] = "Header"
          elem["children"] = self.parse_elements(elem["children"], elem)
          parsed_elem = Cell(elem)

        else:
          for child in elem["children"]:
            child["x"] = elem["x"] + float(child["x"])
            child["y"] = elem["y"] + float(child["y"])
            child["width"] = float(child["width"])
            child["height"] = float(child["height"])
            elements.insert(0, child)
          continue

      # finished creating new element
      new_elem = parsed_elem.elem
      parsed_elements.insert(0, new_elem)
    return parsed_elements[::-1]
