import os
import subprocess
from pixelcode.plugin.interpreter_h import *

class Interpreter(object):
  """
  Takes output from Parser one at a time and generates swift file
    globals (dict): passed in from Parser
    file_name (str): name of current file being generated
    env (dict): environment in which components are being generated
    info (dict): has keys:
      - components (list): info on all components
      - methods (dict): has methods to be added outside of file"s init function
    swift (dict): swift code to generate the artboard

  NOTE: The variable C used in functions is used to denote "code".
  """
  def __init__(self, globals_):
    self.globals = globals_
    self.file_name = ""
    self.env = {}
    self.info = {"components": [], "methods": {}}
    self.swift = {}

  def gen_code(self, components):
    """
    Args:
      components: (list) list of components

    Returns: Fills in the swift instance var with generated code for artboard.
    """
    # Generate header of view controller file
    self.info["components"] = components
    artboard = utils.uppercase(self.globals["artboard"])
    view_controller = "{}ViewController".format(artboard)
    C = gen_viewcontroller_header(view_controller, self.info, True)
    C += utils.set_bg("view", self.globals["background_color"])

    self.file_name = view_controller
    self.swift[view_controller] = C
    self.env = {"in_view": False,
                "is_partial": False,
                "is_long_artboard": self.globals["is_long_artboard"]}
    self.gen_file()
    self.swift = gen_global_colors(self.globals["info"]["colors"], self.swift)

  def gen_partial(self, component):
    """
    Returns (str): swift code for generating part of an artboard.
    """
    ignore_types = ["", "ActionSheetTitle", "Cell", "Header", "Section",
                    "Segment", "SliderContent", "SliderOption", "SliderOptions"]
    if component["type"] in ignore_types:
      return ""
    self.filename = ""
    self.swift[""] = ""
    self.info["components"] = [component]
    self.env = {"in_view": False,
                "is_partial": True,
                "is_long_artboard": self.globals["is_long_artboard"]}
    swift, tc_elem = self.gen_comps(self.info["components"])
    # Write swift code to file
    o1 = open("partial.swift", "w+")
    o1.write(swift)
    o1.close()
    # Use swiftformat to format code
    os.system("swiftformat partial.swift")
    o2 = open("partial.swift", "r")
    swift = o2.read()
    os.remove("partial.swift")
    return swift

  def gen_file(self):
    """
    Returns: Fills in the swift instance variable with generated file.
    """
    swift, tc_elem = self.gen_comps(self.info["components"])
    self.swift[self.file_name] += swift + "}\n\n" + \
                                  add_methods(self.info["methods"])
    self.info["methods"] = {}

    if not tc_elem:
      if self.env["in_view"]:
        self.swift[self.file_name] += "{}\n}}".format(utils.req_init())
      else:
        self.swift[self.file_name] += "}"
    else:
      # add parent classes for table/collection view
      self.swift[self.file_name] = subclass_tc(self.swift[self.file_name],
                                               tc_elem)
      self.swift[self.file_name] += "}"
      self.gen_table_collection_view_files(tc_elem)

  def gen_comps(self, components):
    """
    Args:
      components: (dict list) contains information about components

    Returns (tuple):
      swift code to generate components and info on (table/collection) view if
      there is one.
    """
    # Clear (table/collection) view methods
    self.info["methods"]["tc_methods"] = ""
    navbar_item_ids = [] # holds ids of navbar items
    tc_elem = None
    C = ""

    for comp in components:
      type_ = comp["type"]
      if comp["id"] in navbar_item_ids:
        continue # navbar items already generated with navbar
      elif type_ == "UITabBar":
        gen_tabbar_file(self, comp)
      else:
        if type_ == "SliderView":
          gen_slider_view_pieces(self, comp)
        else:
          if type_ == "UITableView" or type_ == "UICollectionView":
            tc_elem = comp
          elif type_ == "UINavBar":
            navbar_item_ids.extend(get_navbar_item_ids(comp))
          elif type_ == "UILabel":
            self.swift["InsetLabel"] = gen_inset_label() # generate custom Label
        cf = ComponentFactory(comp, self.env)
        C += cf.swift
        self.info["methods"] = concat_dicts(self.info["methods"], cf.methods)
    return C, tc_elem

  def gen_table_collection_view_files(self, tc_elem):
    """
    Returns (None): Generates the necessary (table/collection)view files.
    """
    for name, header in tc_elem["custom_headers"].items():
      # Generate Header file and check for nested table/collection view
      nested_tc = self.gen_cell_header_file(name, header, tc_elem)
      if nested_tc is not None:
        self.gen_table_collection_view_files(nested_tc)

    # Loop through each section
    for section in tc_elem["sections"]:
      # Generate custom cells of this section
      for name, cell in section["custom_cells"].items():
        # Generate Cell file and check for nested table/collection view
        nested_tc = self.gen_cell_header_file(name, cell, tc_elem)
        if nested_tc is not None:
          self.gen_table_collection_view_files(nested_tc)

  def gen_cell_header_file(self, file_name, info, parent):
    """
    Returns (optional dict):
      Sets up (table/collection)view (header/cell) file and then returns the
      nested (table/collection)view, if there is one. Otherwise, returns None.
    """
    self.file_name = file_name
    self.env["in_view"] = True
    type_ = info["type"]
    if type_ == "Cell":
      C = gen_cell_header(parent["type"], info)
      C += utils.setup_rect(parent["id"], type_, info.get("rect"), cell=True)
    else: # type_ is header
      C = gen_header_header(parent["type"], info)
      C += utils.setup_rect(parent["id"], type_, info.get("rect"), header=True)

    swift, tc_elem = self.gen_comps(info.get("components"))
    swift += "layoutSubviews()\n}\n\n"
    swift += add_methods(self.info["methods"])
    self.info["methods"] = {}
    C += "{}\n\n{}\n\n".format(swift, utils.req_init())

    if not tc_elem:
      self.swift[self.file_name] = C + "}"
      return None

    # inner table/collection view exists
    if tc_elem["type"] == "UICollectionView":
      C = move_collection_view(C, tc_elem)
    # add parent classes for table/collection view
    C = subclass_tc(C, tc_elem)
    self.swift[self.file_name] = C + "}"
    return tc_elem
