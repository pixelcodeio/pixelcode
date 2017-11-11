import components.utils as utils

class UITextField(object):
  """
  Class representing a UITextField in swift
  """
  def __init__(self):
    pass

  def set_placeholder_text_and_color(self, tid, text, r, g, b):
    color = ("UIColor(red: {}/255.0, green: {}/255.0, blue: {}/255.0, alpha"
             ": 1.0)"
            ).format(r, g, b)
    return ('{}.attributedPlaceholder = NSAttributedString(string: "{}", '
            'attributes: [NSAttributedStringKey.foregroundColor: {}])\n'
           ).format(tid, text, color)

  def set_left_inset(self, tid, left):
    return ('{}.layer.sublayerTransform = CATransform3DMakeTranslations({}'
            ', 0, 0)'
           ).format(tid, left)
