import utils
from bs4 import BeautifulSoup

class Parser:
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
    return

  def parse_svg(self):
    """
    Returns: Parses an SVG and sets instance variables appropriately
    """
    f = open(self.filepath, "r+")
    soup = BeautifulSoup(f, "lxml")
    f.close()
    e = []

    self.globals = self.parse_globals(soup.svg)
    self.elements = self.parse_elements(soup.svg.g.g)
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
    # set up list of attributes to inherit from artboard
    inheritable = {}
    for attr in artboard.attrs:
      if attr != 'id':
        inheritable[attr] = artboard[attr]

    # grab elements, append attributes, sort by bottom-right coordinate
    elements = [] 
    for elem in artboard.children:
      if elem != "\n":
        for key in inheritable:
          if key not in elem:
            elem[key] = inheritable[key]
        elements.append(elem)
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
          if check_left [0]:
            horizontal = {"direction": "left", "id": check["id"],
                          "distance": check_left[1]}
        if vertical != {} and horizontal != {}:
          break

      if vertical == {}:
        vertical = {"direction": "up", "id": "", "distance": int(elem["y"])}
      if horizontal == {}:
        horizontal = {"direction": "left", "id": "", "distance": int(elem["x"])}

      if elem.name == "rect":
        center_x = int(elem["x"]) + int(elem["width"]) / 2
        center_y = int(elem["y"]) + int(elem["height"]) / 2
        vertical["distance"] = \
            (1.0 * self.globals["height"]) / vertical["distance"]
        horizontal["distance"] = \
            (1.0 * self.globals["width"]) / horizontal["distance"]
        new_elem = {"type": "UIView", "id": elem["id"],
                    "fill": utils.convert_hex_to_rgb(elem["fill"]), 
                    "x": center_x, "y": center_y,
                    "width": elem["width"], "height": elem["height"], 
                    "vertical": vertical, "horizontal": horizontal}
      parsed_elements.insert(0, new_elem)
    return parsed_elements         

if __name__ == "__main__":
  p = Parser("./tests/testrects.svg")
  p2 = Parser("./tests/test1.svg")
  assert utils.convert_hex_to_rgb("#B4FBB8") == (180, 251, 184)
  p.parse_svg()
  #p2.parse_svg()
