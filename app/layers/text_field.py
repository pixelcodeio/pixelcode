import utils
from layers.base_layer import BaseLayer

class TextField(BaseLayer):
  """
  Class representing an TextField layer in Sketch
  """
  def parse_elem(self, elem):
    rect = self.inherit_from_json(elem.rect)
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

    text = self.inherit_from_json(elem.find('text'))
    elem["title"] = ""
    for child in text.children:
      if child != "\n":
        elem["title"] += child.contents[0]
    for key in text.attrs:
      if key not in elem.attrs:
        elem[key] = text[key]
    if "fill" in text.attrs:
      elem["title-color"] = utils.convert_hex_to_rgb(text["fill"])
    else:
      elem["title-color"] = utils.convert_hex_to_rgb(elem["fill"])

    elem["left-inset"] = float(text["x"]) - float(rect["x"])
    return super(TextField, self).parse_elem(elem)
