from . import *

class UISearchBar(BaseComponent):
  """
  Class representing a UISearchBar in swift
  """
  def generate_swift(self):
    return self.setup_component()

  def setup_component(self):
    """
    Returns: swift code to setup uiview.
    """
    return ('{0}.searchBarStyle = .minimal\n{0}.placeholder = "{1}"\n'
           ).format(self.id, self.info["contents"].decode('utf-8'))
