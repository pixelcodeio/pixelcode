from layers.rect import Rect
from layers.text import Text
from . import *

class NavBar(BaseLayer):
  """
  Class representing a Navigation Bar in Sketch
  """
  def parse_elem(self, elem):
    left_button = None
    right_button = None
    title = None
    for child in elem["children"]:
      if child["type"] == "UIBarButtonItem":
        if child["x"] < 375.0/2:
          if left_button:
            raise Exception("Navbar: Only one left button allowed.")
          else:
            left_button = child
        else:
          if right_button:
            raise Exception("Navbar: Only one right button allowed.")
          else:
            right_button = child
      elif child["type"] == "UIView":
        if title:
          raise Exception("Navbar: Only one title view allowed.")
        else:
          title = child

    if title is None and left_button is None and right_button is None:
      raise Exception("Navbar: Navbar is empty.")

    elem["left-button"] = left_button
    elem["right-button"] = right_button
    elem["title"] = title

    return super().parse_elem(elem)
