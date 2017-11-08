import components.utils as utils

class UITextField(object):
  """
  Class representing a UITextField in swift
  """
  def __init__(self):
    pass

  def set_placeholder(self, tid, text):
    return '{}.placeholder = "{}"'.format(tid, text)

  def set_left_inset(self, tid, left):
    return ('{}.layer.sublayerTransform = CATransform3DMakeTranslations({}'
            ', 0, 0)'
           ).format(tid, left)
