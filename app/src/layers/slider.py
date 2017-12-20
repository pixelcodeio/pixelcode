from . import *

class Slider(BaseLayer):
  """
  Class representing a Slider in Sketch
  """
  def parse_elem(self, elem):
    progress_fill = None

    for child in elem["children"]:
      if utils.word_in_str("progress", child["id"]):
        if progress_fill:
          raise Exception("Slider: Only one progress bar allowed.")
        else:
          progress_fill = child["fill"]

    elem["progress_fill"] = progress_fill
    return super().parse_elem(elem)
