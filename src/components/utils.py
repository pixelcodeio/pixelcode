from . import *

def translates_false(elem):
  """
  Returns: The line that sets the translatesAutoResizing property
  of elem to false.
  """
  return '{}.translatesAutoresizingMaskIntoConstraints = false\n'.format(elem)

def set_bg(elem, color, inView=False, opacity=None):
  """
  Args:
    color: (tuple) contains the r, g, b values of the background color
    opacity: (float) between 0 and 1 representing the opacity

  Returns: The line that sets the background color of elem to the
  UIColor with the corresponding r, g, b values.
  """
  o = "1.0" if opacity is None else opacity
  r = color[0]
  g = color[1]
  b = color[2]
  if inView is True:
    return ('backgroundColor = UIColor(red: {}/255.0 , green: '
            '{}/255.0 , blue: {}/255.0 , alpha: {})\n'
           ).format(r, g, b, o)
  # else:
  return ('{}.backgroundColor = UIColor(red: {}/255.0 , green: '
          '{}/255.0 , blue: {}/255.0 , alpha: {})\n'
         ).format(elem, r, g, b, o)

def add_subview(view, elem):
  if view is None:
    return 'addSubview({})\n\n'.format(elem)
  # else:
  return '{}.addSubview({})\n\n'.format(view, elem)

def wh_constraints(elem, width, height, inView=False):
  """
  Returns: The swift code that sets the width and height constraints
  of the elem.
  """
  if inView:
    return ('{}.widthAnchor.constraint(equalToConstant: contentView.frame.width*'
            '{}).isActive = true\n'
            '{}.heightAnchor.constraint(equalToConstant: contentView.frame.'
            'height*{}).isActive = true\n'
           ).format(elem, width, elem, height)
  # else:
  return ('{}.widthAnchor.constraint(equalToConstant: view.frame.width*'
          '{}).isActive = true\n'
          '{}.heightAnchor.constraint(equalToConstant: view.frame.height*'
          '{}).isActive = true\n'
         ).format(elem, width, elem, height)

def position_constraints(elem, horID, horDir, horDist, vertID, vertDir,
                         vertDist, centerX, centerY, inView=False):
  """
  Returns: The swift code to set the centerX and centerY constraints of
  the elem.
  """
  if inView:
    c = ('{}.centerXAnchor.constraint(equalTo: contentView.leftAnchor, '
         'constant: frame.width*{}).isActive = true\n'
         '{}.centerYAnchor.constraint(equalTo: contentView.topAnchor, '
         'constant: frame.height*{}).isActive = true\n'
        ).format(elem, centerX, elem, centerY)
    if horID == '':
      c += ('{}.leftAnchor.constraint(equalTo: contentView.leftAnchor, '
            'constant: frame.width*{}).isActive = true\n'
           ).format(elem, horDist)
    else:
      oppDir = 'left' if horDir == 'right' else 'right'
      c += ('{}.{}Anchor.constraint(equalTo: {}.'
            '{}Anchor, constant: frame.width*{}'
            ').isActive = true\n'
           ).format(elem, horDir, horID, oppDir, horDist)
    if vertID == '':
      c += ('{}.topAnchor.constraint(equalTo: contentView.topAnchor, '
            'constant: frame.height*{}).isActive = true\n\n'
           ).format(elem, vertDist)
    else:
      vertDir = 'top' if vertDir == 'up' else 'bottom'
      oppDir = 'top' if vertDir == 'bottom' else 'bottom'
      c += ('{}.{}Anchor.constraint(equalTo: {}.'
            '{}Anchor, constant: frame.height*{}'
            ').isActive = true\n\n'
           ).format(elem, vertDir, vertID, oppDir, vertDist)
    return c
  # else:
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
    vertDir = 'top' if vertDir == 'up' else 'bottom'
    oppDir = 'top' if vertDir == 'bottom' else 'bottom'
    c += ('{}.{}Anchor.constraint(equalTo: {}.'
          '{}Anchor, constant: view.frame.height*{}'
          ').isActive = true\n\n'
         ).format(elem, vertDir, vertID, oppDir, vertDist)
  return c

def set_border_width(elem, width, inView=False):
  """
  Returns: The swift code to set the border width of elem.
  """
  if inView is True:
    return ("layer.borderWidth = {}\n").format(width)
  # else:
  return ("{}.layer.borderWidth = {}\n").format(elem, width)

def set_border_color(elem, color, opacity=None, inView=False):
  """
  Returns: The swift code to set the border color of elem.
  """
  o = "1.0" if opacity is None else opacity
  r = color[0]
  g = color[1]
  b = color[2]
  if inView is True:
    return ("layer.borderColor = UIColor(red: {}/255.0, green: {}/255.0, "
            "blue: {}/255.0, alpha: {}).cgColor\n"
           ).format(r, g, b, o)
  # else:
  return ("{}.layer.borderColor = UIColor(red: {}/255.0, green: {}/255.0, "
          "blue: {}/255.0, alpha: {}).cgColor\n"
         ).format(elem, r, g, b, o)

def set_corner_radius(elem, radius, inView=False):
  """
  Returns: The swift code to set the corner radius of elem.
  """
  if inView is True:
    return ("layer.cornerRadius = {}\n").format(radius)
  # else:
  return ("{}.layer.cornerRadius = {}\n").format(elem, radius)
