import utils
from . import *

class ComponentFactory(object):
  """
  Base class for components
    swift: (str) contains the swift code to generate a component
    tv_methods: (str) contains the tableview methods for generating a tableview
  """
  def __init__(self, type_, info, bgc=None, in_v=False):
    """
    Args:
      bgc: Refers to background color
      Refer to generate_component for documentation on args
    """
    self.tv_methods = ""
    self.swift = self.generate_component(type_, info, bgc=bgc, in_v=in_v)

  def generate_component(self, type_, info, bgc=None, in_v=False):
    """
    Args:
      type_: (str) The component to be generated
      info: (dict) A dictionary of with values possibly being None. Further
            documentation is available online.
      bgc: (tuple) background color of the screen (used for generating labels)
      in_v: (bool) represents whether the components are being generated
               inside a custom view file (or not)

    Returns: (str) The swift code to generate the component
    """
    cid = info.get('id')
    height = info.get('height')
    hor = info.get('horizontal')
    hor_dir = hor.get('direction')
    hor_dist = hor.get('distance')
    hor_id = hor.get('id')
    rect = info.get('rect')
    vert = info.get('vertical')
    vert_dir = vert.get('direction')
    vert_dist = vert.get('distance')
    vert_id = vert.get('id')
    width = info.get('width')

    c = ""

    if not in_v:
      c += "{} = {}()\n".format(cid, type_)

    c += utils.translates_false(cid)

    if rect is not None:
      c += utils.setup_rect(cid, rect)

    component = utils.create_component(type_, cid, info, in_v=in_v)
    c += component.swift
    if type_ == 'UITableView':
      self.tv_methods = component.tv_methods
    elif type_ == 'UILabel':
      c += utils.set_bg(cid, bgc, in_v=in_v)
    view = 'view' if not in_v else None
    c += utils.add_subview(view, cid)
    c += utils.make_snp_constraints(cid, hor_id, hor_dir,
                                    hor_dist, vert_id, vert_dir,
                                    vert_dist, width, height, in_v)
    return c
