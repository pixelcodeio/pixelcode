def translates_false(elem):
  """
  Returns: The line that sets the translatesAutoResizing property
  of elem to false.
  """
  return '{}.translatesAutoresizingMaskIntoConstraints = false\n'.format(elem)

def set_bg(elem, r, g, b):
  """
  Returns: The line that sets the background color of elem to the
  UIColor with the corresponding r, g, b values.
  """
  return ('{}.backgroundColor = UIColor(red: {}/255.0 , green: '
          '{}/255.0 , blue: {}/255.0 , alpha: 1.0)\n'
         ).format(elem, r, g, b)

def add_subview(view, elem):
  return '{}.addSubview({})\n\n'.format(view, elem)

def wh_constraints(elem, width, height):
  """
  Returns: The swift code that sets the width and height constraints
  of the elem.
  """
  return ('{}.widthAnchor.constraint(equalToConstant: view.frame.width*'
          '{}).isActive = true\n'
          '{}.heightAnchor.constraint(equalToConstant: view.frame.height*'
          '{}).isActive = true\n'
         ).format(elem, width, elem, height)

def position_constraints(elem, horID, horDir, horDist, vertID, vertDir,
                         vertDist, centerX, centerY):
  """
  Returns: The swift code to set the centerX and centerY constraints of
  the elem.
  """
  c = ('{}.centerXAnchor.constraint(equalTo: view.leftAnchor, '
       'constant: view.frame.width*{}).isActive = true\n'
       '{}.centerYAnchor.constraint(equalTo: view.topAnchor, '
       'constant: view.frame.height*{}).isActive = true\n'
      ).format(elem, centerX, elem, centerY)
  if horID == '':
    c += ('{}.leftAnchor.constraint(equalTo: view.leftAnchor, '
          'constant: view.frame.width*{}).isActive = true\n'
         ).format(elem, horDist)
  else:
    oppDir = 'left' if horDir == 'right' else 'right'
    c += ('{}.{}Anchor.constraint(equalTo: {}.'
          '{}Anchor, constant: view.frame.width*{}'
          ').isActive = true\n'
         ).format(elem, horDir, horID, oppDir, horDist)
  if vertID == '':
    c += ('{}.topAnchor.constraint(equalTo: view.topAnchor, '
          'constant: view.frame.height*{}).isActive = true\n\n'
         ).format(elem, vertDist)
  else:
    oppDir = 'top' if horDir == 'bottom' else 'bottom'
    c += ('{}.{}Anchor.constraint(equalTo: {}.'
          '{}Anchor, constant: view.frame.height*{}'
          ').isActive = true\n\n'
         ).format(elem, horDir, horID, oppDir, vertDist)
  return c

def set_border_width(elem, width):
  """
  Returns: The swift code to set the border width of elem.
  """
  return ("{}.layer.borderWidth = {}\n").format(elem, width)

def set_border_color(elem, color):
  """
  Returns: The swift code to set the border color of elem.
  """
  r = color[0]
  g = color[1]
  b = color[2]
  return ("{}.layer.borderColor = UIColor(red: {}/255.0, green: {}/255.0, "
          "blue: {}/255.0, alpha: 1.0).cgColor\n"
         ).format(elem, r, g, b)

def set_corner_radius(elem, radius):
  """
  Returns: The swift code to set the corner radius of elem.
  """
  return ("{}.layer.cornerRadius = {}\n").format(elem, radius)
