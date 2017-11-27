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
    Returns: UIFont generated using font and size.
    """
    return ("UIFont(name: \"{}\", size: {})").format(font, size)

  def set_opacity(self, opacity):
    """
    Returns (str): swift code to set the opacity
    """
    return "{}.alpha = {}\n".format(self.id, opacity)

  def clips_to_bounds(self):
    """
    Args:
      id_ (str): id of element

    Returns: swift code to set the clipsToBounds property
    """
    return "{}.clipsToBounds = true\n".format(self.id)
