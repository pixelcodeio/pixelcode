# library imports
import json
from operator import itemgetter
from bs4 import BeautifulSoup
# custom imports
from layers._all import *
from parser_h import *
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
      - filters: (dict) contains information about shadows
      - info: dictionary with keys (used for style-guide)
        - fill (list)
        - font-family (list)
        - font-size(list)
    is_ios: whether the code being generated is iOS code
  """
  def __init__(self, path, artboard, is_ios):
    """
    Returns: Parser object for parsing the file located at filepath
    """
    self.artboard = artboard
    self.elements = []
    self.json = {}
    self.globals = {}
    self.scale = 1.0
    self.path = path
    self.is_ios = is_ios # Always True for now.

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
    artboard = inherit_from(page, artboard, init=True)

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
    if svg.get('style') is not None:
      bg_hex = svg["style"][:-1].split(" ")[1] # parse hexcode
      bg_color = utils.convert_hex_to_rgb(bg_hex) + (1.0,)
    else:
      bg_color = (255, 255, 255, 1.0)
    height = svg["height"][:-2]
    width = svg["width"][:-2]
    pagename = svg.g["id"]
    artboard = svg.g.g["id"]
    fill = [bg_color, (0, 0, 0, 0)]
    info = {'fill': fill, 'font-family': [], 'font-size': []}
    svg_filters = svg.find_all("filter")
    filters = {}
    for f in svg_filters:
      id_ = f.attrs["id"]
      dx = f.feoffset.attrs["dx"]
      dy = f.feoffset.attrs["dy"]
      fill = parse_filter_matrix(f.fecolormatrix.attrs["values"])
      filters[id_] = {"dx": dx, "dy": dy, "fill": fill}
    return {"background_color": bg_color,
            "width": float(width),
            "height": float(height),
            "pagename": pagename,
            "artboard": artboard,
            "info": info,
            "filters": filters}

  def parse_elements(self, children, parent, init=False):
    """
    Returns: list of parsed elements
    """
    # grab elements, append attributes, sort by bottom-right coordinate
    elements = []
    for elem in [c for c in children if c != "\n"]:
      if init:
        elem = inherit_from(parent, elem)
        elem = create_children(elem, self.json)

      if elem.name == "g":
        elem = parse_fake_group(elem)

      elem["x"] = float(elem["x"])
      elem["y"] = float(elem["y"])
      elem["abs_x"] = float(elem["abs_x"])
      elem["abs_y"] = float(elem["abs_y"])
      elem["width"] = float(elem["width"])
      elem["height"] = float(elem["height"])
      elements.append(elem)
    elements.sort(key=lambda e: (e["x"] + e["y"] + e["width"] + e["height"]))

    parsed_elements = []
    while elements:
      elem = elements.pop(0)
      elem = calculate_spacing(elem, parsed_elements, self.is_ios)
      elem = convert_coords(elem, parent)

      # correctly name grouped elements
      if elem.name == "g":
        if utils.word_in_str("actionSheet", elem["id"]):
          elem.name = "actionsheet"
        elif utils.word_in_str("button", elem["id"]):
          elem.name = "button"
        elif utils.word_in_str("cell", elem["id"]):
          elem.name = "cell"
        elif utils.word_in_str("collectionView", elem["id"]):
          elem.name = "collectionview"
        elif utils.word_in_str("header", elem["id"]):
          elem.name = "header"
        elif utils.word_in_str("listView", elem["id"]):
          elem.name = "tableview"
        elif utils.word_in_str("navBar", elem["id"]):
          elem.name = "navbar"
        elif utils.word_in_str("searchBar", elem["id"]):
          elem.name = "searchbar"
        elif utils.word_in_str("slider", elem["id"]):
          elem.name = "slider"
        elif utils.word_in_str("statusBar", elem["id"]):
          continue
        elif utils.word_in_str("switch", elem["id"]):
          elem.name = "switch"
        elif utils.word_in_str("tabBar", elem["id"]):
          elem.name = "tabbar"
        elif utils.word_in_str("textField", elem["id"]):
          elem.name = "textfield"
        elif utils.word_in_str("view", elem["id"]):
          elem.name = "view"
        else: # ungroup elements inside
          for child in elem["children"]:
            child["x"] = elem["x"] + float(child["x"])
            child["y"] = elem["y"] + float(child["y"])
            child["width"] = float(child["width"])
            child["height"] = float(child["height"])
            elements.insert(0, child)
          continue

      elem["children"] = self.parse_elements(elem["children"], elem)
      if elem.name == "actionsheet":
        parsed_elem = ActionSheet(elem, "UIActionSheet")
      elif elem.name == "button":
        parsed_elem = Button(elem, "UIButton")
      elif elem.name == "cell":
        parsed_elem = Container(elem, "Cell")
      elif elem.name == "collectionview":
        parsed_elem = TableCollectionView(elem, "UICollectionView")
      elif elem.name == "header":
        parsed_elem = Container(elem, "Header")
      elif elem.name in {"image", "polygon", "path", "circle"}:
        parsed_elem = Image(elem, "UIImageView")
      elif elem.name == "navbar":
        parsed_elem = NavBar(elem, "UINavBar")
      elif elem.name == "rect" or elem.name == "view":
        parsed_elem = Rect(elem, "UIView")
      elif elem.name == "searchbar":
        parsed_elem = SearchBar(elem, "UISearchBar")
      elif elem.name == "slider":
        parsed_elem = Slider(elem, "UISlider")
      elif elem.name == "switch":
        parsed_elem = Switch(elem, "UISwitch")
      elif elem.name == "tabbar":
        parsed_elem = TabBar(elem, "UITabBar")
      elif elem.name == "tableview":
        parsed_elem = TableCollectionView(elem, "UITableView")
      elif elem.name == "text":
        parsed_elem = Text(elem, "UILabel")
      elif elem.name == "textfield":
        parsed_elem = TextField(elem, "UITextField")
      elif elem.name == "tspan":
        parsed_elem = TextSpan(elem, "")
      else:
        raise Exception("Parser: Unhandled elem type for " + elem.name)

      # finished creating new element
      new_elem = parsed_elem.elem
      parsed_elements.insert(0, new_elem)
      self.extract_to_info(new_elem)
    return parsed_elements[::-1]

  def extract_to_info(self, elem):
    """
    Returns: extracts style-guide information from elem and adds it to info
    """
    keys = ['fill', 'font-family', 'font-size']
    fill, font_family, font_size = utils.get_vals(keys, elem)
    self.add_to_info('fill', fill)
    self.add_to_info('font-family', font_family)
    self.add_to_info('font-size', font_size)

  def add_to_info(self, key, new_value):
    """
    Args:
      key (str): either 'font', 'font-family', or 'font-size'
    """
    if new_value is not None:
      if key == 'fill':
        new_value = [float(v) for v in new_value] # convert strings to float
      if new_value not in self.globals["info"][key]:
        self.globals["info"][key].append(new_value)
