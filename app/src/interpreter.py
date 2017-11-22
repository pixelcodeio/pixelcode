from components.component_factory import ComponentFactory
import components.utils as utils

class Interpreter(object):
  """
  Takes output from Parser one at a time and generates swift file
    globals: (dict) passed in from Parser
    swift: (str) the swift code to generate all the elements
  """
  def __init__(self, glob):
    glob['bgc'] = glob['background_color'] + ("1.0",) # adding opacity
    self.globals = glob
    self.swift = {}

  def gen_global_vars(self, elements):
    """
    Args:
      elements: (list) list of elements

    Returns: (str) The swift code of the global variables for the swift class
    """
    variables = ["var {}: {}!\n".format(e['id'], e['type']) for e in elements]
    return "".join(variables)

  def gen_vc_header(self, elements):
    """
    Args:
      elements: (list) list of elements

    Returns: The swift code of the header
    """
    artboard = self.globals['artboard'].capitalize()
    viewController = '{}ViewController'.format(artboard)
    h = ("import UIKit\nimport SnapKit\n\n"
         "class {}: UIViewController {{\n\n"
        ).format(viewController)
    h += self.gen_global_vars(elements)
    h += "\noverride func viewDidLoad() {\n"
    return h

  def gen_cell_header(self, tv_id, cell):
    """
    Args:
      tv_id: (str) the id of the parent tableview (capitalized)
      cell: (dict) the cell being generated

    Returns: (str) The swift code to generate the header of a UITableViewCell.
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
      tv_id: (str) the id of the parent tableview (capitalized)
      header: (dict) the header view being generated

    Returns: (str) The swift code for generating the header of a UITableView
             Header file.
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
      components: (dict list) contains information about components

    Returns: (str) The swift code to generate all the global variables of each
    component in components AND initialize them.
    """
    c = ""
    for comp in components:
      c += 'var {} = {}()\n'.format(comp.get('id'), comp.get('type'))
    return c

  def gen_comps(self, components, in_view):
    """
    Args:
      components: (dict list) contains information about components
      in_view: (bool) represents whether the components are being generated
               inside a custom view file (or not)

    Returns: (tuple) A triple consisting of:
      - the swift code to generate each component in components.
      - the dictionary of the tableview if components contains one.
      - the tableview methods for the tableview.
    """
    c = ""
    tv_elem = None
    tv_methods = ""
    for comp in components:
      typ = comp.get('type')
      if typ == 'UILabel':
        cf = ComponentFactory(typ, comp, bgc=self.globals['bgc'],
                              in_view=in_view)
        c += cf.swift
      else:
        cf = ComponentFactory(typ, comp, in_view=in_view)
        c += cf.swift
        if typ == 'UITableView':
          tv_elem = comp
          tv_methods = cf.tv_methods
    return (c, tv_elem, tv_methods)

  def gen_elements(self, elements, f_name, in_view=False):
    """
    Args:
      elements: (dict list) contains information of all the elements
      f_name: The name of the file.

    Returns: (str) The swift code of the to generate the elements.
    """
    c = self.swift[f_name]
    s, tv_elem, tv_methods = self.gen_comps(elements, in_view)
    c += s

    if tv_elem is None:
      c += "\n}\n}"
      self.swift[f_name] = c
    else:
      f = utils.ins_after_key(c, ": UIViewController",
                              ", UITableViewDelegate, UITableViewDataSource ")
      if f:
        c = f
      else:
        c = utils.ins_after_key(c, ": UITableViewCell",
                                ", UITableViewDelegate, UITableViewDataSource ")

      c += "\n}}\n{}}}\n".format(tv_methods)
      self.swift[f_name] = c

      # Generating tableview cell file:
      tv_id = tv_elem.get('id')
      tv_cells = tv_elem.get('cells')
      cap_id = tv_id.capitalize()
      tv_cell = tv_cells[0]
      c = ""
      c += self.gen_cell_header(cap_id, tv_cell)

      rect = tv_cell.get('rect')
      c += utils.setup_rect(tv_id, rect, in_view=True)

      # ctv_elem represents a tableview inside a cell
      s, ctv_elem, ctv_methods = self.gen_comps(tv_cell.get('components'),
                                                in_view=True)
      c += s
      c += "}}\n\n{}\n\n".format(utils.required_init())

      if ctv_elem is None:
        c += "}"
        self.swift[cap_id + 'Cell'] = c
      else:
        c = utils.ins_after_key(c, ": UITableViewCell",
                                ", UITableViewDelegate, UITableViewDataSource ")
        c += "\n{}}}\n".format(ctv_methods)
        self.swift[cap_id + 'Cell'] = c

        # Generating cell within a tableview cell
        ctv_id = ctv_elem.get('id')
        ctv_cells = ctv_elem.get('cells')
        ctv_cell = ctv_cells[0]
        cap_ctv_id = ctv_id.capitalize()
        c = ""
        c += self.gen_cell_header(cap_ctv_id, ctv_cell)
        self.swift[cap_ctv_id + 'Cell'] = c
        self.gen_elements(ctv_elem, cap_ctv_id + 'Cell', in_view=True)

      tv_header = tv_elem.get('header')
      if tv_header is not None:
        c = ""
        c += self.gen_header_header(cap_id, tv_header)
        c += utils.setup_rect(tv_id, tv_header.get('rect'), in_view=True,
                              tv_header=True)
        c += (self.gen_comps(tv_header.get('components'), in_view=True))[0]
        c += "}}\n\n{}\n\n}}".format(utils.required_init())
        self.swift[cap_id + 'HeaderView'] = c

  def gen_code(self, elements):
    """
    Args:
      elements: (list) list of elements

    Returns: (None) Fills in the swift instance variable with the swift code
             to generate all the elements.
    """
    file_h = self.gen_vc_header(elements)
    file_h += utils.set_bg('view', self.globals['bgc'])
    ab = self.globals['artboard'].capitalize()
    vc = '{}ViewController'.format(ab)
    self.swift[vc] = file_h
    self.gen_elements(elements, vc)
