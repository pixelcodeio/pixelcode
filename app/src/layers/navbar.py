from layers.rect import Rect
from layers.text import Text
from . import *

class NavBar(BaseLayer):
  """
  Class representing a Navigation Bar in Sketch
  """
  def parse_elem(self, elem):
    left_bar_button = None
    right_bar_button = None
    title = None
    for child in elem["children"]:
      if child["type"] == "UIView":
        if "barButton" in child["id"] or "BarButton" in child["id"]:
          if child["x"] < 375.0/2:
            if left_bar_button:
              raise Exception("Navbar: Only one left button allowed.")
            else:
              left_bar_button = child
          else:
            if right_bar_button:
              raise Exception("Navbar: Only one right button allowed.")
            else:
              right_bar_button = child
        else:
          if title:
            raise Exception("Navbar: Only one title view allowed.")
          else:
            title = child
      else:
        raise Exception("Navbar: Navbar has unsupported elements.")

    if title is None and left_bar_button is None and right_bar_button is None:
      raise Exception("Navbar: Navbar is empty.")

    elem["left-bar-button"] = left_bar_button
    elem["right-bar-button"] = right_bar_button
    elem["title"] = title

    return super().parse_elem(elem)
