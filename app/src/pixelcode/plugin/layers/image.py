from . import *

class Image(BaseLayer):
  """
  Class representing an Image layer in Sketch
  """
  def parse_elem(self, elem):
    img_fill = None

    if elem.attrs.get("fill"):
      img_fill = elem.attrs["fill"]

    elem["img_fill"] = img_fill
    if ":" in elem["originalName"]:
      id_index = elem["id"].find(":") # rename id
      elem["id"] = elem["id"][:id_index]
      index = elem["originalName"].find(":") # get name of image
      img_name = elem["originalName"][:index]
    else:
      img_name = elem["originalName"]
    elem["path"] = img_name + ".png" # TODO: change this later
    return super().parse_elem(elem)
