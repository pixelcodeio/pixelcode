from . import *

class ActionSheet(BaseLayer):
  """
  Class representing a ActionSheet in Sketch
  """
  def parse_elem(self, elem):
    actions = []
    title = None # Refers to ActionSheetTitle

    for child in elem["children"]:
      if child["type"] == "UIButton":
        if child.get("text") and child["text"]["textspan"]:
          actions.append(child)
        else:
          raise Exception("ActionSheet: Button does not contain text.")
      elif child["type"] == "ActionSheetTitle":
        if title:
          raise Exception("ActionSheet: More than one title in: " + elem["id"])
        else:
          title = child

    actions = sorted(actions, key=lambda a: a['y'])
    elem["actions"] = actions
    elem["title"] = title
    return super().parse_elem(elem)
