from . import *

class ActionSheet(BaseLayer):
  """
  Class representing a ActionSheet in Sketch
  """
  def parse_elem(self, elem):
    actions = []

    for child in elem["children"]:
      if child["type"] == "UIButton":
        if child.get("text") and child["text"]["textspan"]:
          actions.append(child)
        else:
          raise Exception("ActionSheet: Button does not contain text.")

    actions = sorted(actions, key=lambda a: a['y'])
    elem["actions"] = actions
    return super().parse_elem(elem)
