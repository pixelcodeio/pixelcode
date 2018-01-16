from . import *

class UIActionSheet(BaseComponent):
  """
  Class representing a UIActionSheet in swift
  """
  def generate_swift(self):
    return self.setup_component()

  def setup_component(self):
    """
    Returns: swift code to setup UIActionSheet.
    """
    if self.info.get("title"):
      if self.info["title"].get("title"):
        title = '"{}"'.format(self.info["title"]["title"].decode('utf-8'))
      else:
        title = "nil"
      if self.info["title"].get("message"):
        message = '"{}"'.format(self.info["title"]["message"].decode('utf-8'))
      else:
        message = "nil"
    else:
      title = "nil"
      message = "nil"
    C = ("let alertController = UIAlertController(title: {}, message: {}, "
         "preferredStyle: .actionSheet)\n").format(title, message)

    actions = self.info["actions"]
    titles = [a["text"]["textspan"][0]["contents"] for a in actions]
    titles = [title.decode('utf-8') for title in titles]
    for index, action in enumerate(actions):
      if utils.word_in_str("destructive", action["id"]):
        style = ".destructive"
      elif utils.word_in_str("cancel", action["id"]):
        style = ".cancel"
      else:
        style = ".default"
      C += self.gen_action(titles[index], style)

    add_actions = [self.add_action(title) for title in titles]
    C += "".join(add_actions)
    C += "self.present(alertController, animated: true, completion: nil)\n"
    return C

  def gen_action(self, title, style):
    """
    Returns (str): swift code to generate a UIAlertAction
    """
    lowercased = title if not title else title[0].lower() + title[1:]
    return ('let {}Action = UIAlertAction(title: "{}", style: {}, handler'
            ': nil)\n').format(lowercased, title, style)

  def add_action(self, title):
    """
    Returns (str): swift code to add action to alertController
    """
    lowercased = title if not title else title[0].lower() + title[1:]
    return ("alertController.addAction({}Action)\n").format(lowercased)
