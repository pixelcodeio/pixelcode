import components.utils as utils
from . import *

class BaseComponent(object):
  """
  Base class for components
  """
  def __init__(self, comp, info, bgColor=None, generating_cell=False):
    """
    Args:
      Refer to generate_component for documentation on args
    """
    if generating_cell is False:
      self.tableViewMethods = ""
      self.swift = self.generate_component(comp, info, bgColor)
    else:
      self.cell = self.generate_cell(info)

  def create_object(self, comp, bgColor=None):
    """
    Args:
      comp: (str) the component to be created

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
    elif comp == 'UITableView':
      return UITableView()
    return ""

  def setup_rect(self, cid, rect, inView=False):
    """
    Args:
      cid: (int) id of component
      rect: (dict) see generate_component for more information

    Returns: The swift code to apply all the properties from rect.
    """
    fill = rect['fill']
    border_r = rect['border-radius']
    str_c = rect['stroke-color']
    str_w = rect['stroke-width']
    opacity = rect['opacity']
    str_o = rect['stroke-opacity']
    c = utils.set_bg(cid, fill, inView, opacity) if fill != None else ""
    c += utils.set_border_color(cid, str_c, str_o, inView) if str_c != None else ""
    c += utils.set_border_width(cid, str_w, inView) if str_w != None else ""
    c += utils.set_corner_radius(cid, border_r, inView) if border_r != None else ""
    return c

  def cell_for_row_at(self, elem, cells):
    """
    Args:
      cells: see generate_component's docstring for more information

    Returns: The swift code for the cellForRowAt function of a UITableView.
    """
    capElem = elem.capitalize()
    c = ("func tableView(_ tableView: UITableView, cellForRowAt "
         "indexPath: IndexPath) -> UITableViewCell {{\n"
         'let cell = {}.dequeueReusableCell(withIdentifier: "{}ID") as! '
         '{}Cell\n'
         "switch indexPath.row {{"
        ).format(elem, elem, capElem)
    for i, cell in enumerate(cells):
      components = cell['components']
      c += '\ncase {}:\n'.format(i)
      for component in components:
        comp = component['type']
        cid = component['id']
        obj = self.create_object(comp)
        cellComp = "cell.{}".format(cid)
        if comp == 'UIButton':
          contents = component['text']['textspan'][0]['contents']
          if contents != None:
            # assuming not varying text
            c += obj.set_title(cellComp, contents)
        elif comp == 'UIImageView':
          path = component['path']
          if path != None:
            c += obj.set_image(cellComp, path)
        elif comp == 'UILabel':
          contents = component['textspan'][0]['contents']
          if contents != None:
            c += obj.set_text(cellComp, contents)
        elif comp == 'UITextField' or comp == 'UITextView':
          textspan = component['text']['textspan']
          placeholder = textspan[0]['contents']
          placeholder_c = textspan[0]['fill']
          opacity = textspan[0]['opacity']
          c += obj.set_placeholder_text_and_color(cellComp, placeholder,
                                                  placeholder_c, opacity)
      c += '\nreturn cell'
    c += '\ndefault: return cell\n}\n}\n\n'
    return c

  def number_of_rows_in_section(self, cells):
    """
    Args:
      cells: see generate_component's docstring for more information

    Returns: The swift code for the numberOfRowsInSection func of a UITableView.
    """
    numRows = len(cells)
    return ("func tableView(_ tableView: UITableView, "
            "numberOfRowsInSection section: Int) -> Int {{\n"
            "return {} \n"
            "}}\n"
           ).format(numRows)

  def height_for_row_at(self, elem, cells):
    """
    Args:
      cells: see generate_component's docstring for more information
      tvHeight: (float) height of the uitableview as percentage of screen's
                height

    Returns: The swift code for the heightForRowAt func of a UITableView.
    """
    cellHeightPerc = cells[0]['rect']['height']
    print(cellHeightPerc)
    return ("func tableView(_ tableView: UITableView, heightForRowAt "
            "indexPath: IndexPath) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(elem, cellHeightPerc)

  def generate_component(self, comp, info, bgColor=None, inView=False):
    """
    Args:
      comp (str): represents the component that is to be generated
      info (dict): is a dictionary of keys (values may be None):
        - id: (str) name of view
        - x: (float) x-coor of view's center as pixels
        - y: (float) y-coor of view's center as pixels
        - cx: (float) x-coor of view's center as percentage of screen's width
        - cy: (float) y-coor of view's center as percentage of screen's height
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
          - stroke-opacity: (float) between 0 and 1 of the border opacity
          - border-radius: (int) the number of pixels representing the
                           corner radius. Has value None if no value is provided
          - opacity: (float) between 0 and 1.
        - text: (dict) contains a key for textspan. textspan is a dict list
          with the following keys:
          - contents: (str) the string to be displayed in the view
          - fill: (tuple) r, g, b values for string color. Has value
                  None if no value is provided
          - text-align: (str) alignment center of text
          - font-size: (int) font-size of the text
          - font-family: (str) name of the font of title
          - opacity: (float) between 0 and 1.
        - textspan: (dict list) dictionary with the keys described above
        - cells: (dict list) list of dictionary with keys:
          - rect: (dict) described above
          - components: (list) list of components (a component can be a button,
                        textfield, textview, label, or imageview)
        - inView: (boolean) of whether component is being generated inside a
                  view class or not

        # - subtext-colors: (dict list) dict list containing colors and
        #                  indices of substrings of the text.
        # - subtext-fonts: (dict list) dict list containing the fonts of
        #                 substrings of the text.

    Returns: The swift code to generate the component
    """
    obj = self.create_object(comp, bgColor)
    centerX = info['cx']
    centerY = info['cy']
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
    if inView is True:
      c = "var {} = {}()\n".format(cid, comp)
    else:
      c = "{} = {}()\n".format(cid, comp)
    c += utils.translates_false(cid)
    # if comp == 'UIView':
    #   print('rect is:')
    #   print(rect)
    if rect != None:
      c += self.setup_rect(cid, rect)
    if comp == 'UIView':
      c += obj.setup_uiview(cid, info)
    elif text != None and comp == 'UIButton':
      textspan = text['textspan']
      c += obj.setup_uibutton(cid, textspan, inView)
    elif comp == 'UILabel':
      textspan = info['textspan']
      c += obj.setup_uilabel(cid, textspan, inView)
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
      c += obj.setup_uitextfield(cid, textspan, left_inset, inView)
    elif text != None and comp == 'UITextView':
      textspan = text['textspan']
      c += obj.setup_uitextview(cid, textspan, left_inset, inView)
    elif comp == 'UIImageView':
      c += obj.setup_uiimageview(cid, info, inView)
    elif comp == 'UITableView':
      # TODO: assuming no tableviews are within tableviews
      cells = info['cells']
      c += obj.setup_uitableview(cid, cells)
      tvm = self.cell_for_row_at(cid, cells)
      tvm += self.number_of_rows_in_section(cells)
      tvm += self.height_for_row_at(cid, cells)
      self.tableViewMethods = tvm
    if inView is False:
      c += utils.add_subview('view', cid)
    else:
      c += utils.add_subview(None, cid)
    c += utils.wh_constraints(cid, width, height, inView)
    c += utils.position_constraints(
        cid, horizontalID, horizontalDir, horizontalDist, verticalID,
        verticalDir, verticalDist, centerX, centerY, inView)
    return c

  def generate_cell(self, info):
    """
    Args:
      info: see generate_component's docstring for more information

    Returns: The swift code to generate a UITableViewCell swift file
    """
    cid = info['id']
    cells = info['cells']
    capID = cid.capitalize()
    c = ("import UIKit\n class {}Cell: UITableViewCell {{\n").format(capID)
    for cell in cells:
      components = cell['components']
      for component in components:
        cid = component['id']
        ctype = component['type']
        c += 'var {} = {}()\n'.format(cid, ctype)
      break
    c += ("override init(style: UITableViewCellStyle, reuseIdentifier: "
          "String?) {\n"
          "super.init(style: style, reuseIdentifier: reuseIdentifier)\n\n"
         )
    for cell in cells:
      rect = cell['rect']
      components = cell['components']
      c += self.setup_rect(cid, rect, True)
      for component in components:
        #comp, info, bgColor=None, inView=False
        comp = component['type']
        c += self.generate_component(comp, component, None, True)
      break # we are only considering cells with the same components
    c += ("}\n\n required init?(coder aDecoder: NSCoder) {\n"
          'fatalError("init(coder:) has not been implemented")\n}\n\n}'
         )
    return c
