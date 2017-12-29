from . import *

class SliderOptions(BaseLayer):
  """
  Class representing a SliderOptions layer in Sketch
  """
  def parse_elem(self, elem):
    options = []
    rect = None

    for child in elem["children"]:
      if child["type"] == "SliderOption":
        options.append(child)
      elif utils.word_in_str("bound", child["id"]):
        rect = child

    if not options:
      raise Exception("SliderOptions: No options found in " + elem["id"])
    elif rect is None:
      raise Exception("SliderOptions: No bound in " + elem["id"])

    options = sorted(options, key=lambda i: i["x"])
    selected_index = 0
    for index, i in enumerate(options):
      if utils.word_in_str("active", i["id"]):
        selected_index = index
        break

    if options[selected_index]["rect"].get("filter") is None:
      raise Exception("SliderOptions: Selected option missing inner shadow.")

    elem["selected_index"] = selected_index
    elem["options"] = options
    elem["rect"] = rect
    return super().parse_elem(elem)
