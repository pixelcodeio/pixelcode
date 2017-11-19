import json
from operator import itemgetter
from bs4 import BeautifulSoup
from layers._all import *
import utils

class Parser(object):
  """
  Parses a SVG file and outputs a dictionary with necessary attributes
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
    artboard = self.inherit_from(soup.svg.g, soup.svg.g.g, True)

    # init rwidth and rheight for inheritance
    artboard["rwidth"] = self.globals["width"]
    artboard["rheight"] = self.globals["height"]

    self.elements = self.parse_elements(
        [c for c in artboard.children],
        artboard,
        True
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
        elem = self.inherit_from(parent, elem)
        elem = self.create_children(elem)

      if elem.name == "g":
        elem = self.parse_fake_group(elem)

      elem["x"] = float(elem["x"])
      elem["y"] = float(elem["y"])
      elem["width"] = float(elem["width"])
      elem["height"] = float(elem["height"])
      elements.append(elem)
    elements.sort(key=lambda e: (e["x"] + e["y"] + e["width"] + e["height"]))

    parsed_elements = []
    while elements:
      elem = elements.pop(0)
      elem = self.calculate_spacing(elem, parsed_elements)
      elem = self.convert_coords(elem, parent)

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
        if "Button" in elem["id"]:
          elem["type"] = "UIButton"
          parsed_elem = Button(elem)

        elif "TextField" in elem["id"]:
          elem["type"] = "UITextField"
          parsed_elem = TextField(elem)

        elif "ListView" in elem["id"]:
          elem["type"] = "UITableView"
          elem["children"] = self.parse_elements(elem["children"], elem)
          parsed_elem = TableView(elem)

        elif "Cell" in elem["id"]:
          elem["type"] = "Cell"
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

  def create_children(self, elem):
    elem = self.inherit_from_json(elem)
    elem = self.inherit_from(elem.parent, elem)
    num_children = sum(1 for _ in elem.children)
    if num_children == 0:
      elem["children"] = []
      return elem

    children = []
    for child in elem.children:
      if child != "\n" and child.name is not None:
        children.append(self.parse_fake_group(self.create_children(child)))
    elem["children"] = children
    return elem

  def calculate_spacing(self, elem, parsed_elements):
    """
    Returns:
      elem with keys vertical and horizontal added, where vertical
      and horizontal represent the relative spacing between elem
      and parsed_elements
    """
    vertical = {}
    horizontal = {}
    for check in parsed_elements:
      if not vertical:
        check_up = utils.check_spacing(check, elem, "up")
        if check_up[0]:
          vertical = {"direction": "up", "id": check["id"],
                      "distance": check_up[1]}
      if not horizontal:
        check_left = utils.check_spacing(check, elem, "left")
        if check_left[0]:
          horizontal = {"direction": "left", "id": check["id"],
                        "distance": check_left[1]}
      if vertical and horizontal:
        break

    if not vertical:
      vertical = {"direction": "up", "id": "", "distance": elem["y"]}
    if not horizontal:
      horizontal = {"direction": "left", "id": "", "distance": elem["x"]}

    elem["horizontal"] = horizontal
    elem["vertical"] = vertical
    return elem

  def convert_coords(self, elem, parent):
    """
    Returns: elem with coords set relative to parent height/width
    """
    width = parent["rwidth"]
    height = parent["rheight"]
    # cache pixel widths
    elem["rwidth"] = elem["width"]
    elem["rheight"] = elem["height"]
    # convert units to percentages
    elem["width"] /= width
    elem["height"] /= height
    elem["horizontal"]["distance"] /= width
    elem["vertical"]["distance"] /= height

    # generate center
    elem["cx"] = elem["x"]/width + elem["width"]/2
    elem["cy"] = elem["y"]/height + elem["height"]/2
    return elem

  def inherit_from(self, parent, child, first=False):
    """
    Returns: child with attributes from parent not defined in child passed down
    """
    for attr in parent.attrs:
      skip = attr == "id"
      if first:
        skip = (skip
                or (attr == "fill" and parent["fill"] == "none")
                or (attr == "stroke" and parent["stroke"] == "none")
                or (attr == "stroke-width" and parent["stroke"] == "none")
                or attr == "fill-rule")

      if not skip and attr not in child.attrs:
        child[attr] = parent[attr]
    return child

  def inherit_from_json(self, child):
    """
    Returns: child with attributes from json not defined in child passed down
    """
    if "id" in child.attrs:
      for layer in self.json["layers"]:
        if child["id"] == layer["name"]:
          for key in layer.keys():
            if key not in child.attrs:
              child[key] = layer[key]
          break
    return child

  def parse_fake_group(self, elem):
    """
    Handles the case where an elem is a group but none of its children have ids.
    We first make sure that we are in this case (by checking its children),
    then we pick a child to make the main element. Finally, we replace the group
    with this new element, after making sure it inherits from all the other
    elements.
    """
    if elem.name == "g":
      # set-up children and ensure that no children have ids.
      children = []
      for child in [c for c in elem["children"] if c != "\n"]:
        if "id" in child.attrs:
          return elem
        children.append(child)

      # two separate lists for easy checking later
      use_children = []
      main_children = []
      for child in children:
        if child.name == "use":
          use_children.append(child)
        else:
          main_children.append(child)

      if (not main_children) and use_children:
        for ind, child in enumerate(use_children):
          if "xlink:href" in child.attrs:
            child.name = "rect"
            use_children.pop(ind)
            main_children = [child]
            break

      # ensure that there is only one main child
      if len(main_children) == 1 and use_children:
        parent_id = elem["id"]
        for child in use_children:
          elem = self.inherit_from(child, elem)
        elem = self.inherit_from(elem, main_children[0])
        elem["id"] = parent_id
      else:
        raise Exception("Unhandled case in parse_fake_group.")
    return elem