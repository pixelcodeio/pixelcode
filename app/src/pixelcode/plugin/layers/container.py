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
      if utils.word_in_str('bound', child["id"]):
        if rect is None:
          rect = child
        else:
          raise Exception("Container: Multiple bound fields in " + elem["id"])
      else:
        components.append(child)

    if rect is None:
      raise Exception("Container: No bound field in " + elem["id"])

    elem["components"] = components
    elem["rect"] = rect
    return super().parse_elem(elem)