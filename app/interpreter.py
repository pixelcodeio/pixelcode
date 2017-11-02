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
    viewController = glob['artboard'] + 'ViewController'
    header = 'import UIKit\nclass ' + viewController + ': UIViewController {\n'
    header += '\noverride func viewDidLoad() {\n\n}\n}'
    return header

  def translates_false(self, elem):
    """
    Returns: The line that sets the translatesAutoResizing property
    of elem to false.
    """
    return elem + '.translatesAutoresizingMaskIntoConstraints = false\n'

  def set_bg(self, elem, r, g, b):
    """
    Returns: The line that sets the background color of elem to the
    UIColor with the corresponding r, g, b values.
    """
    red = str(r)
    green = str(g)
    blue = str(b)
    bg = elem + '.backgroundColor = UIColor(red: ' + red + '/255.0 , green: '
    bg += green + '/255.0 , blue: ' + blue + '/255.0 , alpha: 1.0)\n'
    return bg

  def add_subview(self, view, elem):
    return view + '.addSubview(' + elem + ')\n\n'

  def wh_constraints(self, elem, width, height):
    """
    Returns: The swift code that sets the width and height constraints
    of the elem.
    """
    w = str(width)
    h = str(height)
    c = elem + '.widthAnchor.constraint(equalToConstant: view.frame.width*'
    c += w + ').isActive = true\n'
    c += elem + '.heightAnchor.constraint(equalToConstant: view.frame.height*'
    c += h + ').isActive = true\n'
    return c

  def position_constraints(self, elem, horID, horDir, horDist, vertID, vertDir,
      vertDist, centerX, centerY):
    """
    Returns: The swift code to set the centerX and centerY constraints of
    the elem.
    """
    x = str(centerX)
    y = str(centerY)
    hDist = str(horDist)
    vDist = str(vertDist)
    c = elem + '.centerXAnchor.constraint(equalTo: view.leftAnchor, '
    c += 'constant: view.frame.width*' + x + ').isActive = true\n'
    c += elem + '.centerYAnchor.constraint(equalTo: view.topAnchor, '
    c += 'constant: view.frame.height*' + y + ').isActive = true\n'
    if horID == '':
      c += elem + '.leftAnchor.constraint(equalTo: view.leftAnchor, '
      c += 'constant: view.frame.width*' + hDist + ').isActive = true\n'
    else:
      oppDir = 'left' if horDir == 'right' else 'right'
      c += elem + '.' + horDir + 'Anchor.constraint(equalTo: ' + horID + '.'
      c += oppDir + 'Anchor, constant: view.frame.width*' + hDist
      c += ').isActive = true\n'
    if vertID == '':
      c += elem + '.topAnchor.constraint(equalTo: view.topAnchor, '
      c += 'constant: view.frame.height*' + vDist + ').isActive = true\n'
    else:
      oppDir = 'top' if horDir == 'bottom' else 'bottom'
      c += elem + '.' + horDir + 'Anchor.constraint(equalTo: ' + horID + '.'
      c += oppDir + 'Anchor, constant: view.frame.height*' + vDist
      c += ').isActive = true\n'
    return c
