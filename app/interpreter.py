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
    return ('import UIKit\nclass {}: UIViewController {\n'
            '\noverride func viewDidLoad() {\n\n}\n}'
           ).format(viewController)


  def generate_component(self):
    pass
