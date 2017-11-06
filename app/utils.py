def check_spacing(r1, r2, direction): # pylint: disable=R0911
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
  Returns: [hex_string] converted to a rgb tuple.
  """
  h = hex_string.lstrip('#')
  return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def init_optional_params(elem, params):
  """
  Returns: elem with params initialized to None, except for fill
  """
  for param in params:
    if param == "fill":
      if "fill" in elem.attrs and elem["fill"] != "none":
        elem["fill"] = convert_hex_to_rgb(elem["fill"])
      else:
        elem["fill"] = None
    elif param == "font-family":
      if "font-family" in elem.attrs:
        elem["font-family"] = elem["font-family"].split(",")[0]
      else:
        elem["font-family"] = None
    else:
      if param not in elem.attrs:
        elem[param] = None
  return elem
