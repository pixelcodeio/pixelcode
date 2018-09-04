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
        if child["type"] == "UIImageView": # bound with an image fill
          components.append(child)
        if rect is None:
          rect = child
        else:
          raise Exception("Container: Multiple bound fields in " + elem["id"])
      else:
        components.append(child)

    elem["components"] = components
    elem["rect"] = rect
    return super().parse_elem(elem)
