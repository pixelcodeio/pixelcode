from . import *

class SliderOption(BaseLayer):
  """
  Class representing an SliderOption layer in Sketch
  """
  def parse_elem(self, elem):
    text = img = rect = None

    for child in elem["children"]:
      if child["type"] == "UILabel":
        if child["textspan"]:
          text = child
        else:
          raise Exception("SliderOption: No text in SliderOption: " + elem["id"])
      elif child["type"] == "UIImageView":
        img = child
      elif utils.word_in_str("bound", child["id"]):
        rect = child

    if text is None and img is None:
      raise Exception("SliderOption: No content in SliderOption: " + elem["id"])
    elif rect is None:
      raise Exception("SliderOption: No bound in SliderOption: " + elem["id"])

    elem["img"] = img
    elem["rect"] = rect
    elem["text"] = text
    return super().parse_elem(elem)
