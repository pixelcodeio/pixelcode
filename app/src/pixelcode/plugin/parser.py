# library imports
import json
import requests
from operator import itemgetter
from urllib import request
from bs4 import BeautifulSoup
# custom imports
from pixelcode.plugin.layers._all import *
from pixelcode.plugin.parser_h import *
import pixelcode.plugin.utils as utils

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
        - colors (list of dicts)
        - text-styles (list of dicts)
    is_ios: whether the code being generated is iOS code
  """
  def __init__(self, path, artboard, is_ios, debug):
    """
    Returns: Parser object for parsing the file located at filepath
    """
    self.artboard = artboard
    self.debug = debug
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
    if self.debug:
      # initializes self.json
      f = open(self.path + self.artboard + ".json", "r+")
      self.json = json.loads(f.read())

      # parses svg and sets instance variables appropriately
      f = open(self.path + self.artboard + ".svg", "r+")
      soup = BeautifulSoup(f, "lxml")
      f.close()
    else:
      # initializes self.json
      f = requests.get(self.path + self.artboard + ".json")
      self.json = json.loads(f.content)

      # parses svg and sets instance variables appropriately
      f = requests.get(self.path + self.artboard + ".svg")
      soup = BeautifulSoup(f.content, "lxml")

    self.globals = self.parse_globals(soup.svg)
    self.scale = float(self.globals["width"]) / 375
    page = soup.svg.g
    artboard = soup.svg.g.g
    artboard = inherit_from(page, artboard, init=True)

    # init rwidth and rheight for inheritance
    artboard["rwidth"] = self.globals["rwidth"]
    artboard["rheight"] = self.globals["rheight"]

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
    rwidth = float(svg["width"][:-2])
    rheight = float(svg["height"][:-2])
    # Get proper height based on width
    height = {320: 568, 375: 667, 414: 736}.get(rwidth)
    if height is None:
      height = rheight
    is_long_artboard = height < float(svg["height"][:-2])
    pagename = svg.g["id"]
    artboard = svg.g.g["id"]
    fill = [{'r': int(float(bg_color[0])),
             'g': int(float(bg_color[1])),
             'b': int(float(bg_color[2])),
             'a': float(bg_color[3])},
            {'r': 0, 'g': 0, 'b': 0, 'a': 0.0}]
    info = {'colors': fill, 'text-styles': []}
    svg_filters = svg.find_all("filter")
    filters = {}
    for f in svg_filters:
      id_ = f.attrs["id"]
      dx = f.feoffset["dx"]
      dy = f.feoffset["dy"]
      # check if shadow is inner or outer
      is_outer = utils.word_in_str("outer", f.feoffset["result"])
      d_size = 0 # change in width and height of shadow in pixels
      radius = 0
      if f.femorphology is not None:
        radius += float(f.femorphology["radius"])
        d_size = float(f.femorphology["radius"]) * 2.0
      if f.fegaussianblur is not None:
        radius += float(f.fegaussianblur["stddeviation"])
      fill = parse_filter_matrix(f.fecolormatrix["values"])
      filters[id_] = {"dx": dx, "dy": dy, "radius": radius, "fill": fill,
                      "d_size": d_size, "is_outer": is_outer}
    return {"artboard": artboard,
            "background_color": bg_color,
            "filters": filters,
            "height": height,
            "info": info,
            "is_long_artboard": is_long_artboard,
            "pagename": pagename,
            "rheight": rheight,
            "rwidth": rwidth,
            "width": rwidth}

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
      elem = convert_coords(self, elem, parent)

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
        elif utils.word_in_str("tableView", elem["id"]):
          elem.name = "tableview"
        elif utils.word_in_str("section", elem["id"]):
          elem.name = "section"
        elif utils.word_in_str("sliderContent", elem["id"]):
          elem.name = "slidercontent"
        elif utils.word_in_str("sliderOptions", elem["id"]):
          elem.name = "slideroptions"
        elif utils.word_in_str("sliderOption", elem["id"]):
          elem.name = "slideroption"
        elif utils.word_in_str("sliderView", elem["id"]):
          elem.name = "sliderview"
        elif utils.word_in_str("navBar", elem["id"]):
          elem.name = "navbar"
        elif utils.word_in_str("searchBar", elem["id"]):
          elem.name = "searchbar"
        elif utils.word_in_str("segmentedControl", elem["id"]):
          elem.name = "segmentedcontrol"
        elif utils.word_in_str("segment", elem["id"]):
          elem.name = "segment"
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
      elif elem.name == "section":
        parsed_elem = Section(elem, "Section")
      elif elem.name == "slidercontent":
        parsed_elem = Container(elem, "SliderContent")
      elif elem.name == "slideroption":
        parsed_elem = SliderOption(elem, "SliderOption")
      elif elem.name == "slideroptions":
        parsed_elem = SliderOptions(elem, "SliderOptions")
      elif elem.name == "sliderview":
        parsed_elem = SliderView(elem, "SliderView")
      elif elem.name == "navbar":
        parsed_elem = NavBar(elem, "UINavBar")
      elif elem.name == "rect":
        parsed_elem = Rect(elem, "UIView")
      elif elem.name == "searchbar":
        parsed_elem = SearchBar(elem, "UISearchBar")
      elif elem.name == "segmentedcontrol":
        parsed_elem = SegmentedControl(elem, "UISegmentedControl")
      elif elem.name == "segment":
        parsed_elem = Segment(elem, "Segment")
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
      elif elem.name == "view":
        parsed_elem = Container(elem, "UIView")
      else:
        raise Exception("Parser: Unhandled elem type for " + elem.name)

      # finished creating new element
      new_elem = parsed_elem.elem
      if new_elem.get('filter') is not None: # lookup filter in filters
        new_elem["filter"] = self.globals["filters"][new_elem["filter"]]
      parsed_elements.insert(0, new_elem)
      self.globals["info"] = extract_to_info(new_elem, self.globals["info"])
    return parsed_elements[::-1]
