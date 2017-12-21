import utils

def inherit_from(parent, child, init=False):
  """
  Returns: (dict) child with attributes from parent passed down
  """
  for attr in parent.attrs:
    skip = attr == "id"
    if init:
      skip = (skip
              or (attr == "fill" and parent["fill"] == "none")
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
  filtered_elements = []
  ignored_elements = []
  ignore = {"UIActionSheet", "UINavBar", "UITabBar"}
  for e in elements:
    if e['type'] in ignore or utils.word_in_str("overlay", e["id"]):
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
    #print("filtered")
    parsed_elements = filter_elements(elem, parsed_elements)
  # for p in parsed_elements:
  #   print(p["id"])

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

def convert_coords(elem, parent):
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
        if "xlink:href" in child.attrs:
          child.name = "rect"
          use_children.pop(ind)
          main_children = [child]
          break

    # ensure that there is only one main child
    if len(main_children) == 1 and use_children:
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
