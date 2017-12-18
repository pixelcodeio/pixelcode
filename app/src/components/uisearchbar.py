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
    C = ('{0}.searchBarStyle = .minimal\n{0}.placeholder = "{1}"\n'
        ).format(self.id, self.info["contents"].decode('utf-8'))
    if self.info.get("search-icon"):
      C += self.set_img(self.info['search-icon']['path'], '.search')
    if self.info.get("bookmark-icon"):
      C += ('{}.showsBookmarkButton = true\n').format(self.id)
      C += self.set_img(self.info['bookmark-icon']['path'], '.bookmark')
    return C

  def set_img(self, path, icon_type):
    """
    Returns (str): swift code to set image of type icon_type
    """
    return ('{}.setImage(UIImage(named: "{}"), for: {}, state: .normal)\n'
           ).format(self.id, path, icon_type)
