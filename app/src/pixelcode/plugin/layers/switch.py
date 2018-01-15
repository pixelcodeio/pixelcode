from . import *

class Switch(BaseLayer):
  """
  Class representing a Switch in Sketch
  """
  def parse_elem(self, elem):
    rect = None

    for child in elem["children"]:
      if utils.word_in_str("bound", child["id"]):
        rect = child

    if rect is None:
      raise Exception("Switch: No bound in switch.")

    elem["is_on"] = utils.word_in_str("off", elem["id"])
    elem["rect"] = rect
    return super().parse_elem(elem)
