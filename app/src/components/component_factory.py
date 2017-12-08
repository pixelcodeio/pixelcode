from components.uibutton import UIButton
from components.uiimageview import UIImageView
from components.uilabel import UILabel
from components.uinavbar import UINavBar
from components.uitablecollectionview import UITableCollectionView
from components.uitextfieldview import UITextFieldView
from components.uiview import UIView
from . import *

class ComponentFactory(object):
  """
  Initializes components (constraints, background-color, etc.)
    swift (str): swift code to generate a component
    info (dict): contains information about component
    tc_methods (str): (table/collection) view methods
    in_view (bool): whether component is generated inside a custom view file
  """
  def __init__(self, type_, info, in_v, bgc=None):
    """
    Args:
      bgc (tuple): background color of screen
      info (dict): info on component
      in_v (bool): is whether generating from within a custom view
    """
    self.tc_methods = ""
    self.info = info
    self.in_view = in_v
    self.swift = self.generate_component(type_, bgc)

  def generate_component(self, type_, bgc):
    """
    Returns: (str) The swift code to generate component
    """
    id_ = self.info.get('id')
    rect = self.info.get('rect')

    C = ""

    if type_ == 'UINavBar':
      self.setup_navbar_items()

    if not self.in_view:
      C += self.init_comp(type_, id_)

    if type_ == 'UITableView' or type_ == 'UICollectionView':
      self.setup_set_properties()

    env = {"in_view": self.in_view}
    component = self.create_component(type_, id_, self.info, env)
    C += component.swift

    if rect is not None:
      C += utils.setup_rect(id_, rect, self.in_view)

    if type_ == 'UIView' and self.info.get('components') is not None:
      id_ = self.info['id']
      components = self.info['components']
      C += self.gen_subcomponents(id_, components, True)

    if type_ == 'UITableView' or type_ == 'UICollectionView':
      self.tc_methods = component.tc_methods
    elif type_ == 'UILabel':
      C += utils.set_bg(id_, bgc)

    if type_ == 'UINavBar':
      return C

    view = 'view' if not self.in_view else None
    C += utils.add_subview(view, id_)
    C += self.gen_constraints(self.info)
    return C

  def create_component(self, type_, id_, info, env):
    """
    Args:
      env (dict): env for component. Possible keys are
                  [set_prop, in_view, in_cell, in_header]

    Returns: (obj) An instance of the component to be created
    """
    # init keys
    for key in ["set_prop", "in_view", "in_cell", "in_header"]:
      if key not in env:
        env[key] = False

    if type_ == 'UITextField' or type_ == 'UITextView':
      type_ = 'UITextFieldView'
    elif type_ == 'UITableView' or type_ == 'UICollectionView':
      type_ = 'UITableCollectionView'
    # using eval for clean code
    return eval(type_ + "(id_, info, env)") # pylint: disable=W0123

  def gen_constraints(self, component):
    """
    Returns: (str) swift code to set all constraints using SnapKit.
    """
    keys = ['id', 'height', 'width', 'horizontal', 'vertical']
    id_, height, width, hor, vert = utils.get_vals(keys, component)

    keys = ['id', 'direction', 'distance']
    hor_id, hor_dir, hor_dist = utils.get_vals(keys, hor)
    vert_id, vert_dir, vert_dist = utils.get_vals(keys, vert)

    C = ("{}.snp.updateConstraints {{ make in\n"
         "make.size.equalTo(CGSize(width: frame.width*{}, height: "
         "frame.height*{}))\n"
        ).format(id_, width, height)

    if hor_id:
      opp_dir = self.get_opp_dir(hor_dir)
      C += ('make.{}.equalTo({}.snp.{}).offset(frame.width*{})\n'
           ).format(hor_dir, hor_id, opp_dir, hor_dist)
    else:
      C += ('make.left.equalToSuperview().offset(frame.width*{})\n'
           ).format(hor_dist)

    if vert_id:
      opp_dir = self.get_opp_dir(vert_dir)
      if vert_id == 'navBar': # cannot position relative to navbar
        navbar_height = ("(self.navigationController?.navigationBar.intrinsicCo"
                         "ntentSize.height)!")
        C += ('make.{}.equalToSuperview().offset(frame.height*{} + {})\n'
             ).format(vert_dir, vert_dist, navbar_height)
      else:
        C += ('make.{}.equalTo({}.snp.{}).offset(frame.height*{})\n'
             ).format(vert_dir, vert_id, opp_dir, vert_dist)
    else:
      C += ('make.top.equalToSuperview().offset(frame.height*{})\n'
           ).format(vert_dist)
    C += "}\n\n"

    if not self.in_view:
      C = C.replace("frame", "view.frame")
    return C

  def get_opp_dir(self, d):
    """
    Returns: direction opposite to [d]
    """
    return {
        "top": "bottom",
        "bottom": "top",
        "left": "right",
        "right": "left"
    }[d]

  def init_comp(self, type_, id_):
    """
    Returns (str): swift code to initialize a component
    """
    if type_ == 'UICollectionView':
      return ("let layout = UICollectionViewFlowLayout()\n"
              "{} = {}(frame: .zero, collectionViewLayout: layout)\n"
             ).format(id_, type_)
    elif "barButton" in id_ or "BarButton" in id_:
      return "{} = UIButton(type: .system)\n".format(id_)
    elif type_ == 'UINavBar':
      return "" # cannot initialize a navigation bar
    return "{} = {}()\n".format(id_, type_)

  def setup_set_properties(self):
    """
    Returns (None):
      Adds code for setting properties of all cells/headers' subcomponents to
      the info instance variable.
    """
    if self.info.get('header') is not None:
      ids = []
      C = "case 0:\n"
      components = self.info.get('header').get('components')
      ids = [comp.get('id') for comp in components]
      C += self.gen_subcomponents_properties("header", components, ids)
      self.info["header_set_prop"] = C

    cells = self.info.get('cells')
    fst_cell_comps = cells[0].get('components')
    ids = [comp.get('id') for comp in fst_cell_comps]

    C = ""
    index = 0
    for cell in cells:
      components = cell.get('components')
      if len(components) != len(fst_cell_comps):
        continue
      C += '\ncase {}:\n'.format(index)
      C += self.gen_subcomponents_properties("cell", components, ids)
      C += 'return cell'
      index += 1

    self.info["cell_set_prop"] = C

  def gen_subcomponents(self, parent_id, components, add_constraints):
    """
    Returns (str): swift code to generate subcomponents
    """
    C = ""

    for comp in components:
      type_ = comp.get('type')
      id_ = comp.get('id')
      C += self.init_comp(type_, id_)
      com = self.create_component(type_, id_, comp, {})
      C += com.swift
      C += self.set_frame(comp) if not add_constraints else ""
      C += utils.add_subview(parent_id, id_) if parent_id is not None else ""
      C += self.gen_constraints(comp) if add_constraints else ""

    return C

  def gen_subcomponents_properties(self, c_or_h, components, ids):
    """
    Args:
      c_or_h: (str) should either be "cell" or "header"

    Returns (str):
      swift code to set properties of subcomponents inside a (table/collection)
      view cell/header.
    """
    C = ""
    components = [c for c in components if c['type'] != "UICollectionView"]
    for j, comp in enumerate(components):
      type_ = comp.get('type')
      id_ = "{}.{}".format(c_or_h, ids[j])

      env = {"set_prop": True}
      if type_ == 'UILabel':
        env["in_" + c_or_h] = True

      com = self.create_component(type_, id_, comp, env)
      C += com.swift
    return C

  def setup_navbar_items(self):
    """
    Returns (None): setups up code for navbar items inside self.info
    """
    keys = ['left-buttons', 'right-buttons', 'title']
    left, right, title = utils.get_vals(keys, self.info['navbar-items'])
    self.info['left-buttons-code'] = self.gen_subcomponents(None, left, False)
    self.info['right-buttons-code'] = self.gen_subcomponents(None, right, False)
    C = self.init_comp(title.get('type'), title.get('id'))
    C += self.set_frame(title)
    C += self.gen_subcomponents(title.get('id'), title.get('components'), False)
    self.info['title-code'] = C

  def set_frame(self, component):
    """
    Returns (str): swift code to set frame of the component
    """
    keys = ['id', 'x', 'y', 'rwidth', 'rheight']
    id_, x, y, w, h = utils.get_vals(keys, component)
    return ("{}.frame = CGRect(x: {}, y: {}, width: {}, height: {})\n"
           ).format(id_, x, y, w, h)
