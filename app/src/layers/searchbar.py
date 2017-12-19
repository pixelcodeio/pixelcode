from . import *

class SearchBar(BaseLayer):
  """
  Class representing a SearchBar in Sketch
  """
  def parse_elem(self, elem):
    contents = "Search" # default placeholder text to "Search"
    search_icon = None
    bookmark_icon = None

    for child in elem["children"]:
      if child["type"] == "UILabel":
        contents = child["textspan"][0]["contents"].decode('utf-8')
      elif child["type"] == "UIImageView":
        center_x = elem['x'] + elem['rwidth']/2.0
        if child['x'] < center_x: # implies that child is a search icon
          if search_icon:
            raise Exception("Searchbar: Only one search icon allowed.")
          else:
            search_icon = child
        else: # implies that child is a bookmark icon
          if bookmark_icon:
            raise Exception("Searchbar: Only one bookmark icon allowed.")
          else:
            bookmark_icon = child

    elem["contents"] = contents
    elem["search-icon"] = search_icon
    elem["bookmark-icon"] = bookmark_icon
    return super().parse_elem(elem)
