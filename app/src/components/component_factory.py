import components.utils as utils
from . import *

class ComponentFactory(object):
  """
  Base class for components
    swift: (str) contains the swift code to generate a component
    tv_methods: (str) contains the tableview methods for generating a tableview
  """
  def __init__(self, comp, info, bgc=None, in_view=False):
    """
    Args:
      bgc: Refers to background color
      Refer to generate_component for documentation on args
    """
    self.tv_methods = ""
    self.swift = self.generate_component(comp, info, bgc=bgc, in_view=in_view)

  def create_component(self, comp, bgc=None):
    """
    Args:
      comp: (str) the component to be created

    Returns: (obj) An instance of the component to be created
    """
    return {
        "UIButton": UIButton(),
        "UILabel": UILabel(bgc),
        "UIImageView": UIImageView(),
        "UITableView": UITableView(),
        "UITextField": UITextField(),
        "UITextView": UITextView(),
        "UIView": UIView(),
    }.get(comp, None)

  def generate_component(self, comp, info, bgc=None, in_view=False):
    """
    Args:
      comp: (str) The component to be generated
      info: (dict) A dictionary of with values possibly being None. Further
            documentation is available online.
      bgc: (tuple) background color of the screen (used for generating labels)
      in_view: (bool) represents whether the components are being generated
               inside a custom view file (or not)

    Returns: The swift code to generate the component
    """
    obj = self.create_component(comp, bgc=bgc)
    cid = info.get('id')
    height = info.get('height')
    hor = info.get('horizontal')
    hor_dir = hor.get('direction')
    hor_dist = hor.get('distance')
    hor_id = hor.get('id')
    rect = info.get('rect')
    text = info.get('text')
    vert = info.get('vertical')
    vert_dir = vert.get('direction')
    vert_dist = vert.get('distance')
    vert_id = vert.get('id')
    width = info.get('width')
    left_inset = info.get('left-inset')

    c = ""
    if not in_view:
      c += "{} = {}()\n".format(cid, comp)

    c += utils.translates_false(cid)

    if rect is not None:
      c += utils.setup_rect(cid, rect)

    if comp == 'UIView':
      c += obj.setup_uiview(cid, info)
    elif text is not None and comp == 'UIButton':
      textspan = text['textspan']
      c += obj.setup_uibutton(cid, textspan, in_view=in_view)
    elif comp == 'UILabel':
      textspan = info['textspan']
      line_sp = info.get('line-spacing')
      char_sp = info.get('char-spacing')
      c += obj.setup_uilabel(cid, textspan, line_sp, char_sp, in_view=in_view)
    elif text is not None:
      textspan = text['textspan']
      if comp == 'UITextField':
        c += obj.setup_uitextfield(cid, textspan, left_inset, in_view=in_view)
      elif comp == 'UITextView':
          c += obj.setup_uitextview(cid, textspan, left_inset, in_view=in_view)
    elif comp == 'UIImageView':
      c += obj.setup_uiimageview(cid, info, in_view=in_view)
    elif comp == 'UITableView':
      cells = info['cells']
      header = info['header']
      c += obj.setup_uitableview(cid, cells, header)
      tvm = obj.cell_for_row_at(cid, cells) # tvm are the tableview methods
      tvm += obj.number_of_rows_in_section(cells)
      tvm += obj.height_for_row_at(cid, cells)
      if header is not None:
        tvm += obj.view_for_header(cid, header)
        tvm += obj.height_for_header(cid, header)
      self.tv_methods = tvm

    if not in_view:
      c += utils.add_subview('view', cid)
    else:
      c += utils.add_subview(None, cid)
    c += utils.make_snp_constraints(cid, hor_id, hor_dir,
                                    hor_dist, vert_id, vert_dir,
                                    vert_dist, width, height, in_view)
    return c
