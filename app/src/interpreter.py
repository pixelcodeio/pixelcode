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
    swift (dict): swift code to generate the artboard

  NOTE: The variable C used in functions is used to denote "code".
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
    C = gen_viewcontroller_header(view_controller, self.info, True) \
        + utils.set_bg('view', self.globals['bgc'])

    self.file_name = view_controller
    self.swift[view_controller] = C
    self.gen_file(False)

  def gen_file(self, in_v):
    """
    Returns: Fills in the swift instance variable with generated file.
    """
    self.swift[self.file_name] += self.gen_comps(self.info["components"], in_v)

    types = [c['type'] for c in self.info["components"]]
    if "UIActionSheet" in types: # move UIActionSheet code to viewDidAppear
      self.swift[self.file_name] = move_action_sheet(self.swift[self.file_name])

    if not self.info["tc_elem"]:
      if in_v:
        self.swift[self.file_name] += "{}\n}}".format(utils.req_init())
      else:
        self.swift[self.file_name] += "}"
    else:
      # add parent classes for table/collection view
      self.swift[self.file_name] = subclass_tc(self.swift[self.file_name],
                                               self.info)
      self.swift[self.file_name] += '\n}}\n{}}}'.format(self.info["tc_methods"])

      tc_elem = self.info["tc_elem"]
      tc_id = tc_elem['id']
      tc_header = tc_elem.get('header')

      if tc_header is not None:
        # nested table/collection view
        if self.setup_cell_header('header', tc_id, tc_header):
          self.gen_file(True)

      tc_cell = tc_elem.get('cells')[0]
      # nested table/collection view
      if self.setup_cell_header('cell', tc_id, tc_cell):
        self.gen_file(True)

  def gen_comps(self, components, in_v):
    """
    Args:
      components: (dict list) contains information about components

    Returns (str): swift code to generate components.
    """
    self.clear_tv()
    navbar_item_ids = [] # holds ids of navbar items
    C = ""

    for comp in components:
      type_ = comp['type']
      if comp['id'] in navbar_item_ids:
        # navbar items already generated with navbar
        continue
      elif type_ == 'UITabBar':
        comp['active_vc'] = self.file_name # name of active view controller
        cf = ComponentFactory(type_, comp, in_v)
        # generate tabbar viewcontroller file
        vc_name = utils.uppercase(comp['id']) + 'ViewController'
        self.swift[vc_name] = gen_tabbar_vc(vc_name, cf.swift, self.info)
      else:
        if type_ == 'UILabel':
          if self.swift.get('InsetLabel') is None: # generate custom UILabel
            self.swift['InsetLabel'] = gen_inset_label()
          cf = ComponentFactory(type_, comp, in_v, bgc=self.globals['bgc'])
        else:
          cf = ComponentFactory(type_, comp, in_v)
          if type_ == 'UITableView' or type_ == 'UICollectionView':
            self.info["tc_elem"] = comp
            self.info["tc_methods"] = cf.tc_methods
          elif type_ == 'UINavBar':
            items = comp["navbar-items"]
            navbar_item_ids.extend([i['id'] for i in items['left-buttons']])
            navbar_item_ids.extend([i['id'] for i in items['right-buttons']])
            if items.get('title') is not None:
              title = items['title']
              navbar_item_ids.append(title['id'])
              navbar_item_ids.extend(c['id'] for c in title['components'])
        C += cf.swift
    return C

  def setup_cell_header(self, type_, id_, info):
    """
    Returns (bool):
      True if there is an nested (table/collection) view, False otherwise.
      NOTE: also sets up (table/collection)view header/cell file.
    """
    if type_ == "cell":
      self.file_name = utils.uppercase(id_) + "Cell"
      C = gen_cell_header(id_, info)
      C += utils.setup_rect(id_, info.get('rect'), tc_cell=True)
    else: # type_ is header
      self.file_name = utils.uppercase(id_) + "HeaderView"
      C = gen_header_header(id_, info)
      C += utils.setup_rect(id_, info.get('rect'), tc_header=True)

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

  def clear_tv(self):
    """
    Returns (None): Resets tc_elem and tc_methods instance variables
    """
    self.info["tc_elem"] = {}
    self.info["tc_methods"] = ""
