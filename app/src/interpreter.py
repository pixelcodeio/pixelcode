from components.component_factory import ComponentFactory
import utils

class Interpreter(object):
  """
  Takes output from Parser one at a time and generates swift file
    globals (dict): passed in from Parser
    file_name (str): name of current file being generated
    elements (dict): info on all components
    tc_elem (dict): info on current (table/collection)view being generated
    tc_methods (str): necessary (table/collection)view methods
    swift (dict): swift code to generate all elements
  """
  def __init__(self, globals_):
    globals_['bgc'] = globals_['background_color'] + ("1.0",) # adding opacity
    self.globals = globals_
    self.file_name = ""
    self.elements = None
    self.tc_elem = None
    self.tc_methods = ""
    self.swift = {}

  def clear_tv(self):
    """
    Returns (None): Resets tc_elem and tc_methods instance variables
    """
    self.tc_elem = None
    self.tc_methods = ""

  def gen_global_vars(self, elements):
    """
    Args:
      elements (list): list of elements from Parser

    Returns: (str) swift code of the global variables
    """
    # one-liner to concat all variable names
    variables = ["var {}: {}!\n".format(e['id'], e['type']) for e in elements]
    return "".join(variables)

  def gen_vc_header(self, elements):
    """ Generates header of view controller
    Args:
      elements (list): list of elements

    Returns (str): swift code of the header
    """
    artboard = self.globals['artboard'].capitalize()
    viewController = '{}ViewController'.format(artboard)
    header = ("import UIKit\nimport SnapKit\n\n"
              "class {}: UIViewController {{\n\n"
             ).format(viewController)
    header += self.gen_global_vars(elements)
    header += "\noverride func viewDidLoad() {\n"
    return header

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
      C = C.replace('TableView', 'CollectionView')

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

  def init_g_vars(self, components):
    """
    Args:
      components: (dict list) contains info about components

    Returns (str): swift code to generate/init all glob vars of components
    """
    C = ""
    for comp in components:
      C += "var {} = {}()\n".format(comp.get('id'), comp.get('type'))
    return C

  def gen_comps(self, components, in_v):
    """
    Args:
      components: (dict list) contains information about components

    Returns:
      (tuple) A triple consisting of:
        - swift code to generate components.
        - dict of the tableview or None
        - tableview methods for the tableview.
    """
    self.clear_tv()
    C = ""
    for comp in components:
      type_ = comp.get('type')
      if type_ == 'UILabel':
        cf = ComponentFactory(type_, comp, in_v, bgc=self.globals['bgc'])
        C += cf.swift
      else:
        cf = ComponentFactory(type_, comp, in_v)
        C += cf.swift
        if type_ == 'UITableView' or type_ == 'UICollectionView':
          self.tc_elem = comp
          self.tc_methods = cf.tc_methods

    return C

  def subclass_tc(self):
    """
    Returns (None): adds necessary (table/collection)view parent classes
    """
    C = self.swift[self.file_name]
    ext = ", UITableViewDelegate, UITableViewDataSource"
    if self.tc_elem.get('type') == 'UICollectionView':
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

  def setup_tv_ch(self, type_, id_, info):
    """
    Returns (bool):
      fills in swift var with code to setup (table/collection)view header/cell
      file. True if there is an inner tableview, False otherwise.
    """
    if type_ == "cell":
      self.file_name = id_.capitalize() + "Cell"
      C = self.gen_cell_header(id_, info)
      C += utils.setup_rect(id_, info.get('rect'), True, tc_cell=True)
    else: # must be tableview header
      self.file_name = id_.capitalize() + "HeaderView"
      C = self.gen_header_header(id_, info)
      C += utils.setup_rect(id_, info.get('rect'), True, tc_header=True)

    C += self.gen_comps(info.get('components'), True)
    C += "}}\n\n{}\n\n".format(utils.required_init())

    if self.tc_elem is None:
      self.swift[self.file_name] = C + "}"
      return False

    # inner tableview exists
    self.subclass_tc()
    C += "\n{}\n}\n".format(self.tc_methods)
    self.swift[self.file_name] = C
    id_ = self.tc_elem.get('id')
    cell = self.tc_elem.get('cells')[0]
    self.file_name = id_.capitalize() + 'Cell'
    self.swift[self.file_name] = self.gen_cell_header(id_, cell)
    self.elements = self.tc_elem
    return True

  def gen_elements(self, in_v):
    """
    Returns: Fills in the swift instance variable with generated code.
    """
    self.swift[self.file_name] += self.gen_comps(self.elements, in_v)

    if self.tc_elem is None:
      self.swift[self.file_name] += "\n}\n}"
    else:
      self.subclass_tc()
      self.swift[self.file_name] += "\n}}\n{}}}\n".format(self.tc_methods)

      tc_elem = self.tc_elem
      tc_id = tc_elem.get('id')
      tc_header = tc_elem.get('header')

      if tc_header is not None:
        if self.setup_tv_ch('header', tc_id, tc_header): # nested table view
          self.gen_elements(True)

      tc_cell = tc_elem.get('cells')[0]
      if self.setup_tv_ch("cell", tc_id, tc_cell): # nested table view
        self.gen_elements(True)

  def gen_code(self, elements):
    """
    Args:
      elements: (list) list of elements

    Returns: Fills in the swift instance var with generated code for artboard.
    """
    C = self.gen_vc_header(elements) + utils.set_bg('view', self.globals['bgc'])
    vc = '{}ViewController'.format(self.globals['artboard'].capitalize())
    self.file_name = vc
    self.swift[vc] = C
    self.elements = elements
    self.gen_elements(False)
