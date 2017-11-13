import components.utils as utils
from . import *

class BaseComponent(object):
  """
  Base class for components
  """
  def __init__(self, comp, info, bgColor=None):
    """
    Args:
      Refer to generate_component for documentation on args
    """
    self.swift = self.generate_component(comp, info, bgColor)

  def create_object(self, comp, info, bgColor):
    """
    Args:
      comp: (str) the component to be created
      info: (dict) dictionary of keys used in base_component
      bgColor: (tuple) background color of as r, g, b values (used for labels)

    Returns: An instance of the component to be created
    """
    if comp == 'UIView':
      return UIView()
    elif comp == 'UILabel':
      return UILabel(bgColor)
    elif comp == 'UIImageView':
      return UIImageView()
    elif comp == 'UIButton':
      return UIButton()
    elif comp == 'UITextField':
      return UITextField()
    elif comp == 'UITextView':
      return UITextView()
    return ""

  def setup_rect(self, cid, rect):
    """
    Args:
      cid: (int) id of component
      rect: (dict) see generate_component for more information

    Returns: The swift code to apply all the properties from rect.
    """
    fill = rect['fill']
    border_r = rect['border-radius']
    stroke_c = rect['stroke-color']
    stroke_w = rect['stroke-width']
    opacity = rect['opacity']
    c = utils.set_bg(cid, fill, opacity) if fill != None else ""
    c += utils.set_border_color(cid, stroke_c) if stroke_c != None else ""
    c += utils.set_border_width(cid, stroke_w) if stroke_w != None else ""
    c += utils.set_corner_radius(cid, border_r) if border_r != None else ""
    return c

  def generate_component(self, comp, info, bgColor):
    """
    Args:
      comp (str): represents the component that is to be generated
      info (dict): is a dictionary of keys (values may be None):
        - id: (str) name of view
        - x: (float) x-coor of view's center as percentage of screen's width
        - y: (float) y-coor of view's center as percentage of screen's height
        - vertical: (dict) dict containing constraints for top/bottom of view
        - horizontal: (dict) dict containing constraints for left/right of view
        - width: (float) width of view as percentage of screen's width
        - height: (float) height of view as percentage of screen's height
        - path: (str) name of the image file (e.g. iphone.png)
        - opacity: (float) between 0 and 1.
        - stroke-color: (tuple) r, g, b values representing the border
                        color. Has value None if no value is provided
        - stroke-width: (int) the number of pixels representing the
                        border width. Has value None if no value is provided
        - left-inset: (int) the number of pixels of the left-inset of a
                      textfield or textview
        - rect: (dict) dictionary of following keys (values may be None):
          - fill: (tuple) r, g, b values for background color. Has value
                  None if no value is provided
          - stroke-color: (tuple) r, g, b values representing the border
                          color. Has value None if no value is provided
          - stroke-width: (int) the number of pixels representing the
                          border width. Has value None if no value is provided
          - border-radius: (int) the number of pixels representing the
                           corner radius. Has value None if no value is provided
          - opacity: (float) between 0 and 1.
        - text: (dict) contains a key for textspan. textspan is a dict array
          with the following keys:
          - contents: (str) the string to be displayed in the view
          - fill: (tuple) r, g, b values for string color. Has value
                  None if no value is provided
          - text-align: (str) alignment center of text
          - font-size: (int) font-size of the text
          - font-family: (str) name of the font of title
          - opacity: (float) between 0 and 1.
        - textspan: (dict array) dictionary with the keys described above

        # - subtext-colors: (dict array) dict array containing colors and
        #                  indices of substrings of the text.
        # - subtext-fonts: (dict array) dict array containing the fonts of
        #                 substrings of the text.

    Returns: The swift code to generate the component
    """
    obj = self.create_object(comp, info, bgColor)
    centerX = info['x']
    centerY = info['y']
    cid = info['id']
    height = info['height']
    horizontal = info['horizontal']
    horizontalDir = horizontal['direction']
    horizontalDist = horizontal['distance']
    horizontalID = horizontal['id']
    rect = info['rect']
    # subtextColors = info['subtext-colors']
    # subtextFonts = info['subtext-fonts']
    text = info['text']
    vertical = info['vertical']
    verticalDir = vertical['direction']
    verticalDist = vertical['distance']
    verticalID = vertical['id']
    width = info['width']
    left_inset = info['left-inset']
    c = "{} = {}()\n".format(cid, comp)
    c += utils.translates_false(cid)
    # if comp == 'UIView':
    #   print('rect is:')
    #   print(rect)
    if rect != None:
      c += self.setup_rect(cid, rect)
    if text != None and comp == 'UIButton':
      textspan = text['textspan']
      c += obj.setup_uibutton(cid, textspan)
    elif comp == 'UILabel':
      textspan = info['textspan']
      c += obj.setup_uilabel(cid, textspan)
      # if subtextColors is None and subtextFonts is None:
      #   c += obj.set_text(cid, txt) if txt != None else ""
      # else:
      #   c += obj.create_attributed_str(cid, txt)
      #   strID = "{}AttributedStr".format(cid)
      #   if subtextColors != None:
      #     for sub in subtextColors:
      #       color = sub['color']
      #       start = sub['start']
      #       length = sub['length']
      #       c += obj.set_substring_color(strID, color, start, length)
      #   if subtextFonts != None:
      #     for sub in subtextFonts:
      #       font = sub['font']
      #       size = sub['size']
      #       start = sub['start']
      #       length = sub['length']
      #       c += obj.set_substring_font(strID, font, size, start, length)
    elif text != None and comp == 'UITextField':
      textspan = text['textspan']
      c += obj.setup_uitextfield(cid, textspan, left_inset)
    elif text != None and comp == 'UITextView':
      textspan = text['textspan']
      c += obj.setup_uitextview(cid, textspan, left_inset)
    elif comp == 'UIImageView':
      c += obj.setup_uiimageview(cid, info)
    c += utils.add_subview('view', cid)
    c += utils.wh_constraints(cid, width, height)
    c += utils.position_constraints(
        cid, horizontalID, horizontalDir, horizontalDist, verticalID,
        verticalDir, verticalDist, centerX, centerY)
    return c
