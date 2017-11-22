from components import *

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

def set_bg(elem, color, in_view=False):
  """
  Args:
    color: (tuple) contains the r, g, b values of the background color

  Returns: The line that sets the background color of elem to the
  UIColor with the corresponding r, g, b values.
  """
  if in_view:
    return ('backgroundColor = {}\n'
           ).format(create_uicolor(color))
  return ('{}.backgroundColor = {}\n'
         ).format(elem, create_uicolor(color))

def add_subview(view, elem):
  if view is None:
    return 'addSubview({})\n\n'.format(elem)
  return '{}.addSubview({})\n\n'.format(view, elem)

def wh_constraints(elem, width, height, in_view=False):
  """
  Returns: The swift code that sets the width and height constraints
  of the elem.
  """
  if in_view:
    return ('{}.widthAnchor.constraint(equalToConstant: contentView.frame.width'
            '*{}).isActive = true\n'
            '{}.heightAnchor.constraint(equalToConstant: contentView.frame.'
            'height*{}).isActive = true\n'
           ).format(elem, width, elem, height)
  return ('{}.widthAnchor.constraint(equalToConstant: view.frame.width*'
          '{}).isActive = true\n'
          '{}.heightAnchor.constraint(equalToConstant: view.frame.height*'
          '{}).isActive = true\n'
         ).format(elem, width, elem, height)

def position_constraints(elem, horID, horDir, horDist, vertID, vertDir,
                         vertDist, centerX, centerY, in_view=False):
  """
  Returns: The swift code to set the centerX and centerY constraints of
  the elem.
  """
  if in_view:
    c = ('{}.centerXAnchor.constraint(equalTo: contentView.leftAnchor, '
         'constant: contentView.frame.width*{}).isActive = true\n'
         '{}.centerYAnchor.constraint(equalTo: contentView.topAnchor, '
         'constant: contentView.frame.height*{}).isActive = true\n'
        ).format(elem, centerX, elem, centerY)
    if horID == '':
      c += ('{}.leftAnchor.constraint(equalTo: contentView.leftAnchor, '
            'constant: contentView.frame.width*{}).isActive = true\n'
           ).format(elem, horDist)
    else:
      oppDir = 'left' if horDir == 'right' else 'right'
      c += ('{}.{}Anchor.constraint(equalTo: {}.'
            '{}Anchor, constant: contentView.frame.width*{}'
            ').isActive = true\n'
           ).format(elem, horDir, horID, oppDir, horDist)
    if vertID == '':
      c += ('{}.topAnchor.constraint(equalTo: contentView.topAnchor, '
            'constant: contentView.frame.height*{}).isActive = true\n\n'
           ).format(elem, vertDist)
    else:
      vertDir = 'top' if vertDir == 'up' else 'bottom'
      oppDir = 'top' if vertDir == 'bottom' else 'bottom'
      c += ('{}.{}Anchor.constraint(equalTo: {}.'
            '{}Anchor, constant: contentView.frame.height*{}'
            ').isActive = true\n\n'
           ).format(elem, vertDir, vertID, oppDir, vertDist)
    return c
  c = ('{}.centerXAnchor.constraint(equalTo: view.leftAnchor, '
       'constant: view.frame.width*{}).isActive = true\n'
       '{}.centerYAnchor.constraint(equalTo: view.topAnchor, '
       'constant: view.frame.height*{}).isActive = true\n'
      ).format(elem, centerX, elem, centerY)
  if not horID:
    c += ('{}.leftAnchor.constraint(equalTo: view.leftAnchor, '
          'constant: view.frame.width*{}).isActive = true\n'
         ).format(elem, horDist)
  else:
    oppDir = 'left' if horDir == 'right' else 'right'
    c += ('{}.{}Anchor.constraint(equalTo: {}.'
          '{}Anchor, constant: view.frame.width*{}'
          ').isActive = true\n'
         ).format(elem, horDir, horID, oppDir, horDist)
  if not vertID:
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

def make_snp_constraints(elem, horID, horDir, horDist, vertID, vertDir,
                         vertDist, width, height, in_view=False):
  """
  Returns: The swift code to set width/height and position constraints using
  the SnapKit library.
  """
  if in_view:
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

def set_edges_constraints(elem, superview, top, bottom, left, right):
  """
  Returns: The swift code to set constraints on all edges of a subview relative
  to a superview.
  """
  return ("{}.topAnchor.constraint(equalTo: {}.topAnchor, constant: {}.frame."
          "height*{}).isActive = true\n"
          "{}.bottomAnchor.constraint(equalTo: {}.bottomAnchor, constant: -{}."
          "frame.height*{}).isActive = true\n"
          "{}.leftAnchor.constraint(equalTo: {}.leftAnchor, constant: {}.frame."
          "width*{}).isActive = true\n"
          "{}.rightAnchor.constraint(equalTo: {}.rightAnchor, constant: -{}."
          "frame.width*{}).isActive = true\n\n"
         ).format(elem, superview, superview, top, elem, superview, superview,
                  bottom, elem, superview, superview, left, elem, superview,
                  superview, right)

def set_border_width(elem, width, in_view=False):
  """
  Returns: The swift code to set the border width of elem.
  """
  if in_view:
    return ("layer.borderWidth = {}\n").format(width)
  return ("{}.layer.borderWidth = {}\n").format(elem, width)

def set_border_color(elem, color, in_view=False):
  """
  Returns: The swift code to set the border color of elem.
  """
  if in_view:
    return ("layer.borderColor = {}.cgColor\n"
           ).format(create_uicolor(color))
  return ("{}.layer.borderColor = {}.cgColor\n"
         ).format(elem, create_uicolor(color))

def set_corner_radius(elem, radius, in_view=False):
  """
  Returns: The swift code to set the corner radius of elem.
  """
  if in_view:
    return ("layer.cornerRadius = {}\n").format(radius)
  return ("{}.layer.cornerRadius = {}\n").format(elem, radius)

def setup_rect(cid, rect, in_view=False, tv_header=False):
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
      c += set_bg('contentView', fill, in_view=False)
    else:
      c += set_bg(cid, fill, in_view)
  if str_c is not None:
    c += set_border_color(cid, str_c, in_view)
  if str_w is not None:
    c += set_border_width(cid, str_w, in_view)
  if border_r is not None:
    c += set_corner_radius(cid, border_r, in_view)

  return c

def required_init():
  """
  Returns: The swift code for the required init?(coder:) function for custom
  views.
  """
  return ("required init?(coder aDecoder: NSCoder) {\n"
          'fatalError("init(coder:) has not been implemented")\n}')

def find_and_ins(s, k, ins):
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
    return ""
  end_i = i + len(k)
  return s[:end_i] + ins + s[end_i:]
