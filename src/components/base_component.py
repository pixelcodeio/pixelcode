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
    if generating_cell:
      self.cell = self.generate_cell(info)
    else:
      self.tableViewMethods = ""
      self.swift = self.generate_component(comp, info, bgColor)

  def create_object(self, comp, bgColor=None):
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

  def setup_rect(self, cid, rect, inView=False):
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
    opacity = rect.get('opacity')
    str_o = rect.get('stroke-opacity')

    c = ""
    if fill is not None:
      c += utils.set_bg(cid, fill, inView, opacity)
    if str_c is not None:
      c += utils.set_border_color(cid, str_c, str_o, inView)
    if str_w is not None:
      c += utils.set_border_width(cid, str_w, inView)
    if border_r is not None:
      c += utils.set_corner_radius(cid, border_r, inView)

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
      components = cell.get('components')
      c += '\ncase {}:\n'.format(i)
      for component in components:
        comp = component.get('type')
        cid = component.get('id')
        obj = self.create_object(comp)
        cellComp = "cell.{}".format(cid)

        if comp == 'UIButton':
          contents = component['text']['textspan'][0]['contents']
          if contents is not None:
            # assuming not varying text
            c += obj.set_title(cellComp, contents)

        elif comp == 'UIImageView':
          path = component.get('path')
          if path is not None:
            c += obj.set_image(cellComp, path)

        elif comp == 'UILabel':
          contents = component['textspan'][0]['contents']
          if contents is not None:
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
    cellHeightPerc = cells[0]['height']
    return ("func tableView(_ tableView: UITableView, heightForRowAt "
            "indexPath: IndexPath) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(elem, cellHeightPerc)

  def generate_component(self, comp, info, bgColor=None, inView=False):
    """
    Args:
      comp (str): The component to be generated
      info (dict):
        A dictionary of keys (values may be None). Further documentation is
        available online.

    Returns: The swift code to generate the component
    """
    obj = self.create_object(comp, bgColor)
    centerX = info.get('cx')
    centerY = info.get('cy')
    cid = info.get('id')
    height = info.get('height')
    horizontal = info.get('horizontal')
    horizontalDir = horizontal.get('direction')
    horizontalDist = horizontal.get('distance')
    horizontalID = horizontal.get('id')
    rect = info.get('rect')
    # subtextColors = info.get('subtext-colors')
    # subtextFonts = info.get('subtext-fonts')
    text = info.get('text')
    vertical = info.get('vertical')
    verticalDir = vertical.get('direction')
    verticalDist = vertical.get('distance')
    verticalID = vertical.get('id')
    width = info.get('width')
    left_inset = info.get('left-inset')

    if inView:
      c = "var {} = {}()\n".format(cid, comp)
    else:
      c = "{} = {}()\n".format(cid, comp)

    c += utils.translates_false(cid)
    # if comp == 'UIView':
    #   print('rect is:')
    #   print(rect)

    if rect is not None:
      c += self.setup_rect(cid, rect)

    if comp == 'UIView':
      c += obj.setup_uiview(cid, info)
    elif text is not None and comp == 'UIButton':
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
    elif text is not None and comp == 'UITextField':
      textspan = text['textspan']
      c += obj.setup_uitextfield(cid, textspan, left_inset, inView)
    elif text is not None and comp == 'UITextView':
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

    if not inView:
      c += utils.add_subview('view', cid)
    else:
      c += utils.add_subview('contentView', cid)
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
    cid = info.get('id')
    cells = info.get('cells')
    capID = cid.capitalize()
    c = ("import UIKit\n class {}Cell: UITableViewCell {{\n").format(capID)

    for cell in cells:
      components = cell.get('components')
      for component in components:
        cid = component.get('id')
        ctype = component.get('type')
        c += 'var {} = {}()\n'.format(cid, ctype)
      break

    c += ("override init(style: UITableViewCellStyle, reuseIdentifier: "
          "String?) {\n"
          "super.init(style: style, reuseIdentifier: reuseIdentifier)\n\n"
         )

    for cell in cells:
      rect = cell.get('rect')
      components = cell.get('components')
      c += self.setup_rect(cid, rect, True)
      for component in components:
        #comp, info, bgColor=None, inView=False
        comp = component.get('type')
        c += self.generate_component(comp, component, None, True)
      break # we are only considering cells with the same components

    c += ("}\n\n required init?(coder aDecoder: NSCoder) {\n"
          'fatalError("init(coder:) has not been implemented")\n}\n\n}'
         )
    return c
