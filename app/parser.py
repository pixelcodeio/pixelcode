import json
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
    self.elements = self.parse_elements(
        self.inherit_from(soup.svg.g, soup.svg.g.g, True)
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

  def parse_elements(self, artboard):
    """
    Returns: list of parsed elements
    """
    # grab elements, append attributes, sort by bottom-right coordinate
    elements = []
    for elem in artboard.children:
      if elem != "\n":
        elem = self.inherit_from(artboard, elem)
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
    while elements != []:
      elem = elements.pop()
      elem = self.calculate_spacing(elem, parsed_elements)
      elem = self.convert_coords(elem)

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

        else:
          for child in elem["children"]:
            elements.insert(0, child)
          continue

      # finished creating new element
      new_elem = parsed_elem.elem
      parsed_elements.insert(0, new_elem)
    return parsed_elements[::-1] # reverse so top-left element is first

  def create_children(self, elem):
    elem = self.inherit_from_json(elem)
    elem = self.inherit_from(elem.parent, elem)
    num_children = sum(1 for _ in elem.children)
    if num_children == 0:
      elem["children"] = []
      return elem

    children = []
    for child in elem.children:
      if child != "\n" and child.name != None:
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
      if vertical == {}:
        check_up = utils.check_spacing(check, elem, "up")
        if check_up[0]:
          vertical = {"direction": "up", "id": check["id"],
                      "distance": check_up[1]}
      if horizontal == {}:
        check_left = utils.check_spacing(check, elem, "left")
        if check_left[0]:
          horizontal = {"direction": "left", "id": check["id"],
                        "distance": check_left[1]}
      if vertical != {} and horizontal != {}:
        break

    if vertical == {}:
      vertical = {"direction": "up", "id": "", "distance": elem["y"]}
    if horizontal == {}:
      horizontal = {"direction": "left", "id": "", "distance": elem["x"]}

    elem["horizontal"] = horizontal
    elem["vertical"] = vertical
    return elem

  def convert_coords(self, elem):
    """
    Returns: elem with coords set relative to global height/width
    """
    # convert units to percentages
    elem["width"] /= self.globals["width"]
    elem["height"] /= self.globals["height"]
    elem["x"] /= self.globals["width"]
    elem["y"] /= self.globals["height"]
    elem["horizontal"]["distance"] /= self.globals["width"]
    elem["vertical"]["distance"] /= self.globals["height"]

    # generate center
    elem["x"] = elem["x"] + elem["width"] / 2
    elem["y"] = elem["y"] + elem["height"] / 2
    return elem

  def inherit_from(self, parent, child, first=False):
    """
    Returns: child with attributes from parent not defined in child passed down
    """
    for attr in parent.attrs:
      if first: #TODO: fix this shit
        if attr == "fill" and parent["fill"] == "none":
          pass
        elif attr == "stroke" and parent["stroke"] == "none":
          pass
        elif attr == "stroke-width" and parent["stroke"] == "none":
          pass
        elif attr == "fill-rule":
          pass
        elif attr != "id" and attr not in child.attrs:
          child[attr] = parent[attr]
      else:
        if attr != "id" and attr not in child.attrs:
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
    Returns: elem after checking if it is fake or not
    """
    if elem.name == "g":
      children = []
      for child in elem["children"]:
        if child != "\n" and "id" not in child.attrs:
          children.append(child)
      if len(children) == 2:
        parent_id = elem["id"]
        use_children = [c for c in children if c.name == "use"]
        main_child = [c for c in children if c.name != "use"][0]
        for child in use_children:
          elem = self.inherit_from(child, elem)
        elem = self.inherit_from(elem, main_child)
        elem["id"] = parent_id
    return elem
