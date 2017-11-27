from components.component_factory import ComponentFactory
import utils

class Interpreter(object):
  """
  Takes output from Parser one at a time and generates swift file
    globals: (dict) passed in from Parser
    swift: (dict) swift code to generate all elements
  """
  def __init__(self, globals_):
    globals_['bgc'] = globals_['background_color'] + ("1.0",) # adding opacity
    self.globals = globals_
    self.swift = {}

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
    C = ""
    tv_elem = None
    tv_methods = ""
    for comp in components:
      type_ = comp.get('type')
      if type_ == 'UILabel':
        cf = ComponentFactory(type_, comp, bgc=self.globals['bgc'],
                              in_v=in_v)
        C += cf.swift
      else:
        cf = ComponentFactory(type_, comp, in_v=in_v)
        C += cf.swift
        if type_ == 'UITableView':
          tv_elem = comp
          tv_methods = cf.tv_methods
    return (C, tv_elem, tv_methods)

  def gen_elements(self, elements, f_name, in_v=False):
    """
    Args:
      elements: (dict list) contains information of all the elements
      f_name: The name of the file.

    Returns: Fills in the swift instance variable with generated code.
    """
    C = self.swift[f_name]
    s, tv_elem, tv_methods = self.gen_comps(elements, in_v)
    C += s

    if tv_elem is None:
      C += "\n}\n}"
      self.swift[f_name] = C
    else:
      ins = utils.ins_after_key(C, ": UIViewController",
                                ", UITableViewDelegate, UITableViewDataSource ")
      if ins:
        C = ins
      else:
        C = utils.ins_after_key(C, ": UITableViewCell",
                                ", UITableViewDelegate, UITableViewDataSource ")

      C += "\n}}\n{}}}\n".format(tv_methods)
      self.swift[f_name] = C

      # Generating tableview cell file:
      tv_id = tv_elem.get('id')
      tv_cells = tv_elem.get('cells')
      cap_id = tv_id.capitalize()
      tv_cell = tv_cells[0]
      C = self.gen_cell_header(cap_id, tv_cell)

      rect = tv_cell.get('rect')
      C += utils.setup_rect(tv_id, rect, in_v=True)

      # ctv_elem represents a tableview inside a cell
      swift, ctv_elem, ctv_methods = self.gen_comps(tv_cell.get('components'),
                                                    in_v=True)
      C += swift
      C += "}}\n\n{}\n\n".format(utils.required_init())

      if ctv_elem is None:
        C += "}"
        self.swift[cap_id + 'Cell'] = C
      else:
        C = utils.ins_after_key(C, ": UITableViewCell",
                                ", UITableViewDelegate, UITableViewDataSource ")
        C += "\n{}}}\n".format(ctv_methods)
        self.swift[cap_id + 'Cell'] = C

        # Generating cell within a tableview cell
        ctv_id = ctv_elem.get('id')
        ctv_cells = ctv_elem.get('cells')
        ctv_cell = ctv_cells[0]
        cap_ctv_id = ctv_id.capitalize()
        C = self.gen_cell_header(cap_ctv_id, ctv_cell)
        self.swift[cap_ctv_id + 'Cell'] = C
        self.gen_elements(ctv_elem, cap_ctv_id + 'Cell', in_v=True)

      tv_header = tv_elem.get('header')
      if tv_header is not None:
        C = self.gen_header_header(cap_id, tv_header)
        C += utils.setup_rect(tv_id, tv_header.get('rect'), in_v=True,
                              tv_header=True)
        C += (self.gen_comps(tv_header.get('components'), in_v=True))[0]
        C += "}}\n\n{}\n\n}}".format(utils.required_init())
        self.swift[cap_id + 'HeaderView'] = C

  def gen_code(self, elements):
    """
    Args:
      elements: (list) list of elements

    Returns: Fills in the swift instance var with generated code for artboard.
    """
    file_h = self.gen_vc_header(elements)
    file_h += utils.set_bg('view', self.globals['bgc'])
    ab = self.globals['artboard'].capitalize()
    vc = '{}ViewController'.format(ab)
    self.swift[vc] = file_h
    self.gen_elements(elements, vc)
