class Interpreter:
  """
  Takes output from Parser one at a time and generates swift file
  """
  def __init__(self):
    pass

  def generate_header(self, glob):
    """
    TODO: Fill in arguments necessary to generate any headers
    """
    viewController = '{}ViewController'.format(glob['artboard'])
    header = 'import UIKit\nclass {}: UIViewController {\n'.format(viewController)
    header += '\noverride func viewDidLoad() {\n\n}\n}'
    return header

  def generate_component(self):
    pass
