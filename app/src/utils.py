from components.uibutton import UIButton
from components.uiimageview import UIImageView
from components.uilabel import UILabel
from components.uitableview import UITableView
from components.uitextfieldview import UITextFieldView
from components.uiview import UIView


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

def create_uicolor(color):
  """
  Returns: The UIColor of [color].
  """
  r, g, b, o = color
  return ("UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha"
          ": {})").format(r, g, b, o)

def set_bg(id_, color, in_v=False):
  """
  Args:
    color: (tuple) the r, g, b values of the background color

  Returns: (str) swift code that sets the background color of id_ to [color].
  """
  if id_ is not None:
    return ('{}.backgroundColor = {}\n').format(id_, create_uicolor(color))
  elif in_v:
    return ('backgroundColor = {}\n').format(create_uicolor(color))
  else:
    raise Exception("utils: set_bg has invalid args")

def add_subview(view, id_):
  if view is None:
    return 'addSubview({})\n\n'.format(id_)
  return '{}.addSubview({})\n\n'.format(view, id_)

def set_border_width(id_, width, in_v=False):
  """
  Returns: (str) swift code to set the border width of id_.
  """
  if in_v:
    return ("layer.borderWidth = {}\n").format(width)
  return ("{}.layer.borderWidth = {}\n").format(id_, width)

def set_border_color(id_, color, in_v=False):
  """
  Returns: (str) swift code to set the border color of id_.
  """
  if in_v:
    return ("layer.borderColor = {}.cgColor\n"
           ).format(create_uicolor(color))
  return ("{}.layer.borderColor = {}.cgColor\n"
         ).format(id_, create_uicolor(color))

def set_corner_radius(id_, radius, in_v=False):
  """
  Returns: (str) swift code to set the corner radius of id_.
  """
  if id_ is not None:
    return ("{}.layer.cornerRadius = {}\n").format(id_, radius)
  elif in_v:
    return ("layer.cornerRadius = {}\n").format(radius)
  else:
    raise Exception("utils: set_corner_radius has invalid args")

def setup_rect(cid, rect, in_v, tv_header=False, tv_cell=False):
  """
  Args:
    cid: (int) id of component
    rect: (dict) see generate_component for more information

  Returns: (str) swift code to apply all the properties from rect.
  """
  keys = ["fill", "border-radius", "stroke-color", "stroke-width"]
  fill, border_r, str_c, str_w = get_vals(keys, rect)

  c = ""
  if fill is not None:
    if tv_header:
      c += set_bg('contentView', fill)
    elif tv_cell:
      c += set_bg(None, fill, in_v=in_v)
    else:
      c += set_bg(cid, fill, in_v)
  if str_c is not None:
    c += set_border_color(cid, str_c, in_v)
  if str_w is not None:
    c += set_border_width(cid, str_w, in_v)
  if border_r is not None:
    c += set_corner_radius(cid, border_r, in_v)

  return c

def required_init():
  """
  Returns: (str) swift code for a required function for custom views.
  """
  return ("required init?(coder aDecoder: NSCoder) {\n"
          'fatalError("init(coder:) has not been implemented")\n}')

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

def create_component(type_, id_, info, env):
  """
  Args:
    type_ (str): the component to be created
    id_ (str): the name of the component
    info (dict): information on component
    env (dict): env for component. Possible keys are
                [set_prop, in_view, in_cell, in_header]

  Returns: (obj) An instance of the component to be created
  """
  # init keys
  for key in ["set_prop", "in_view", "in_cell", "in_header"]:
    if key not in env:
      env[key] = False
  if type_ == 'UITextField' or type_ == 'UITextView':
    type_ = 'UITextFieldView'
  # using eval for clean code
  return eval(type_ + "(id_, info, env)") # pylint: disable=W0123
