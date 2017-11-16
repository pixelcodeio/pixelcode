from . import *

class Cell(BaseLayer):
  """
  Class representing a Cell in Sketch
  """
  def parse_elem(self, elem):
    """
    Args:
      Refer to args in __init__
    """
    rect = None
    components = []
    for child in elem["children"]:
      if child["type"] == "UIView" and "Bound" in child["id"]:
        if rect is None:
          rect = child
        else:
          raise Exception("Multiple fields named bound.")
      else:
        components.append(child)

    if rect is None:
      raise Exception("No bound field. for elem " + elem["id"])

    elem["rect"] = rect
    elem["components"] = components
    return super(Cell, self).parse_elem(elem)
