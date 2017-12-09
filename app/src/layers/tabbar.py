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
      if "tabButton" in child["id"] or "TabButton" in child["id"]:
        tabbar_buttons.append(child)
      elif "wash" in child["id"]:
        if rect:
          raise Exception("Tabbar: Only one wash allowed in " + elem["id"])
        else:
          rect = child
      else:
        raise Exception("Tabbar: Tavbar does not support: " + child["id"])

    if not tabbar_buttons:
      raise Exception("Tabbar: Tabbar is empty.")

    # sort buttons by x value
    tabbar_buttons = sorted(tabbar_buttons, key=lambda c: c.get('x'))

    elem["tabbar-buttons"] = tabbar_buttons
    elem["rect"] = rect

    return super().parse_elem(elem)
