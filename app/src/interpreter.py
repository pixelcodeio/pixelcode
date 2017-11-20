from components.base_component import BaseComponent

class Interpreter(object):
  """
  Takes output from Parser one at a time and generates swift file
    globals: (dict) passed in from Parser
    swift: (str) the swift code to generate all the elements
  """
  def __init__(self, glob):
    self.globals = glob
    self.swift = ""

  def generate_global_vars(self, elements):
    """
    Args:
      elements: (list) list of elements

    Returns: The swift code of the global variables for the swift class
    """
    g = ""
    for elem in elements:
      g += "var {}: {}!\n".format(elem['id'], elem['type'])
    return g

  def generate_header(self, elements):
    """
    Args:
      elements: (list) list of elements

    Returns: The swift code of the header
    """
    artboard = self.globals['artboard'].capitalize()
    viewController = '{}ViewController'.format(artboard)
    h = ("import UIKit\nimport SnapKit\n\nclass {}: UIViewController {{\n\n"
        ).format(viewController)
    h += self.generate_global_vars(elements)
    h += "\noverride func viewDidLoad() {\n"
    return h

  def set_view_bg(self):
    """
    Returns: The swift code to set the view's background color.
    """
    bg = self.globals['background_color']
    r, g, b = bg
    return ("view.backgroundColor = UIColor(red: {}/255.0, green: {}/255.0,"
            " blue: {}/255.0, alpha: 1.0)\n\n"
           ).format(r, g, b)

  def generate_code(self, elements):
    """
    Args:
      elements: (list) list of elements

    Returns: The swift code for the file to generate all the elements
    """
    c = self.generate_header(elements)
    c += self.set_view_bg()
    tableViewExists = False
    tableViewElem = None
    tableViewMethods = ""
    for elem in elements:
      comp = elem["type"]
      if comp == 'UILabel':
        # if elem['id'] == 'top':
        #   print(elem)
        bc = BaseComponent(comp, elem, self.globals['background_color'])
        c += bc.swift
      else:
        bc = BaseComponent(comp, elem)
        c += bc.swift
        if comp == 'UITableView':
          tableViewElem = elem
          tableViewExists = True
          tableViewMethods = bc.tableViewMethods
    if tableViewExists is False:
      c += "\n}\n}"
      self.swift = c
      return
    # else:
    indexVC = c.index(": UIViewController")
    c = ("{}, UITableViewDelegate, UITableViewDataSource {}"
        ).format(c[:indexVC+18], c[indexVC+18:])
    c += "\n}}\n{}}}\n".format(tableViewMethods)
    c += "TableViewCell File: \n"
    bc = BaseComponent('UITableView', tableViewElem, None, True)
    c += bc.cell
    if tableViewElem['header'] is not None:
      bc = BaseComponent('UITableView', tableViewElem, None, False, True)
      c += "\nTableViewHeader File: \n"
      c += bc.tableViewHeader
    self.swift = c
