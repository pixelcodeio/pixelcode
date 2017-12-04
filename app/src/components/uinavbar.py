from . import *

class UINavBar(BaseComponent):
  """
  Class representing a UINavBar in swift
  """
  def generate_swift(self):
    return self.setup_component()

  def setup_component(self):
    """
    Returns: (str) swift code to setup uinavbar items
    """
    C = self.info['left-buttons-code']
    C += self.add_barbuttons(True)

    C += self.info['right-buttons-code']
    C += self.add_barbuttons(False)

    C += self.info['title-code']
    C += ('self.navigationItem.titleView = {}\n'
         ).format(self.info['navbar-items']['title']['id'])
    return C

  def add_barbuttons(self, left_or_right):
    """
    """
    dir_ = 'left' if left_or_right else 'right'
    ids = [b['id'] for b in self.info['navbar-items'][dir_ + '-buttons']]
    C = self.gen_barbuttons(ids)
    ids = [id_ + 'BarButton' for id_ in ids] # convert ids to its barbutton id
    C += ('self.navigationItem.{}BarButtonItems = [{}]\n\n'
         ).format(dir_, ", ".join(ids))
    return C

  def gen_barbuttons(self, ids):
    C = ""
    for id_ in ids:
      C += "let {0}BarButton = UIBarButtonItem(customView: {0})\n".format(id_)
    return C
