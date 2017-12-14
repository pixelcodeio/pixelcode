from components.component_factory import ComponentFactory
import utils

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
    view_controller = self.globals['artboard'].capitalize() + 'ViewController'
    C = self.gen_viewcontroller_header(view_controller, True) \
        + utils.set_bg('view', self.globals['bgc'])

    self.info["components"] = components
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
    header += self.declare_g_vars() if declare_vars else ""
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

  def gen_cell_header(self, tc_id, cell):
    """
    Args:
      tc_id (str): id of the parent (table/collection)view
      cell (dict): info of cell being generated

    Returns (str): swift code to generate the header of a cell
    """
    tc_id = tc_id.capitalize()
    C = ("import UIKit\nimport SnapKit\n\nclass {}Cell: UITableViewCell "
         "{{\n\n{}"
         "\noverride init(style: UITableViewCellStyle, reuseIdentifier: "
         "String?) {{\n"
         "super.init(style: style, reuseIdentifier: reuseIdentifier)\n"
         "layoutSubviews()\n}}\n\n"
         "override func layoutSubviews() {{\n"
         "super.layoutSubviews()\n\n"
        ).format(tc_id, self.init_g_vars(cell.get('components')))

    if "collection" in tc_id or "Collection" in tc_id:
      C = C.replace('style: UITableViewCellStyle, reuseIdentifier: String?',
                    'frame: CGRect')
      C = C.replace('style: style, reuseIdentifier: reuseIdentifier',
                    'frame: frame')
      C = C.replace('Table', 'Collection')

    return C

  def gen_header_header(self, tc_id, header):
    """
    Args:
      tc_id (str): id of the parent (table/collection)view
      header: (dict) info of header being generated

    Returns (str): swift code for generating the header of a header
    """
    tc_id = tc_id.capitalize()
    C = ("import UIKit\nimport SnapKit\n\nclass {}HeaderView: "
         "UITableViewHeaderFooterView {{\n\n{}"
         "\noverride init(reuseIdentifier: String?) {{\n"
         "super.init(reuseIdentifier: reuseIdentifier)\n"
         "layoutSubviews()\n}}\n\n"
         "override func layoutSubviews() {{"
         "\nsuper.layoutSubviews()\n\n"
        ).format(tc_id, self.init_g_vars(header.get('components')))

    if "collection" in tc_id or "Collection" in tc_id:
      C = C.replace('reuseIdentifier: String?', 'frame: CGRect')
      C = C.replace('reuseIdentifier: reuseIdentifier', 'frame: frame')
      C = C.replace('UITableViewHeaderFooterView', 'UICollectionReusableView')

    return C

  def declare_g_vars(self):
    """
    Returns (str): swift code to declare global variables
    """
    components = list(self.info["components"]) # get copy of components
    navbar_items = [c.get("navbar-items") for c in components]
    navbar_items = [n for n in navbar_items if n is not None]
    if navbar_items:
      navbar_items = navbar_items[0] # only one nav bar per screen
      components.extend(navbar_items['left-buttons'])
      components.extend(navbar_items['right-buttons'])
      if navbar_items.get('title') is not None:
        components.append(navbar_items['title'])
        if navbar_items['title'].get('components') is not None:
          components.extend(navbar_items['title']['components'])

    # filter components to not include navigation bar
    filter_comps = [c for c in components if c['type'] != 'UINavBar']

    # one-liner to concat all variable names
    gvars = ["var {}: {}!\n".format(e['id'], e['type']) for e in filter_comps]
    return "".join(gvars)

  def init_g_vars(self, components):
    """
    Args:
      components: (dict list) contains info about components

    Returns (str): swift code to generate/init all glob vars of components
    """
    C = ""
    for comp in components:
      if comp['type'] == 'UICollectionView': # do not init collection views
        C += "var {}: UICollectionView!\n".format(comp['id'])
      elif comp['type'] == 'UINavBar': # cannot init navigation bars
        continue
      else:
        C += "var {} = {}()\n".format(comp['id'], comp['type'])
    return C

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
        comp['active-vc'] = self.file_name # name of active view controller
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
    view_controller = id_.capitalize() + 'ViewController'
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
      self.file_name = id_.capitalize() + "Cell"
      C = self.gen_cell_header(id_, info)
      C += utils.setup_rect(id_, info.get('rect'), True, tc_cell=True)
    else: # type_ is header
      self.file_name = id_.capitalize() + "HeaderView"
      C = self.gen_header_header(id_, info)
      C += utils.setup_rect(id_, info.get('rect'), True, tc_header=True)

    C += self.gen_comps(info.get('components'), True)
    C += "}}\n\n{}\n\n".format(utils.req_init())
    self.swift[self.file_name] = C

    tc_elem = self.info["tc_elem"]
    if not tc_elem:
      self.swift[self.file_name] += "}"
      return False

    # inner table/collection view exists
    if tc_elem['type'] == 'UICollectionView':
      self.move_collection_view()
    self.subclass_tc() # add parent classes for table/collection view
    self.swift[self.file_name] += "\n{}\n}}\n".format(self.info["tc_methods"])
    id_ = tc_elem['id']
    cell = tc_elem.get('cells')[0]
    self.file_name = id_.capitalize() + 'Cell'
    self.swift[self.file_name] = self.gen_cell_header(id_, cell)
    # get components of first cell
    self.info["components"] = tc_elem.get('cells')[0].get('components')
    return True

  def move_collection_view(self):
    """
    Returns (None):
      Moves swift code that sets up UICollectionView to inside current file's
      init function.
    """
    C = self.swift[self.file_name]
    beg = C.find('layout.')
    mid = C.find('addSubview', beg)
    end = C.find('\n', mid)
    cv = ("let layout = UICollectionViewFlowLayout()\n"
          "{} = {}(frame: .zero, collectionViewLayout: layout)\n"
          "{}\n"
         ).format(self.info['tc_elem']['id'], 'UICollectionView', C[beg:end])
    C = C[:beg] + C[end:]

    if 'reuseIdentifier)\n' in C:
      C = utils.ins_after_key(C, 'reuseIdentifier)\n', cv)
    elif 'frame)\n' in C:
      C = utils.ins_after_key(C, 'frame)\n', cv)

    self.swift[self.file_name] = C
