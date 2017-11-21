from . import *

def translates_false(elem):
  """
  Returns: The line that sets the translatesAutoResizing property
  of elem to false.
  """
  return '{}.translatesAutoresizingMaskIntoConstraints = false\n'.format(elem)

def set_bg(elem, color, inView=False):
  """
  Args:
    color: (tuple) contains the r, g, b values of the background color

  Returns: The line that sets the background color of elem to the
  UIColor with the corresponding r, g, b values.
  """
  r, g, b, o = color
  if o is None:
    o = "1.0"
  if inView:
    return ('backgroundColor = UIColor(red: {}/255.0 , green: '
            '{}/255.0 , blue: {}/255.0 , alpha: {})\n'
           ).format(r, g, b, o)
  return ('{}.backgroundColor = UIColor(red: {}/255.0 , green: '
          '{}/255.0 , blue: {}/255.0 , alpha: {})\n'
         ).format(elem, r, g, b, o)

def add_subview(view, elem):
  if view is None:
    return 'addSubview({})\n\n'.format(elem)
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
                         vertDist, width, height, inView=False):
  """
  Returns: The swift code to set width/height and position constraints using
  the SnapKit library.
  """
  if inView:
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

def set_border_width(elem, width, inView=False):
  """
  Returns: The swift code to set the border width of elem.
  """
  if inView:
    return ("layer.borderWidth = {}\n").format(width)
  return ("{}.layer.borderWidth = {}\n").format(elem, width)

def set_border_color(elem, color, inView=False):
  """
  Returns: The swift code to set the border color of elem.
  """
  r, g, b, o = color
  if o is None:
    o = "1.0"
  if inView:
    return ("layer.borderColor = UIColor(red: {}/255.0, green: {}/255.0, "
            "blue: {}/255.0, alpha: {}).cgColor\n"
           ).format(r, g, b, o)
  return ("{}.layer.borderColor = UIColor(red: {}/255.0, green: {}/255.0, "
          "blue: {}/255.0, alpha: {}).cgColor\n"
         ).format(elem, r, g, b, o)

def set_corner_radius(elem, radius, inView=False):
  """
  Returns: The swift code to set the corner radius of elem.
  """
  if inView:
    return ("layer.cornerRadius = {}\n").format(radius)
  return ("{}.layer.cornerRadius = {}\n").format(elem, radius)

def create_object(comp, bgColor=None):
  """
  Args:
    comp: (str) the component to be created

  Returns: An instance of the component to be created
  """
  return {
      "UIButton": UIButton(),
      "UILabel": UILabel(bgColor),
      "UIImageView": UIImageView(),
      "UITableView": UITableView(),
      "UITextField": UITextField(),
      "UITextView": UITextView(),
      "UIView": UIView(),
  }.get(comp, None)
