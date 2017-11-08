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

  def generate_header(self):
    """
    Returns: The swift code of the header
    """
    viewController = '{}ViewController'.format(self.globals['artboard'])
    return ("import UIKit\nclass {}: UIViewController {{\n"
            "\noverride func viewDidLoad() {{\n"
           ).format(viewController)

  def set_view_bg(self):
    """
    Returns: The swift code to set the view's background color.
    """
    bg = self.globals['background_color']
    r = bg[0]
    g = bg[1]
    b = bg[2]
    return ("view.backgroundColor = UIColor(red: {}/255.0, green: {}/255.0,"
            " blue: {}/255.0, alpha: 1.0)\n\n"
           ).format(r, g, b)

  def generate_code(self, elements):
    """
    Args:
      elements: (list) list of elements

    Returns: The swift code for the file to generate all the elements
    """
    c = self.generate_header()
    c += self.set_view_bg()
    for elem in elements:
      comp = elem["type"]
      if comp == 'UILabel':
        bc = BaseComponent(comp, elem, self.globals['background_color'])
        c += bc.swift
      else:
        bc = BaseComponent(comp, elem)
        c += bc.swift
    c += "\n}\n}"
    self.swift = c
