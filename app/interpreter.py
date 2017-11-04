from components import *

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

  def generate_code(self, elements):
    """
    Args:
      elements: (list) list of elements

    Returns: The swift code for the file to generate all the elements
    """
    c = self.generate_header()
    for ele in elements:
      t = ele["type"]
      if t == "UIView":
        v = UIView(ele)
        c += v.swift
      elif t == "UIButton":
        b = UIButton(ele)
        c += b.swift
      elif t == "UIImageView":
        iv = UIImageView(ele)
        c += iv.swift
      elif t == "UILabel":
        l = UILabel(ele)
        c += l.swift
    c += "\n}\n}"
    self.swift = c
