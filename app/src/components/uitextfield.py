from . import *

class UITextField(BaseComponent):
  """
  Class representing a UITextField in swift
    swift: (str) the swift code to create/set properties of a UITextField
  """
  def generate_swift(self):
    if self.env["set_prop"]:
      tspan = info.get('text').get('textspan')
      placeholder = tspan[0]['contents']
      pl_color = tspan[0]['fill']
      return self.set_placeholder_tc(placeholder, pl_color)
    return self.setup_component()

  def set_placeholder_tc(self, text, color):
    """
    Args:
      text: (str) placeholder text
      color: (tuple) color of placeholder

    Returns: (str) swift code to set placeholder's text and color.
    """
    return ('{}.attributedPlaceholder = NSAttributedString(string: "{}", '
            'attributes: [NSAttributedStringKey.foregroundColor: {}])\n'
           ).format(self.id, text, utils.create_uicolor(color))

  def set_left_inset(self, left):
    """
    Args:
      left: (int) left-inset, in pixels

    Returns: (str) The swift code to set the left-inset of a UITextField
    """
    return ('{}.layer.sublayerTransform = CATransform3DMakeTranslation({}'
            ', 0, 0)\n'
           ).format(self.id, left)

  def set_font_family_size(self, font, size):
    """
    Args:
      font: (str) font family
      size: (int) font size

    Returns:
      (str) The swift code to set font-family and size of the title
    """
    return ("{}.font = {}\n").format(self.id, super().create_font(font, size))

  def setup_component(self):
    """
    Returns (str): swift code to setup uitextfield.
    """
    info = self.info
    tspan = info.get('text').get('textspan')
    left_inset = info.get('left-inset')
    txt = tspan[0]

    keys = ["contents", "fill", "font-family", "font-size"]
    placeholder, p_color, font, size = utils.get_vals(keys, txt)

    C = ""
    if not in_v:
      C += self.set_placeholder_tc(placeholder, p_color)
    C += self.set_font_family_size(font, size)
    C += self.set_left_inset(left_inset)
    C += super().clips_to_bounds()
    return C
