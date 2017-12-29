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


    content_cv = content
    content_cv["id"] = "sliderCollectionView"
    content_cv["type"] = "UICollectionView"
    content_cv["separator"] = [0]
    content_cv["cells"] = [{"rect": content["rect"],
                            "rwidth": content["rwidth"],
                            "rheight": content["rheight"],
                            "components": content["components"]}]
    del content_cv["components"]

    print(type(slider_options))
    elem["content_cv"] = content_cv
    elem["slider_options"] = slider_options
    elem["rect"] = rect
    return super().parse_elem(elem)
