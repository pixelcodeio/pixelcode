from layers.rect import Rect
from layers.text import Text
from . import *

class TabBar(BaseLayer):
  """
  Class representing a Tab Bar in Sketch
  """
  def parse_elem(self, elem):
    tabbar_buttons = []
    rect = None

    for child in elem["children"]:
      if utils.word_in_str("tabButton", child["id"]):
        child["active"] = utils.word_in_str("active", child["id"])
        tabbar_buttons.append(child)
      elif utils.word_in_str('bound', child["id"]):
        if rect:
          raise Exception("Tabbar: Only one bound allowed in " + elem["id"])
        else:
          rect = child
      else:
        raise Exception("Tabbar: Tavbar does not support: " + child["id"])

    if not tabbar_buttons:
      raise Exception("Tabbar: Tabbar is empty.")

    # sort buttons by x value
    tabbar_buttons = sorted(tabbar_buttons, key=lambda c: c.get('x'))

    elem["rect"] = rect
    elem["tabbar-buttons"] = tabbar_buttons
    return super().parse_elem(elem)
