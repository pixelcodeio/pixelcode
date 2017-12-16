from components.component_factory import ComponentFactory
from interpreter_h import *

class Interpreter(object):
  """
  Takes output from Parser one at a time and generates swift file
    globals (dict): passed in from Parser
    file_name (str): name of current file being generated
    info (dict): has keys:
      - components (list): info on all components
      - tc_elem (dict): info on current (table/collection)view being generated
      - tc_methods (str): any necessary (table/collection)view methods
    swift (dict): swift code to generate all components
  """
  def __init__(self, globals_):
    globals_['bgc'] = globals_['background_color'] + ("1.0",) # adding opacity
    self.globals = globals_
    self.file_name = ""
    self.info = {"components": [], "tc_elem": {}, "tc_methods": ""}
    self.swift = {}

  def gen_code(self, components):
    """
    Args:
      components: (list) list of components

    Returns: Fills in the swift instance var with generated code for artboard.
    """
    # Generate header of view controller file
    self.info["components"] = components
    artboard = utils.uppercase(self.globals['artboard'])
    view_controller = '{}ViewController'.format(artboard)
    C = self.gen_viewcontroller_header(view_controller, True) \
        + utils.set_bg('view', self.globals['bgc'])

    self.file_name = view_controller
    self.swift[view_controller] = C
    self.gen_components(False)

  def gen_viewcontroller_header(self, view_controller, declare_vars):
    """
    Args:
      view_controller (str): name of viewcontroller
      declare_vars (bool): whether or not to declare global variables.
    Returns (str): swift code of the view controller header
    """
    header = ("import UIKit\nimport SnapKit\n\n"
              "class {}: UIViewController {{\n\n"
             ).format(view_controller)
    header += declare_g_vars(self.info["components"]) if declare_vars else ""
    header += "\noverride func viewDidLoad() {\nsuper.viewDidLoad()\n"
    return header

  def gen_components(self, in_v):
    """
    Returns: Fills in the swift instance variable with generated code.
    """
    self.swift[self.file_name] += self.gen_comps(self.info["components"], in_v)

    if not self.info["tc_elem"]:
      if in_v:
        self.swift[self.file_name] += "}}\n{}\n}}".format(utils.req_init())
      else:
        self.swift[self.file_name] += "\n}\n}"
    else:
      self.subclass_tc() # add parent classes for table/collection view
      self.swift[self.file_name] += "\n}}\n{}}}".format(self.info["tc_methods"])

      tc_elem = self.info["tc_elem"]
      tc_id = tc_elem['id']
      tc_header = tc_elem.get('header')

      if tc_header is not None:
        # nested table/collection view
        if self.setup_cell_header('header', tc_id, tc_header):
          self.gen_components(True)

      tc_cell = tc_elem.get('cells')[0]
      # nested table/collection view
      if self.setup_cell_header('cell', tc_id, tc_cell):
        self.gen_components(True)

  def clear_tv(self):
    """
    Returns (None): Resets tc_elem and tc_methods instance variables
    """
    self.info["tc_elem"] = {}
    self.info["tc_methods"] = ""

  def gen_comps(self, components, in_v):
    """
    Args:
      components: (dict list) contains information about components

    Returns (str): swift code to generate components.
    """
    self.clear_tv()
    C = ""

    for comp in components:
      type_ = comp['type']
      if type_ == 'UITabBar':
        comp['active_vc'] = self.file_name # name of active view controller
        cf = ComponentFactory(type_, comp, in_v)
        self.gen_tabbar_viewcontroller(comp['id'], cf.swift)
      else:
        if type_ == 'UILabel':
          cf = ComponentFactory(type_, comp, in_v, bgc=self.globals['bgc'])
        else:
          cf = ComponentFactory(type_, comp, in_v)
          if type_ == 'UITableView' or type_ == 'UICollectionView':
            self.info["tc_elem"] = comp
            self.info["tc_methods"] = cf.tc_methods
        C += cf.swift
    return C

  def gen_tabbar_viewcontroller(self, id_, swift):
    """
    Args:
      swift (str): code generated for the tabbar

    Returns (None): generates file for tabbar view controller in self.swift
    """
    view_controller = utils.uppercase(id_) + 'ViewController'
    C = self.gen_viewcontroller_header(view_controller, False)
    C = C.replace(': UIViewController', ': UITabBarController')
    C += ("{}}}\n}}\n").format(swift)
    self.swift[view_controller] = C

  def subclass_tc(self):
    """
    Returns (None): adds necessary (table/collection)view parent classes
    """
    C = self.swift[self.file_name]
    ext = ", UITableViewDelegate, UITableViewDataSource"
    if self.info["tc_elem"]['type'] == 'UICollectionView':
      ext = ext.replace('Table', 'Collection')
      ext += ", UICollectionViewDelegateFlowLayout"

    if ": UIViewController" in C:
      C = utils.ins_after_key(C, ": UIViewController", ext)
    elif ": UITableViewCell" in C:
      C = utils.ins_after_key(C, ": UITableViewCell", ext)
    elif ": UITableViewHeaderFooterView" in C:
      C = utils.ins_after_key(C, ": UITableViewHeaderFooterView", ext)
    elif ": UICollectionReusableView" in C:
      C = utils.ins_after_key(C, ": UICollectionReusableView", ext)
    elif ": UICollectionViewCell" in C:
      C = utils.ins_after_key(C, ": UICollectionViewCell", ext)
    else:
      raise Exception("interpreter: invalid file in subclass_tc()")

    self.swift[self.file_name] = C

  def setup_cell_header(self, type_, id_, info):
    """
    Returns (bool):
      True if there is an nested (table/collection) view, False otherwise.
      NOTE: also sets up (table/collection)view header/cell file.
    """
    if type_ == "cell":
      self.file_name = utils.uppercase(id_) + "Cell"
      C = gen_cell_header(id_, info)
      C += utils.setup_rect(id_, info.get('rect'), True, tc_cell=True)
    else: # type_ is header
      self.file_name = utils.uppercase(id_) + "HeaderView"
      C = gen_header_header(id_, info)
      C += utils.setup_rect(id_, info.get('rect'), True, tc_header=True)

    C += self.gen_comps(info.get('components'), True)
    C += "}}\n\n{}\n\n".format(utils.req_init())

    tc_elem = self.info["tc_elem"]
    if not tc_elem:
      self.swift[self.file_name] = C + "}"
      return False

    # inner table/collection view exists
    if tc_elem['type'] == 'UICollectionView':
      C = move_collection_view(C, self.info)
    # add parent classes for table/collection view
    C = subclass_tc(C, self.info)
    self.swift[self.file_name] = C + "\n{}\n}}".format(self.info["tc_methods"])
    id_ = tc_elem['id']
    cell = tc_elem.get('cells')[0]
    self.file_name = utils.uppercase(id_) + 'Cell'
    self.swift[self.file_name] = gen_cell_header(id_, cell)
    # get components of first cell
    self.info["components"] = tc_elem.get('cells')[0].get('components')
    return True
