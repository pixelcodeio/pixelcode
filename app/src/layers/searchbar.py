from . import *

class SearchBar(BaseLayer):
  """
  Class representing a SearchBar in Sketch
  """
  def parse_elem(self, elem):
    contents = "Search" # default placeholder text to "Search"

    for child in elem["children"]:
      if child["type"] == "UILabel":
        contents = child["textspan"][0]["contents"].decode('utf-8')

    elem["contents"] = contents
    return super().parse_elem(elem)
