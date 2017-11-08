import components.utils as utils

class UITextView(object):
  """
  Class representing a UITextView in swift
  """
  def __init__(self):
    pass

  def set_placeholder(self, tid, text):
    return '{}.placeholder = "{}"'.format(tid, text)

  def set_left_inset(self, tid, left):
    return ('{}.layer.sublayerTransform = CATransform3DMakeTranslation({}'
            ', 0, 0)'
           ).format(tid, left)
