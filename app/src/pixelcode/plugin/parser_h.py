import pixelcode.plugin.utils as utils

def inherit_from(parent, child, init=False):
  """
  Returns: (dict) child with attributes from parent passed down
  """
  for attr in parent.attrs:
    skip = attr == "id" or (attr == "fill" and (parent["fill"] == "none" or \
                                                parent["fill"][0] != "#"))
    if init:
      skip = (skip
              or (attr == "fill" and (parent["fill"] == "none" or \
                  parent["fill"][0] != "#"))
              or (attr == "stroke" and parent["stroke"] == "none")
              or (attr == "stroke-width" and parent["stroke"] == "none")
              or attr == "fill-rule")
    if not skip and attr not in child.attrs:
      child[attr] = parent[attr]
  return child

def inherit_from_json(child, json):
  """
  Returns: (dict) child with attributes from json passed down
  """
  if "id" in child.attrs:
    for layer in json["layers"]:
      if child["id"] == layer["name"]:
        for key in layer.keys():
          if key not in child.attrs:
            child[key] = layer[key]
        break
  return child

def create_children(elem, json):
  """
  Returns: (dict) elem with children recursively initialized.
  """
  elem = inherit_from_json(elem, json)
  elem = inherit_from(elem.parent, elem)
  num_children = sum(1 for _ in elem.children)
  if num_children == 0:
    elem["children"] = []
    return elem

  children = []
  for child in elem.children:
    if child != "\n" and child.name is not None:
      children.append(parse_fake_group(create_children(child, json)))
  elem["children"] = children
  return elem

def contains(elem1, elem2):
  """
  Returns (str): whether elem2 is inside elem1
  """
  return (elem2["abs_x"] >= elem1["abs_x"] and \
          elem2["abs_x"] <= (elem1["abs_x"] + elem1["width"]) and \
          elem2["abs_y"] >= elem1["abs_y"] and \
          elem2["abs_y"] <= (elem1["abs_y"] + elem1["height"]))

def filter_elements(elem, elements):
  """
  Returns:
    The filtered elements (filtered based on their types and ids) to calculate
    spacing for generating iOS code.
  """
  filtered_elements = []
  ignored_elements = []
  ignore = {"UIActionSheet", "UINavBar", "UITabBar", "SliderView"}
  for e in elements:
    if e['type'] in ignore or \
    (e.get("id") and utils.word_in_str("overlay", e["id"])):
      ignored_elements.append(e)

  for e in elements:
    should_ignore = [contains(i, e) for i in ignored_elements]
    if e not in ignored_elements and not any(should_ignore):
      filtered_elements.append(e)

  return filtered_elements


def calculate_spacing(elem, parsed_elements, is_ios):
  """
  Returns:
    (dict) elem with keys vertical and horizontal added, where
    vertical and horizontal represent the relative spacing between elem
    and parsed_elements
  """
  if is_ios:
    parsed_elements = filter_elements(elem, parsed_elements)

  vertical = {}
  horizontal = {}
  for check in parsed_elements:
    if not vertical:
      check_top = check_spacing(check, elem, "top")
      if check_top[0]:
        vertical = {"direction": "top", "id": check["id"],
                    "distance": check_top[1]}
    if not horizontal:
      check_left = check_spacing(check, elem, "left")
      if check_left[0]:
        horizontal = {"direction": "left", "id": check["id"],
                      "distance": check_left[1]}
    if vertical and horizontal:
      break

  if not vertical:
    vertical = {"direction": "top", "id": "", "distance": elem["y"]}
  if not horizontal:
    horizontal = {"direction": "left", "id": "", "distance": elem["x"]}

  elem["horizontal"] = horizontal
  elem["vertical"] = vertical
  return elem

def convert_coords(parser, elem, parent):
  """
  Returns: (dict) elem with coords set relative to parent height/width
  """
  width = parent["rwidth"]
  height = parent["rheight"]

  # cache pixel widths
  elem["rwidth"] = elem["width"]
  elem["rheight"] = elem["height"]
  # convert units to percentages
  elem["width"] = min(elem["width"]/width, 1.0)
  elem["height"] = min(elem["height"]/height, 1.0)
  elem["horizontal"]["distance"] /= width
  elem["vertical"]["distance"] /= height

  # Adjust height for long components in long artboards
  if parser.is_ios and parser.globals["is_long_artboard"] and \
  elem["height"] == 1.0 and parent["id"] == parser.artboard:
      elem["height"] -= elem["y"]/height

  # generate center
  elem["cx"] = elem["x"]/width + elem["width"]/2
  elem["cy"] = elem["y"]/height + elem["height"]/2
  return elem

def parse_fake_group(elem):
  """
  Handles the case where an elem is a group but none of its children have ids.
  We first make sure that we are in this case (by checking its children),
  then we pick a child to make the main element. Finally, we replace the group
  with this new element, after making sure it inherits from all the other
  elements.
  """
  if elem.name == "g":
    # set-up children and ensure that no children have ids.
    children = []
    for child in [c for c in elem["children"] if c != "\n"]:
      if "id" in child.attrs:
        return elem
      children.append(child)

    # two separate lists for easy checking later
    use_children = []
    main_children = []
    for child in children:
      if child.name == "use":
        use_children.append(child)
      else:
        main_children.append(child)

    if (not main_children) and use_children:
      for ind, child in enumerate(use_children):
        if "xlink:href" in child.attrs and "filter" not in child.attrs:
          if child.attrs["fill"][0] == "u": # url(...): for image fills
            child.name = "image"
          else:
            child.name = "rect"
          use_children.pop(ind)
          main_children = [child]
          break
      if not main_children: # every use tag contains filter
        child = use_children[0]
        child.name = "rect"
        use_children.pop(0)
        main_children = [child]

    # ensure that there is only one main child
    if len(main_children) == 1:
      parent_id = elem["id"]
      for child in use_children:
        elem = inherit_from(child, elem)
      elem = inherit_from(elem, main_children[0])
      elem["id"] = parent_id
    else:
      raise Exception("Unhandled case in parse_fake_group.")
  return elem

def check_spacing(r1, r2, direction):
  """
  Args:
    r1: The rectangle with a smaller bottom-right coordinate sum
    r2: The rectangle we are currently checking
    direction: direction to check; one-of [top, left]

  Returns:
    A tuple (bool, dist) representing whether r2 can have its spacing
    defined in [direction] with respect to r1, where dist is the
    distance between the two rectangles in pixels.
  """
  if "x" not in r1 or "y" not in r1:
    raise Exception("check_spacing: x or y not present in " + r1["id"])
  r1_top = (int(r1["x"]), int(r1["y"])) # top-left
  r1_bottom = (r1_top[0] + int(r1["rwidth"]), r1_top[1] + int(r1["rheight"]))
  r2_top = (int(r2["x"]), int(r2["y"])) # top-left
  r2_bottom = (r2_top[0] + int(r2["width"]), r2_top[1] + int(r2["height"]))

  if r2_top[0] > r1_bottom[0] and r2_top[1] > r1_bottom[1]:
    return False, 0

  if direction == "top":
    if r2_top[1] >= r1_bottom[1]:
      t_btwn = r2_top[0] >= r1_top[0] and r2_top[0] <= r1_bottom[0]
      b_btwn = r2_bottom[0] >= r1_top[0] and r2_bottom[0] <= r1_bottom[0]
      contains = r2_top[0] <= r1_top[0] and r2_bottom[0] >= r1_bottom[0]
      if t_btwn or b_btwn or contains:
        return True, (r2_top[1] - r1_bottom[1])
    return False, 0
  else:
    if r2_top[0] >= r1_bottom[0]:
      t_btwn = r2_top[1] >= r1_top[1] and r2_top[1] <= r1_bottom[1]
      b_btwn = r2_bottom[1] >= r1_top[1] and r2_bottom[1] <= r1_bottom[1]
      contains = r2_top[1] <= r1_top[1] and r2_bottom[1] >= r1_bottom[1]
      if t_btwn or b_btwn or contains:
        return True, (r2_top[0] - r1_bottom[0])
    return False, 0

def adjust_size(parser, elem):
  rect = elem["rect"]
  if rect["rwidth"] != elem["rwidth"] or rect["rheight"] != elem["rheight"]:
    # Adjust width/heights of elem and all of its children
    artboard_w = parser.globals["width"]
    artboard_h = parser.globals["height"]
    parent_w = min(elem["rwidth"] / elem["width"], artboard_w)
    parent_h = min(elem["rheight"] / elem["height"], artboard_h)
    elem["rwidth"] = rect["rwidth"]
    elem["rheight"] = rect["rheight"]
    elem["width"] = elem["rwidth"] / parent_w
    elem["height"] = elem["rheight"] / parent_h
    for child in elem["children"]:
      child["width"] = child["rwidth"] / elem["rwidth"]
      child["height"] = child["rheight"] / elem["rheight"]
  return elem

def add_to_info(key, new_value, info):
  """
  Args:
    key (str): either 'fill' or 'text'
  """
  if new_value is None:
    return info
  if key == 'fill':
    key = 'colors'
    new_value = {'r': int(float(new_value[0])), # convert strings to int
                 'g': int(float(new_value[1])),
                 'b': int(float(new_value[2])),
                 'a': float(new_value[3])}
  else:
    key = 'text-styles'
    letter_spacing = new_value.get('char-spacing')
    line_height = new_value.get('line-spacing')
    tspan_keys = ['fill', 'font-family', 'font-size']
    fill, font, size = utils.get_vals(tspan_keys, new_value['textspan'][0])
    if fill is not None:
      fill = {'r': int(float(fill[0])),
              'g': int(float(fill[1])),
              'b': int(float(fill[2])),
              'a': float(fill[3])}
    new_value = {'font': font,
                 'font_size': size,
                 'letter_spacing': letter_spacing,
                 'line_height': line_height,
                 'color': fill}
  if new_value not in info[key]:
    info[key].append(new_value)
  return info

def extract_to_info(elem, info):
  """
  Returns: extracts style-guide information from elem and adds it to info
  """
  # keys = ['char-spacing', 'fill', 'font-family', 'font-size', 'line-spacing']
  keys = ['fill', 'text']
  fill, text = utils.get_vals(keys, elem)
  info = add_to_info('fill', fill, info)
  info = add_to_info('text', text, info)
  return info

def parse_filter_matrix(matrix):
  """
  Args:
    matrix (str): string representation of a filter matrix.

  Returns (tuple): r,g,b,a values parsed from matrix.
  """
  matrix = matrix.split()
  if len(matrix) != 20:
    raise Exception("Parser_h: Filter matrix has invalid format.")
  r = float(matrix[0])
  g = float(matrix[6])
  b = float(matrix[12])
  a = float(matrix[18])
  return (r, g, b, a)

def move_bounds_to_end(elements):
  """
  Returns (list):
    recursively moves bound to the end of each element's children property
  """
  for elem in elements:
    # Move UIViews to end
    rect_indicies = []
    for index, child in enumerate(elem["children"]):
      if child["type"] == "UIView":
        rect_indicies.append(index)
    for rect_index in sorted(rect_indicies, reverse=True):
      elem["children"] += [elem["children"].pop(rect_index)]
    # Move bounds to end
    bound_indicies = []
    for index, child in enumerate(elem["children"]):
      if utils.word_in_str("bound", child["id"]):
        bound_indicies.append(index)
    for bound_index in sorted(bound_indicies, reverse=True):
      elem["children"] += [elem["children"].pop(bound_index)]
    elem["children"] = move_bounds_to_end(elem["children"])
  return elements
