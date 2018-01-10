from .rect import Rect
from .text import Text
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
    rect = None
    for child in elem["children"]:
      if utils.word_in_str('titleView', child["id"]):
        if title_view:
          raise Exception("Navbar: Only one title view allowed.")
        else:
          title_view = child
      elif utils.word_in_str('barButton', child["id"]):
        if child["x"] < 375.0/2: # on left side of screen
          left_bar_buttons.append(child)
        else:
          right_bar_buttons.append(child)
      elif utils.word_in_str("bound", child["id"]):
        if rect:
          raise Exception("Navbar: Only one bound allowed in " + elem["id"])
        else:
          rect = child
      else:
        raise Exception("Navbar: Navbar does not support: " + child["id"])

    if title_view is None and not left_bar_buttons and not right_bar_buttons:
      raise Exception("Navbar: Navbar is empty.")

    # sort buttons by x value
    left_bar_buttons = sorted(left_bar_buttons, key=lambda c: c.get('x'))
    right_bar_buttons = sorted(right_bar_buttons, key=lambda c: c.get('x'))

    navbar_items["left-buttons"] = left_bar_buttons
    navbar_items["right-buttons"] = right_bar_buttons
    navbar_items["title"] = title_view

    elem["navbar-items"] = navbar_items
    elem["rect"] = rect

    return super().parse_elem(elem)
