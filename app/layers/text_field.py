from . import *

class TextField(BaseLayer):
  """
  Class representing an TextField layer in Sketch
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

    if text is not None and rect is not None:
      elem["left-inset"] = float(text["x"]) - float(rect["x"])
    return super(TextField, self).parse_elem(elem)
