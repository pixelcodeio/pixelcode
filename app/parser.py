import utils
from bs4 import BeautifulSoup
from layers import *

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
  def __init__(self, filepath):
    """
    Returns: Parser object for parsing the file located at filepath
    """
    self.elements = []
    self.filepath = filepath
    self.globals = {}

  def parse_svg(self):
    """
    Returns: Parses an SVG and sets instance variables appropriately
    """
    f = open(self.filepath, "r+")
    soup = BeautifulSoup(f, "lxml")
    f.close()

    self.globals = self.parse_globals(soup.svg)
    self.elements = self.parse_elements(
        self.inherit_from(soup.svg.g, soup.svg.g.g)
    )
    return

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
            "width": int(width),
            "height": int(height),
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
        elements.append(self.inherit_from(artboard, elem))
    elements.sort(key=lambda e: (int(e["x"]) + int(e["y"]) +
                                 int(e["width"]) + int(e["height"])))

    parsed_elements = []
    for elem in elements:
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
        vertical = {"direction": "up", "id": "", "distance": int(elem["y"])}
      if horizontal == {}:
        horizontal = {"direction": "left", "id": "", "distance": int(elem["x"])}

      # convert units to percentages
      elem["width"] = int(elem["width"]) / (1.0 * self.globals["width"])
      elem["height"] = int(elem["height"]) / (1.0 * self.globals["height"])
      elem["x"] = int(elem["x"]) / (1.0 * self.globals["width"])
      elem["y"] = int(elem["y"]) / (1.0 * self.globals["height"])
      vertical["distance"] /= (1.0 * self.globals["height"])
      horizontal["distance"] /= (1.0 * self.globals["width"])

      if elem.name == "rect":
        r = Rect(elem, vertical, horizontal)
      else:
        pass
      new_elem = r.elem
      parsed_elements.insert(0, new_elem)
    return parsed_elements[::-1]

  def inherit_from(self, parent, child):
    """
    Attributes from parent not defined in child are passed down
    """
    for attr in parent.attrs:
      if attr not in child.attrs:
        child[attr] = parent[attr]
    return child

if __name__ == "__main__":
  p = Parser("./tests/testrects.svg")
  p2 = Parser("./tests/test1.svg")
  p3 = Parser("./tests/text.svg")
  assert utils.convert_hex_to_rgb("#B4FBB8") == (180, 251, 184)
  p.parse_svg()
  #p2.parse_svg()
