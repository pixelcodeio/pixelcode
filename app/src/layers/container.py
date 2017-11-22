from . import *

class Container(BaseLayer):
  """
  Class representing a Container in Sketch (bounding box + children)
  """
  def parse_elem(self, elem):
    """
    Args:
      Refer to args in __init__
    """
    rect = None
    components = []
    for child in elem["children"]:
      if child["type"] == "UIView" and \
         ("Bound" in child["id"] or "bound" in child["id"]):
        if rect is None:
          rect = child
        else:
          raise Exception("Container: Multiple fields named bound.")
      else:
        components.append(child)

    if rect is None:
      raise Exception("Container: No bound field.")

    elem["rect"] = rect
    elem["components"] = components
    return super().parse_elem(elem)
