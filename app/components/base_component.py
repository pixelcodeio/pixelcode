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

  def generate_component(self, comp, info, bgColor):
    """
    Args:
      comp (str): represents the component that is to be generated
      info (dict): is a dictionary of keys (values may be None):
        - id: (str) name of view
        - text: (str) text that is to be displayed
        - text-color: (tuple) r, g, b values of the text color
        - text-align: (str) alignment center of text
        - opacity: (float) between 0 and 1. global, fill, stroke.
        - subtext-colors: (dict array) dict array containing colors and indices
                         of substrings of the text.
        - subtext-fonts: (dict array) dict array containing the fonts of
                        substrings of the text.
        - title: (str) title that is to be displayed on the button OR the
                 placeholder to be displayed in an empty text(field/view)
        - title-color: (tuple) r, g, b values of the title color OR of the
                       placeholder to be displayed in an empty text(field/view)
        - fill: (tuple) r, g, b values for background color. Has value
                None if no value is provided
        - font-size: (int) font-size of the text
        - font-family: (str) name of the font of title
        - x: (float) x-coor of view's center as percentage of screen's width
        - y: (float) y-coor of view's center as percentage of screen's height
        - vertical: (dict) dict containing constraints for top/bottom of view
        - horizontal: (dict) dict containing constraints for left/right of view
        - width: (float) width of view as percentage of screen's width
        - height: (float) height of view as percentage of screen's height
        - stroke-color: (tuple) r, g, b values representing the border
                        color. Has value None if no value is provided
        - stroke-width: (int) the number of pixels representing the
                        border width. Has value None if no value is provided
        - border-radius: (int) the number of pixels representing the
                         corner radius. Has value None if no value is provided
        - placeholder: (str) the text to be displayed in an empty textfield
                       or textview
        - left-inset: (int) the number of pixels of the left-inset of a
                      textfield or textview
      bgColor: (optional tuple) background color of as r, g, b values
               (used for labels)

    Returns: object to be sent to the interpreter class
    """
    obj = self.create_object(comp, info, bgColor)
    borColor = info['stroke-color']
    borWidth = info['stroke-width']
    centerX = info['x']
    centerY = info['y']
    cid = info['id']
    corRad = info['border-radius']
    fill = info['fill']
    fontFamily = info['font-family']
    fontSize = info['font-size']
    height = info['height']
    horizontal = info['horizontal']
    horizontalDir = horizontal['direction']
    horizontalDist = horizontal['distance']
    horizontalID = horizontal['id']
    # subtextColors = info['subtext-colors']
    # subtextFonts = info['subtext-fonts']
    title = info['title']
    titleColor = info['title-color']
    txt = info['text']
    txtAlign = info['text-align']
    txtColor = info['text-color']
    vertical = info['vertical']
    verticalDir = vertical['direction']
    verticalDist = vertical['distance']
    verticalID = vertical['id']
    width = info['width']
    placeholder = info['placeholder']
    leftInset = info['left-inset']
    c = "{} = {}()\n".format(cid, comp)
    c += utils.translates_false(cid)
    if fill != None:
      c += utils.set_bg(cid, fill)
    if comp == 'UILabel':
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
      c += obj.set_text(cid, txt) if txt != None else ""
      c += obj.set_text_color(cid, txtColor) if txtColor != None else ""
      c += obj.set_bg_color(cid)
      c += obj.set_font_size(cid, fontSize)
      if txtAlign is None:
        c += obj.center_and_wrap(cid, "center")
      else:
        c += obj.center_and_wrap(cid, txtAlign)
      c += obj.set_font_family(cid, fontFamily, fontSize)
    elif comp == 'UIButton':
      c += obj.set_title(cid, title)
      c += obj.set_title_color(cid, titleColor)
      c += obj.set_font_size(cid, fontSize)
      c += obj.set_font_family(cid, fontFamily, fontSize)
    elif comp == 'UIImageView':
      c += obj.set_image(cid)
    elif comp == 'UITextField' or comp == 'UITextView':
      if title != None and titleColor != None:
        r = titleColor[0]
        g = titleColor[1]
        b = titleColor[2]
        c += obj.set_placeholder_text_and_color(cid, title, r, g, b)
      if leftInset != None:
        c += obj.set_left_inset(cid, leftInset)
      c += obj.set_text_font_and_size(cid, fontFamily, fontSize)
      c += obj.set_clips_to_bounds(cid)
    c += utils.set_border_color(cid, borColor) if borColor != None else ""
    c += utils.set_border_width(cid, borWidth) if borWidth != None else ""
    c += utils.set_corner_radius(cid, corRad) if corRad != None else ""
    c += utils.add_subview('view', cid)
    c += utils.wh_constraints(cid, width, height)
    c += utils.position_constraints(
        cid, horizontalID, horizontalDir, horizontalDist, verticalID,
        verticalDir, verticalDist, centerX, centerY)
    return c
