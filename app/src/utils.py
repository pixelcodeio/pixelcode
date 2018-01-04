def convert_hex_to_rgb(hex_string):
  """
  Returns: (tuple) [hex_string] converted to a rgb tuple.
  """
  h = hex_string.lstrip('#')
  return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def get_vals(keys, d):
  """
  Returns: list of values corresponding to [keys] from [d]
  """
  return [d.get(k) for k in keys]

def uppercase(string):
  """
  Returns (str):
    string with the first letter capitalized. if string is the empty string, the
    empty string is returned.
  """
  return string if not string else string[0].upper() + string[1:]

def word_in_str(word, string):
  """
  Returns (bool): whether string contains word or capitalized version of word
  """
  return word in string or uppercase(word) in string

def create_uicolor(color):
  """
  Returns: The UIColor of [color].
  """
  r, g, b, o = color
  return ("UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha"
          ": {})").format(r, g, b, o)

def set_bg(id_, color):
  """
  Args:
    color: (tuple) the r, g, b values of the background color

  Returns: (str) swift code that sets the background color of id_ to [color].
  """
  color = create_uicolor(color)
  if id_ is not None:
    if word_in_str('navBar', id_):
      return ('self.navigationController?.navigationBar.barTintColor = {}\n\n'
             ).format(color)
    return ('{}.backgroundColor = {}\n').format(id_, color)
  return ('backgroundColor = {}\n').format(color)

def add_subview(view, id_, type_):
  if view is None:
    if type_ == "UIImageView":
      return ("addSubview({0})\n"
              "sendSubview(toBack: {0})\n\n").format(id_)
    return "addSubview({})\n\n".format(id_)
  if type_ == "UIImageView":
    return ("{0}.addSubview({1})\n"
            "{0}.sendSubview(toBack: {1})\n\n").format(view, id_)
  return ("{0}.addSubview({1})\n\n").format(view, id_)


def set_border_width(id_, width):
  """
  Returns: (str) swift code to set the border width of id_.
  """
  if id_ is not None:
    return ("{}.layer.borderWidth = {}\n").format(id_, width)
  return ("layer.borderWidth = {}\n").format(width)

def set_border_color(id_, color):
  """
  Returns: (str) swift code to set the border color of id_.
  """
  if id_ is not None:
    return ("{}.layer.borderColor = {}.cgColor\n"
           ).format(id_, create_uicolor(color))
  return ("layer.borderColor = {}.cgColor\n").format(create_uicolor(color))

def set_corner_radius(id_, radius):
  """
  Returns: (str) swift code to set the corner radius of id_.
  """
  if id_ is not None:
    return ("{}.layer.cornerRadius = {}\n").format(id_, radius)
  return ("layer.cornerRadius = {}\n").format(radius)

def add_shadow(id_, type_, filter_):
  """
  Returns (str): swift code to add shadow to id_.
  """
  print(id_)
  print(type_)
  print(filter_)
  keys = ["fill", "radius", "dx", "dy", "d_size", "is_outer"]
  fill, radius, dx, dy, d_size, is_outer = get_vals(keys, filter_)
  C = ("{0}.layer.shadowColor = {1}.cgColor\n"
       "{0}.layer.shadowOpacity = 1\n"
       "{0}.layer.shadowOffset = CGSize(width: {2}, height: {3})\n"
       "{0}.layer.shadowRadius = {4}\n"
      ).format(id_, create_uicolor(fill), dx, dy, radius)

  if is_outer and d_size != 0:
    C += ("{0}.layer.shadowPath = UIBezierPath(rect: {0}.bounds.insetBy(dx: -"
          "{1}, dy: -{1})).cgPath\n").format(id_, d_size)

  if not is_outer:
    C = C.replace("{}.layer".format(id_), "innerShadowLayer")
    C = ("let innerShadowLayer = CALayer()\n"
         "innerShadowLayer.frame = {}.bounds\n"
         "innerShadowLayer.masksToBounds = true\n{}").format(id_, C)
    if d_size != 0:
      C += ("let path = UIBezierPath(rect: innerShadowLayer.bounds.insetBy(dx: "
            "{0}, dy: {0}))\nlet innerPart = UIBezierPath(rect: innerShadow"
            "Layer.bounds).reversing()\npath.append(innerPart)\n"
            "innerShadowLayer.shadowPath = path.cgPath\n").format(d_size/2.0)
    C += ("{}.layer.addSublayer(innerShadowLayer)\n").format(id_)

  if id_ is None:
    C = C.replace("None.", "")
  if type_ == "UINavBar":
    C = C.replace(id_, "navigationController?.navigationBar")
    C += "navigationController?.navigationBar.layer.masksToBounds = false\n"
  return C

def setup_rect(cid, type_, rect, header=False, cell=False):
  """
  Args:
    cid: (str) id of component
    rect: (dict) see generate_component for more information

  Returns: (str) swift code to apply all the properties from rect.
  """
  keys = ["fill", "border-radius", "stroke-color", "stroke-width", "filter"]
  fill, border_r, str_c, str_w, filter_ = get_vals(keys, rect)

  C = ""
  if word_in_str("navBar", cid): # only set background color for UINavBar
    str_c = None
    str_w = None
    border_r = None
  if cell or header:
    cid = None

  if fill is not None:
    if header:
      C += set_bg('backgroundView?', fill)
    elif cid is not None and word_in_str('tabBar', cid):
      C += set_bg('tabBar', fill)
    elif cid is not None and not word_in_str("switch", cid):
      C += ""
    else:
      C += set_bg(cid, fill)
  else:
    C += set_bg(cid, [0, 0, 0, 0]) # transparent color
  if str_c is not None:
    C += set_border_color(cid, str_c)
  if str_w is not None:
    C += set_border_width(cid, str_w)
  if border_r is not None:
    C += set_corner_radius(cid, border_r)
  if filter_ is not None:
    C += add_shadow(cid, type_, filter_)

  return C

def req_init():
  """
  Returns: (str) swift code for a required function for custom views.
  """
  return ("required init?(coder aDecoder: NSCoder) {\n"
          'fatalError("init(coder:) has not been implemented")\n}')

def index_of(str_, key):
  """
  Returns: Maximum of indices of key and capitalized key in str
  """
  return max(str_.find(key), str_.find(uppercase(key)))

def ins_after_key(s, k, ins):
  """
  Args:
    s: (str) the whole string phrase.
    k: (str) the substring to search for inside str.
    ins: (str) the string to insert right after key in str.

  Returns:
    Given a str, insert ins right after key, returning the new string.
    If key is not a substring of str, the empty string is returned.
  """
  i = s.find(k)
  if i == -1:
    raise Exception("Key not found in s")
  end_i = i + len(k)
  return s[:end_i] + ins + s[end_i:]

def set_frame(component):
  """
  Returns (str): swift code to set frame of the component
  """
  keys = ['id', 'x', 'y', 'rwidth', 'rheight']
  id_, x, y, w, h = get_vals(keys, component)
  return ("{}.frame = CGRect(x: {}, y: {}, width: {}, height: {})\n"
         ).format(id_, x, y, w, h)

def str_before_key(string, key):
  """
  Returns: The part of [string] that appears before [key].
  """
  index = string.index(key)
  if index == -1:
    return ""
  return string[0:index]

def create_font(font, size):
  """
  Returns: UIFont generated using font and size.
  """
  return ("UIFont(name: \"{}\", size: {})").format(font, size)
