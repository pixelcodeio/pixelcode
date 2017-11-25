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
      type_: (str) the component to be generated
      info: (dict) vals can be None. Further documentation can be found online
      bgc: (tuple) background color of the screen (used for generating labels)
      in_v: (bool) whether components are generated within a custom view

    Returns: (str) The swift code to generate the component
    """
    id_ = info.get('id')
    rect = info.get('rect')

    c = ""
    if not in_v:
      c += "{} = {}()\n".format(id_, type_)

    c += '{}.translatesAutoresizingMaskIntoConstraints = false\n'.format(id_)

    if rect is not None:
      c += utils.setup_rect(id_, rect)

    component = utils.create_component(type_, id_, info, in_v=in_v)
    c += component.swift

    if type_ == 'UITableView':
      self.tv_methods = component.tv_methods
    elif type_ == 'UILabel':
      c += utils.set_bg(id_, bgc, in_v=in_v)

    view = 'view' if not in_v else None
    c += utils.add_subview(view, id_)
    c += self.gen_constraints(info, in_v=in_v)
    return c

  def gen_constraints(self, info, in_v=False):
    """
    Args:
      info: contains all information on the element
      in_v: whether the element is in a view

    Returns: (str) swift code to set all constraints using SnapKit.
    """
    id_ = info.get('id')
    height = info.get('height')
    hor = info.get('horizontal')
    hor_dir = hor.get('direction')
    hor_dist = hor.get('distance')
    hor_id = hor.get('id')
    vert = info.get('vertical')
    vert_dir = vert.get('direction')
    vert_dist = vert.get('distance')
    vert_id = vert.get('id')
    width = info.get('width')
    if in_v:
      c = ("{}.snp.updateConstraints {{ make in\n"
           "make.size.equalTo(CGSize(width: frame.width*{}, height: "
           "frame.height*{}))\n"
          ).format(id_, width, height)
      if not hor_id:
        c += ('make.left.equalToSuperview().offset(frame.width*{})\n'
             ).format(hor_dist)
      else:
        opp_dir = 'left' if hor_dir == 'right' else 'right'
        c += ('make.{}.equalTo({}.snp.{}).offset(frame.width*{})\n'
             ).format(hor_dir, hor_id, opp_dir, hor_dist)
      if not vert_id:
        c += ('make.top.equalToSuperview().offset(frame.height*{})\n'
             ).format(vert_dist)
      else:
        vert_dir = 'top' if vert_dir == 'up' else 'bottom'
        opp_dir = 'top' if vert_dir == 'bottom' else 'bottom'
        c += ('make.{}.equalTo({}.snp.{}).offset(frame.height*{})\n'
             ).format(vert_dir, vert_id, opp_dir, vert_dist)
      c += "}\n\n"
      return c

    c = ("{}.snp.makeConstraints {{ make in\n"
         "make.size.equalTo(CGSize(width: view.frame.width*{}, height: "
         "view.frame.height*{}))\n"
        ).format(id_, width, height)
    if not hor_id:
      c += ('make.left.equalToSuperview().offset(view.frame.width*{})\n'
           ).format(hor_dist)
    else:
      opp_dir = 'left' if hor_dir == 'right' else 'right'
      c += ('make.{}.equalTo({}.snp.{}).offset(view.frame.width*{})\n'
           ).format(hor_dir, hor_id, opp_dir, hor_dist)
    if not vert_id:
      c += ('make.top.equalToSuperview().offset(view.frame.height*{})\n'
           ).format(vert_dist)
    else:
      vert_dir = 'top' if vert_dir == 'up' else 'bottom'
      opp_dir = 'top' if vert_dir == 'bottom' else 'bottom'
      c += ('make.{}.equalTo({}.snp.{}).offset(view.frame.height*{})\n'
           ).format(vert_dir, vert_id, opp_dir, vert_dist)
    c += "}\n\n"
    return c
