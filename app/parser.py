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
    Returns: Parses an SVG and returns a dictionary representing the contents
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
    return {"background_color": self.convert_hex_to_rgb(bg_color),
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

    # grab children, sort by bottom-right coordinate
    children = [] 
    for child in artboard.children:
      if child != "\n":
        children.append(child)
    children.sort(key=lambda c: (int(c["x"]) + int(c["y"]) + 
                                 int(c["width"]) + int(c["height"])))

    # append parent keys on children
    for child in children:
      for key in inheritable:
        if key not in child:
          child[key] = inheritable[key]

  def check_spacing(self, r1, r2, direction):
    """
    Args:
      r1: The rectangle with a smaller bottom-right coordinate sum
      r2: The rectangle we are currently checking
      direction: direction to check; one-of [up, down, left, right]

    Returns:
      A tuple (bool, dist) representing whether r2 can have its spacing 
      defined in [direction] with respect to r1, where dist is the 
      distance between the two rectangles in pixels.
    """
    r1_top = (int(r1["x"]), int(r1["y"])) # top-left
    r1_bottom = (r1_top[0] + int(r1["width"]), r1_top[1] + int(r1["height"]))
    r2_top = (int(r2["x"]), int(r2["y"])) # top-left
    r2_bottom = (r2_top[0] + int(r2["width"]), r2_top[1] + int(r2["height"]))

    if r2_top[0] > r1_bottom[0] and r2_top[1] > r1_bottom[1]:
      return False, 0

  def convert_hex_to_rgb(self, hex_string):
    """ 
    Returns [hex_string] converted to a rgb tuple. 
    """
    h = hex_string.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

if __name__ == "__main__":
  p = Parser("./tests/testrects.svg")
  p2 = Parser("./tests/test1.svg")
  assert p.convert_hex_to_rgb("#B4FBB8") == (180, 251, 184)
  p.parse_svg()
  p2.parse_svg()
