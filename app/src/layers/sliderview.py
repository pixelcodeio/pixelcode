from . import *

class SliderView(BaseLayer):
  """
  Class representing an SliderView layer in Sketch
  """
  def parse_elem(self, elem):
    slider_options = None
    content = None
    rect = None

    for child in elem["children"]:
      if child["type"] == "SliderOptions":
        slider_options = child
      elif child["type"] == "SliderContent":
        content = child
      elif utils.word_in_str("bound", child["id"]):
        rect = child

    if slider_options is None:
      raise Exception("SliderView: No options in SliderView: " + elem["id"])
    elif rect is None:
      raise Exception("SliderView: No bound in SliderView: " + elem["id"])
    elif content is None:
      raise Exception("SliderView: No content in SliderView: " + elem["id"])

    slider_options["vertical"] = elem["vertical"]
    slider_options["horizontal"] = elem["horizontal"]

    content["id"] = elem["id"] + "CollectionView"
    content["type"] = "UICollectionView"
    content["separator"] = [0]
    content["cells"] = [{"rect": content["rect"],
                         "width": content["width"],
                         "height": content["height"],
                         "components": content["components"]}]
    del content["components"]

    elem["content"] = content
    elem["slider_options"] = slider_options
    elem["rect"] = rect
    return super().parse_elem(elem)
