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
    return "{}.searchBarStyle = .minimal\n"
