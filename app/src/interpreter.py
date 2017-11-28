from components.component_factory import ComponentFactory
import utils

class Interpreter(object):
  """
  Takes output from Parser one at a time and generates swift file
    globals (dict): passed in from Parser
    file_name (str): name of current file being generated
    elements (dict): info on all components
    tv_elem (dict): info on current tableview being generated, if any
    tv_methods (str): necessary tableview methods, if needed
    swift (dict): swift code to generate all elements
  """
  def __init__(self, globals_):
    globals_['bgc'] = globals_['background_color'] + ("1.0",) # adding opacity
    self.globals = globals_
    self.file_name = ""
    self.elements = None
    self.tv_elem = None
    self.tv_methods = ""
    self.swift = {}

  def clear_tv(self):
    """
    Returns (None): Resets tv_elem and tv_methods instance variables
    """
    self.tv_elem = None
    self.tv_methods = ""

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

  def gen_cell_header(self, tv_id, cell):
    """
    Args:
      tv_id (str): id of the parent tableview
      cell (dict): info of cell being generated

    Returns (str): swift code to generate the header of a cell
    """
    tv_id = tv_id.capitalize()
    return ("import UIKit\nimport SnapKit\n\nclass {}Cell: UITableViewCell "
            "{{\n\n{}"
            "\noverride init(style: UITableViewCellStyle, reuseIdentifier: "
            "String?) {{\n"
            "super.init(style: style, reuseIdentifier: reuseIdentifier)\n"
            "layoutSubviews()\n}}\n\n"
            "override func layoutSubviews() {{\n"
            "super.layoutSubviews()\n\n"
           ).format(tv_id, self.init_g_vars(cell.get('components')))

  def gen_header_header(self, tv_id, header):
    """
    Args:
      tv_id (str): id of the parent tableview
      header: (dict) info of header being generated

    Returns (str): swift code for generating the header of a header
    """
    tv_id = tv_id.capitalize()
    return ("import UIKit\nimport SnapKit\n\nclass {}HeaderView: "
            "UITableViewHeaderFooterView {{\n\n{}"
            "\noverride init(reuseIdentifier: String?) {{\n"
            "super.init(reuseIdentifier: reuseIdentifier)\n"
            "layoutSubviews()\n}}\n\n"
            "override func layoutSubviews() {{"
            "\nsuper.layoutSubviews()\n\n"
           ).format(tv_id, self.init_g_vars(header.get('components')))

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
        if type_ == 'UITableView':
          self.tv_elem = comp
          self.tv_methods = cf.tv_methods
    return C

  def subclass_tv(self):
    """
    Returns (None): adds necessary parent (tableview) classes to current file
    """
    C = self.swift[self.file_name]
    tv_ext = ", UITableViewDelegate, UITableViewDataSource "

    if ": UIViewController" in C:
      C = utils.ins_after_key(C, ": UIViewController", tv_ext)
    elif ": UITableViewCell" in C:
      C = utils.ins_after_key(C, ": UITableViewCell", tv_ext)
    elif ": UITableViewHeaderFooterView" in C:
      C = utils.ins_after_key(C, ": UITableViewHeaderFooterView", tv_ext)
    else:
      raise Exception("interpreter: can't generate inner tableview")

    self.swift[self.file_name] = C

  def setup_tv_ch(self, type_, id_, info):
    """
    Returns (bool):
      fills in swift var with code to setup tableview header/cell file.
      True if there is an inner tableview, False otherwise.
    """
    if type_ == "cell":
      self.file_name = id_.capitalize() + "Cell"
      C = self.gen_cell_header(id_, info)
      C += utils.setup_rect(id_, info.get('rect'), True, tv_cell=True)
    else: # must be tableview header
      self.file_name = id_.capitalize() + "HeaderView"
      C = self.gen_header_header(id_, info)
      C += utils.setup_rect(id_, info.get('rect'), True, tv_header=True)

    C += self.gen_comps(info.get('components'), True)
    C += "}}\n\n{}\n\n".format(utils.required_init())

    if self.tv_elem is None:
      self.swift[self.file_name] = C + "}"
      return False
    else: # inner tableview exists
      self.subclass_tv()
      C += "\n{}\n}\n".format(self.tv_methods)
      self.swift[self.file_name] = C
      id_ = self.tv_elem.get('id')
      cell = self.tv_elem.get('cells')[0]
      self.file_name = id_.capitalize() + 'Cell'
      self.swift[self.file_name] = self.gen_cell_header(id_, cell)
      self.elements = self.tv_elem
      return True

  def gen_elements(self, in_v):
    """
    Returns: Fills in the swift instance variable with generated code.
    """
    self.swift[self.file_name] += self.gen_comps(self.elements, in_v)

    if self.tv_elem is None:
      self.swift[self.file_name] += "\n}\n}"
    else:
      self.subclass_tv()
      self.swift[self.file_name] += "\n}}\n{}}}\n".format(self.tv_methods)

      tv_elem = self.tv_elem
      tv_id = tv_elem.get('id')
      tv_header = tv_elem.get('header')

      if tv_header is not None:
        if self.setup_tv_ch('header', tv_id, tv_header): # nested tableview
          self.gen_elements(True)

      tv_cell = tv_elem.get('cells')[0]
      if self.setup_tv_ch("cell", tv_id, tv_cell): # nested tableview
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
