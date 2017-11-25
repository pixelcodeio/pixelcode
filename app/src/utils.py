from components.uibutton import UIButton
from components.uiimageview import UIImageView
from components.uilabel import UILabel
from components.uitableview import UITableView
from components.uitextfield import UITextField
from components.uitextview import UITextView
from components.uiview import UIView

def convert_hex_to_rgb(hex_string):
  """
  Returns: [hex_string] converted to a rgb tuple.
  """
  h = hex_string.lstrip('#')
  return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def translates_false(elem):
  """
  Returns: The line that sets the translatesAutoResizing property
  of elem to false.
  """
  return '{}.translatesAutoresizingMaskIntoConstraints = false\n'.format(elem)

def create_uicolor(color):
  """
  Returns: The UIColor of color.
  """
  r, g, b, o = color
  return ("UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha"
          ": {})"
         ).format(r, g, b, o)

def set_bg(elem, color, in_v=False):
  """
  Args:
    color: (tuple) contains the r, g, b values of the background color

  Returns: The line that sets the background color of elem to the
  UIColor with the corresponding r, g, b values.
  """
  if in_v:
    return ('backgroundColor = {}\n'
           ).format(create_uicolor(color))
  return ('{}.backgroundColor = {}\n'
         ).format(elem, create_uicolor(color))

def add_subview(view, elem):
  if view is None:
    return 'addSubview({})\n\n'.format(elem)
  return '{}.addSubview({})\n\n'.format(view, elem)

def make_snp_constraints(elem, horID, horDir, horDist, vertID, vertDir,
                         vertDist, width, height, in_v=False):
  """
  Returns: The swift code to set width/height and position constraints using
  the SnapKit library.
  """
  if in_v:
    c = ("{}.snp.updateConstraints {{ make in\n"
         "make.size.equalTo(CGSize(width: frame.width*{}, height: "
         "frame.height*{}))\n"
        ).format(elem, width, height)
    if not horID:
      c += ('make.left.equalToSuperview().offset(frame.width*{})\n'
           ).format(horDist)
    else:
      oppDir = 'left' if horDir == 'right' else 'right'
      c += ('make.{}.equalTo({}.snp.{}).offset(frame.width*{})\n'
           ).format(horDir, horID, oppDir, horDist)
    if not vertID:
      c += ('make.top.equalToSuperview().offset(frame.height*{})\n'
           ).format(vertDist)
    else:
      vertDir = 'top' if vertDir == 'up' else 'bottom'
      oppDir = 'top' if vertDir == 'bottom' else 'bottom'
      c += ('make.{}.equalTo({}.snp.{}).offset(frame.height*{})\n'
           ).format(vertDir, vertID, oppDir, vertDist)
    c += "}\n\n"
    return c

  c = ("{}.snp.makeConstraints {{ make in\n"
       "make.size.equalTo(CGSize(width: view.frame.width*{}, height: "
       "view.frame.height*{}))\n"
      ).format(elem, width, height)
  if not horID:
    c += ('make.left.equalToSuperview().offset(view.frame.width*{})\n'
         ).format(horDist)
  else:
    oppDir = 'left' if horDir == 'right' else 'right'
    c += ('make.{}.equalTo({}.snp.{}).offset(view.frame.width*{})\n'
         ).format(horDir, horID, oppDir, horDist)
  if not vertID:
    c += ('make.top.equalToSuperview().offset(view.frame.height*{})\n'
         ).format(vertDist)
  else:
    vertDir = 'top' if vertDir == 'up' else 'bottom'
    oppDir = 'top' if vertDir == 'bottom' else 'bottom'
    c += ('make.{}.equalTo({}.snp.{}).offset(view.frame.height*{})\n'
         ).format(vertDir, vertID, oppDir, vertDist)
  c += "}\n\n"
  return c

def set_border_width(elem, width, in_v=False):
  """
  Returns: The swift code to set the border width of elem.
  """
  if in_v:
    return ("layer.borderWidth = {}\n").format(width)
  return ("{}.layer.borderWidth = {}\n").format(elem, width)

def set_border_color(elem, color, in_v=False):
  """
  Returns: The swift code to set the border color of elem.
  """
  if in_v:
    return ("layer.borderColor = {}.cgColor\n"
           ).format(create_uicolor(color))
  return ("{}.layer.borderColor = {}.cgColor\n"
         ).format(elem, create_uicolor(color))

def set_corner_radius(elem, radius, in_v=False):
  """
  Returns: The swift code to set the corner radius of elem.
  """
  if in_v:
    return ("layer.cornerRadius = {}\n").format(radius)
  return ("{}.layer.cornerRadius = {}\n").format(elem, radius)

def setup_rect(cid, rect, in_v=False, tv_header=False):
  """
  Args:
    cid: (int) id of component
    rect: (dict) see generate_component for more information

  Returns: The swift code to apply all the properties from rect.
  """
  fill = rect.get('fill')
  border_r = rect.get('border-radius')
  str_c = rect.get('stroke-color')
  str_w = rect.get('stroke-width')

  c = ""
  if fill is not None:
    if tv_header:
      c += set_bg('contentView', fill, in_v=False)
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
  Returns: The swift code for the required init?(coder:) function for custom
  views.
  """
  return ("required init?(coder aDecoder: NSCoder) {\n"
          'fatalError("init(coder:) has not been implemented")\n}')

def ins_after_key(s, k, ins):
  """
  Args:
    s: (str) the whole string phrase.
    k: (str) the substring to search for inside str.
    ins: (str) the string to insert right after key in str.

  Returns: Given a str, insert ins right after key, returning the new string.
           If key is not a substring of str, the empty string is returned.
  """
  i = s.find(k)
  if i == -1:
    raise Exception("Key not found in s")
  end_i = i + len(k)
  return s[:end_i] + ins + s[end_i:]

def create_component(t, id_, info, in_v=False, set_p=False, c=False, h=False):
  """
  Args:
    t: (str) the component to be created

  Returns: (obj) An instance of the component to be created
  """
  if t == 'UIButton':
    return UIButton(id_, info, in_v=in_v, set_p=set_p)
  elif t == 'UILabel':
    return UILabel(id_, info, in_v=in_v, set_p=set_p, in_c=c, in_h=h)
  elif t == 'UIImageView':
    return UIImageView(id_, info, in_v=in_v, set_p=set_p)
  elif t == 'UITableView':
    return UITableView(id_, info, in_v=in_v, set_p=set_p)
  elif t == 'UITextField':
    return UITextField(id_, info, in_v=in_v, set_p=set_p)
  elif t == 'UITextView':
    return UITextView(id_, info, in_v=in_v, set_p=set_p)
  elif t == 'UIView':
    return UIView(id_, info, in_v=in_v, set_p=set_p)
