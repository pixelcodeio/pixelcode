def check_spacing(r1, r2, direction):
  """
  Args:
    r1: The rectangle with a smaller bottom-right coordinate sum
    r2: The rectangle we are currently checking
    direction: direction to check; one-of [up, left]

  Returns:
    A tuple (bool, dist) representing whether r2 can have its spacing
    defined in [direction] with respect to r1, where dist is the
    distance between the two rectangles in pixels.
  """
  r1_top = (int(r1["x"]), int(r1["y"])) # top-left
  r1_bottom = (r1_top[0] + int(r1["width"]), r1_top[1] + int(r1["height"]))
  r2_top = (int(r2["x"]), int(r2["y"])) # top-left
  r2_bottom = (r2_top[0] + int(r2["width"]), r2_top[1] + int(r2["height"]))

  if r2_top[0] > r1_bottom[0] and r2_top[1] > r1_bottom[1]:
    return False, 0

  if direction == "up":
    if r2_top[1] >= r1_bottom[1]:
      if r2_top[0] >= r1_top[0] and r2_top[0] <= r1_bottom[0]:
        return True, (r2_top[1] - r1_bottom[1])
      else:
        if r2_bottom[0] >= r1_top[0] and r2_bottom[0] <= r1_bottom[0]:
          return True, (r2_top[1] - r1_bottom[1])
    return False, 0
  else:
    if r2_top[0] >= r1_bottom[0]:
      if r2_top[1] >= r1_top[1] and r2_top[1] <= r1_bottom[1]:
        return True, (r2_top[0] - r1_bottom[0])
      else:
        if r2_bottom[1] >= r1_top[1] and r2_bottom[1] <= r1_bottom[1]:
          return True, (r2_top[0] - r1_bottom[0])
    return False, 0

def convert_hex_to_rgb(hex_string):
  """
  Returns [hex_string] converted to a rgb tuple.
  """
  h = hex_string.lstrip('#')
  return tuple(int(h[i:i+2], 16) for i in (0, 2 ,4))

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
