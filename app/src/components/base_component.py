import components.utils as utils
from . import *

class BaseComponent(object):
  """
  Base class for components
  """
  def __init__(self, comp, info, bgColor=None, generating_cell=False,
               generating_header=False):
    """
    Args:
      Refer to generate_component for documentation on args
    """
    if generating_cell:
      self.cell = self.generate_cell(info)
    elif generating_header:
      self.tableViewHeader = self.generate_header(info)
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

  def setup_rect_for_header(self, cid, rect, inView=False):
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
      c += utils.set_bg_for_header(fill, opacity)
    if str_c is not None:
      c += utils.set_border_color(cid, str_c, str_o, inView)
    if str_w is not None:
      c += utils.set_border_width(cid, str_w, inView)
    if border_r is not None:
      c += utils.set_corner_radius(cid, border_r, inView)

    return c

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

    c = ""
    if not inView:
      c += "{} = {}()\n".format(cid, comp)

    c += utils.translates_false(cid)

    if rect is not None:
      c += self.setup_rect(cid, rect)

    if comp == 'UIView':
      c += obj.setup_uiview(cid, info)
    elif text is not None and comp == 'UIButton':
      textspan = text['textspan']
      c += obj.setup_uibutton(cid, textspan, inView)
    elif comp == 'UILabel':
      textspan = info['textspan']
      line_sp = info.get('line-spacing')
      char_sp = info.get('char-spacing')
      c += obj.setup_uilabel(cid, textspan, line_sp, char_sp, inView)
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
      # Assume no tableviews are within tableviews
      cells = info['cells']
      header = info['header']
      c += obj.setup_uitableview(cid, cells, header)
      tvm = obj.cell_for_row_at(cid, cells)
      tvm += obj.number_of_rows_in_section(cells)
      tvm += obj.height_for_row_at(cid, cells)
      if header is not None:
        tvm += obj.view_for_header(cid, header)
        tvm += obj.height_for_header(cid, header)
      self.tableViewMethods = tvm

    if not inView:
      c += utils.add_subview('view', cid)
    else:
      c += utils.add_subview(None, cid)
    c += utils.make_snp_constraints(cid, horizontalID, horizontalDir,
                                    horizontalDist, verticalID, verticalDir,
                                    verticalDist, width, height, inView)
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
    c = ("import UIKit\nimport SnapKit\n\nclass {}Cell: UITableViewCell {{\n\n"
        ).format(capID)

    for cell in cells:
      components = cell.get('components')
      for component in components:
        cid = component.get('id')
        ctype = component.get('type')
        c += 'var {} = {}()\n'.format(cid, ctype)
      break

    c += ("\noverride init(style: UITableViewCellStyle, reuseIdentifier: "
          "String?) {\n"
          "super.init(style: style, reuseIdentifier: reuseIdentifier)\n"
          "layoutSubviews()\n}\n\n"
          "override func layoutSubviews() {\n"
          "super.layoutSubviews()\n\n"
         )

    for cell in cells:
      rect = cell.get('rect')
      c += self.setup_rect(cid, rect, True)
      components = cell.get('components')
      for component in components:
        comp = component.get('type')
        c += self.generate_component(comp, component, None, True)
      break # we are only considering cells with the same components

    c += ("}\n\n required init?(coder aDecoder: NSCoder) {\n"
          'fatalError("init(coder:) has not been implemented")\n}\n\n}'
         )
    return c

  def generate_header(self, info):
    """
    Returns: The swift code to generate a UITableView header class file.
    """
    cid = info.get('id')
    header = info.get('header')
    capID = cid.capitalize()
    c = ("import UIKit\nimport SnapKit\n\nclass {}HeaderView: UITableViewHeader"
         "FooterView {{\n\n"
        ).format(capID)


    components = header.get('components')
    for component in components:
      cid = component.get('id')
      ctype = component.get('type')
      c += 'var {} = {}()\n'.format(cid, ctype)

    c += ("\noverride init(reuseIdentifier: String?) {\n"
          "super.init(reuseIdentifier: reuseIdentifier)\n"
          "layoutSubviews()\n}\n\n"
          "override func layoutSubviews() {\n"
          "super.layoutSubviews()\n\n"
         )

    rect = header.get('rect')
    c += self.setup_rect_for_header(cid, rect, True)
    for component in components:
      comp = component.get('type')
      c += self.generate_component(comp, component, None, True)

    c += ("}\n\n required init?(coder aDecoder: NSCoder) {\n"
          'fatalError("init(coder:) has not been implemented")\n}\n\n}'
         )
    return c
