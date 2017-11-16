import components.utils as utils

class UITableView(object):
  """
  Class representing a UITableView in swift
  """
  def __init__(self):
    pass

  def setup_uitableview(self, elem, cells):
    """
    Args:
      elem: (str) id of the component
      cells: see generate_component's docstring for more information

    Returns: The swift code to setup a UITableView in viewDidLoad.
    """
    capElem = elem.capitalize()
    c = ('{}.register({}Cell.self, forCellReuseIdentifier: "{}ID")\n'
         '{}.delegate = self\n'
         '{}.dataSource = self\n'
        ).format(elem, capElem, elem, elem, elem)
    return c
