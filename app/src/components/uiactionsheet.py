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
    C = ("let alertController = UIAlertController(title: nil, message: nil, "
         "preferredStyle: .actionSheet)\n")

    actions = self.info["actions"]
    actions = [action.decode('utf-8') for action in actions]
    for i, action in enumerate(actions):
      if i == (len(actions) - 1):
        style = ".cancel"
      else:
        style = ".default"
      C += self.gen_action(action, style)

    add_actions = [self.add_action(action) for action in actions]
    C += "".join(add_actions)
    C += "self.present(alertController, animated: true, completion: nil)\n"
    return C

  def gen_action(self, action, style):
    """
    Returns (str): swift code to generate a UIAlertAction
    """
    lowercased = action if not action else action[0].lower() + action[1:]
    return ('let {}Action = UIAlertAction(title: "{}", style: {}, handler'
            ': nil)\n').format(lowercased, action, style)

  def add_action(self, action):
    """
    Returns (str): swift code to add action to alertController
    """
    lowercased = action if not action else action[0].lower() + action[1:]
    return ("alertController.addAction({}Action)\n").format(lowercased)
