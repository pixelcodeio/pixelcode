import utils
from layers.base_layer import BaseLayer

class Button(BaseLayer):
  """
  Class representing a Button in Sketch
  """
  def parse_elem(self, elem):
    rect = None
    text = None
    for child in elem["children"]:
      if child.name == "rect":
        rect = child
        if "rx" in rect.attrs:
          elem["border-radius"] = rect["rx"]
        if "fill" in rect.attrs:
          elem["fill"] = rect["fill"]
        if "stroke" in rect.attrs:
          elem["stroke-color"] = utils.convert_hex_to_rgb(rect["stroke"])

          if "stroke-width" in rect:
            elem["stroke-width"] = rect["stroke-width"]
          else:
            elem["stroke-width"] = 1
        else:
          elem["stroke-color"] = None
          elem["stroke-width"] = None

    if "fill" not in elem.attrs:
      elem["fill"] = "none"

    for child in elem["children"]:
      if child.name == "text":
        text = child
        elem["title"] = ""
        for tspan in text.children:
          if tspan != "\n":
            elem["title"] += tspan.contents[0]
        for key in text.attrs:
          if key not in elem.attrs:
            elem[key] = text[key]
        if "fill" in text.attrs:
          elem["title-color"] = utils.convert_hex_to_rgb(text["fill"])
        else:
          elem["title-color"] = utils.convert_hex_to_rgb(elem["fill"])

    if rect is None:
      elem["fill"] = "none"

    if elem["id"] == "testButton":
      print elem["fill"]
    return super(Button, self).parse_elem(elem)
