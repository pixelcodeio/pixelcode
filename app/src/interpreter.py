from interpreter_h import *

class Interpreter(object):
  """
  Takes output from Parser one at a time and generates swift file
    globals (dict): passed in from Parser
    file_name (str): name of current file being generated
    info (dict): has keys:
      - components (list): info on all components
      - methods (dict): has methods to be added outside of file"s init function
    swift (dict): swift code to generate the artboard

  NOTE: The variable C used in functions is used to denote "code".
  """
  def __init__(self, globals_):
    self.globals = globals_
    self.file_name = ""
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
    self.gen_file(False)
    self.swift = gen_global_colors(self.globals["info"]["fill"], self.swift)

  def gen_file(self, in_v):
    """
    Returns: Fills in the swift instance variable with generated file.
    """
    swift, tc_elem = self.gen_comps(self.info["components"], in_v)
    self.swift[self.file_name] += swift + "}\n" + \
                                  add_methods(self.info["methods"])
    self.info["methods"] = {}

    if not tc_elem:
      if in_v:
        self.swift[self.file_name] += "{}\n}}".format(utils.req_init())
      else:
        self.swift[self.file_name] += "}"
    else:
      # add parent classes for table/collection view
      self.swift[self.file_name] = subclass_tc(self.swift[self.file_name],
                                               tc_elem)
      self.swift[self.file_name] += "}"

      tc_id = tc_elem["id"]
      tc_header = tc_elem.get("header")

      if tc_header is not None:
        # nested table/collection view
        if self.contains_nested_tc("header", tc_id, tc_header):
          self.gen_file(True)

      tc_cell = tc_elem.get("cells")[0]
      # nested table/collection view
      if self.contains_nested_tc("cell", tc_id, tc_cell):
        self.gen_file(True)

  def gen_comps(self, components, in_v):
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
        gen_tabbar_file(self, comp, in_v)
      else:
        if type_ == "SliderView":
          gen_slider_view_pieces(self, comp, in_v)
        else:
          if type_ == "UITableView" or type_ == "UICollectionView":
            tc_elem = comp
          elif type_ == "UINavBar":
            navbar_item_ids.extend(get_navbar_item_ids(comp))
          elif type_ == "UILabel":
            self.swift["InsetLabel"] = gen_inset_label() # generate custom Label
        cf = ComponentFactory(comp, in_v)
        C += cf.swift
        self.info["methods"] = concat_dicts(self.info["methods"], cf.methods)
    return C, tc_elem

  def contains_nested_tc(self, type_, id_, info):
    """
    Returns (bool):
      True if there is an nested (table/collection) view, False otherwise.
      NOTE: also sets up (table/collection)view header/cell file.
    """
    if type_ == "cell":
      self.file_name = utils.uppercase(id_) + "Cell"
      C = gen_cell_header(id_, info)
      C += utils.setup_rect(id_, type_, info.get("rect"), tc_cell=True)
    else: # type_ is header
      self.file_name = utils.uppercase(id_) + "HeaderView"
      C = gen_header_header(id_, info)
      C += utils.setup_rect(id_, type_, info.get("rect"), tc_header=True)

    swift, tc_elem = self.gen_comps(info.get("components"), True)
    C += "{}}}\n\n{}\n\n".format(swift, utils.req_init())

    if not tc_elem:
      self.swift[self.file_name] = C + "}"
      return False

    # inner table/collection view exists
    if tc_elem["type"] == "UICollectionView":
      C = move_collection_view(C, self.info)
    # add parent classes for table/collection view
    C = subclass_tc(C, tc_elem)
    C += "\n{}\n}}".format(self.info["methods"]["tc_methods"])
    self.swift[self.file_name] = C
    id_ = tc_elem["id"]
    cell = tc_elem.get("cells")[0]
    self.file_name = utils.uppercase(id_) + "Cell"
    self.swift[self.file_name] = gen_cell_header(id_, cell)
    # get components of first cell
    self.info["components"] = tc_elem.get("cells")[0].get("components")
    return True
