import utils

class BaseComponent(object):
  """
  Base class for components
    swift: (str) the swift code used to generate a component
  """
  def __init__(self, id_, info, env):
    self.id = id_
    self.info = info
    self.env = env
    self.swift = self.generate_swift()

  def generate_swift(self):
    """
    Returns generated swift code; must be implemented in child
    """
    pass

  def create_font(self, font, size):
    """
    Args:
      font: (str) font family name
      size: (int) size of font

    Returns: The UIFont generated using font and size.
    """
    return ("UIFont(name: \"{}\", size: {})").format(font, size)

  def set_opacity(self, id_, opacity):
    """
    Args:
      id_: (str) id of the component
      opacity: (float) between 0 and 1

    Returns: (str) The swift code to set the opacity of elem.
    """
    return "{}.alpha = {}\n".format(id_, opacity)

  def clips_to_bounds(self, id_):
    """
    Args:
      id_: (str) id of element

    Returns: The swift code to set the clipsToBounds property of elem to true.
    """
    return "{}.clipsToBounds = true\n".format(id_)
