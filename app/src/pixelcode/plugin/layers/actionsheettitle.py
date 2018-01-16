from . import *

class ActionSheetTitle(BaseLayer):
  """
  Class representing a ActionSheetTitle (part of an ActionSheet) in Sketch
  """
  def parse_elem(self, elem):
    title = None
    message = None

    for child in elem["children"]:
      if child["type"] == "UILabel":
        if utils.word_in_str("title", child["id"]):
            if title:
              raise Exception("ActionSheetTitle: More than one title found.")
            else:
              title = child["textspan"][0]["contents"]
        elif utils.word_in_str("message", child["id"]):
            if message:
              raise Exception("ActionSheetTitle: More than one message found.")
            else:
              message = child["textspan"][0]["contents"]
        else:
          raise Exception("ActionSheetTitle: Labels should either be a " + \
                          "title or a message.")

    if title is None and message is None:
      raise Exception("ActionSheetTitle: Nothing found in: " + elem["id"])                      

    elem["title"] = title
    elem["message"] = message
    return super().parse_elem(elem)
