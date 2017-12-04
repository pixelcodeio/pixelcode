from layers.rect import Rect
from layers.text import Text
from . import *

class NavBar(BaseLayer):
  """
  Class representing a Navigation Bar in Sketch
  """
  def parse_elem(self, elem):
    navbar_items = {}
    left_bar_buttons = []
    right_bar_buttons = []
    title_view = None
    for child in elem["children"]:
      if "titleView" in child["id"] or "TitleView" in child["id"]:
        if title_view:
          raise Exception("Navbar: Only one title view allowed.")
        else:
          title_view = child
      elif "barButton" in child["id"] or "BarButton" in child["id"]:
        if child["x"] < 375.0/2: # on left side of screen
          left_bar_buttons.append(child)
        else:
          right_bar_buttons.append(child)
      else:
        raise Exception("Navbar: Navbar has unsupported elements.")

    if title_view is None and not left_bar_buttons and not right_bar_buttons:
      raise Exception("Navbar: Navbar is empty.")

    # sort buttons by x value
    left_bar_buttons = sorted(left_bar_buttons, key=lambda c: c.get('x'))
    right_bar_buttons = sorted(right_bar_buttons, key=lambda c: c.get('x'))

    navbar_items["left-bar-buttons"] = left_bar_buttons
    navbar_items["right-bar-buttons"] = right_bar_buttons
    navbar_items["title-view"] = title_view

    elem["navbar-items"] = navbar_items

    return super().parse_elem(elem)
