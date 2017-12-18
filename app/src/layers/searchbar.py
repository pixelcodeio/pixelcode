from . import *

class SearchBar(BaseLayer):
  """
  Class representing a SearchBar in Sketch
  """
  def parse_elem(self, elem):
    contents = "Search" # default placeholder text to "Search"
    search_button = None
    bookmark_button = None

    for child in elem["children"]:
      if child["type"] == "UILabel":
        contents = child["textspan"][0]["contents"].decode('utf-8')
      elif child["type"] == "UIButton":
        center_x = elem['x'] + elem['rwidth']/2.0
        if child['x'] < center_x:
          if search_button:
            raise Exception("Searchbar: Only one search button allowed.")
          else:
            search_button = child
        else:
          if bookmark_button:
            raise Exception("Searchbar: Only one bookmark button allowed.")
          else:
            bookmark_button = child

    elem["contents"] = contents
    elem["search-button"] = search_button
    elem["bookmark-button"] = bookmark_button
    return super().parse_elem(elem)
