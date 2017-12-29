from components._all import *
from . import *

class ComponentFactory(object):
  """
  Initializes components (constraints, background-color, etc.)
    swift (str): swift code to generate a component
    info (dict): contains information about component
    methods (dict): contains methods to be added outside of file's init function
    in_view (bool): whether component is generated inside a custom view file
  """
  def __init__(self, info, in_v):
    """
    Args:
      info (dict): info on component
      in_v (bool): is whether generating from within a custom view
    """
    self.info = info
    self.methods = {}
    self.in_view = in_v
    self.swift = self.generate_component()

  def generate_component(self):
    """
    Returns: (str) The swift code to generate component
    """
    id_ = self.info["id"]
    type_ = self.info["type"]
    C = ""

    if not self.in_view:
      C += self.init_comp(type_, id_)

    # prepare for create_component
    self.prepare_for_create_component()

    env = {"in_view": self.in_view}
    component = self.create_component(type_, id_, self.info, env)
    C += component.swift

    # finish creating component
    return self.finish_creating_component(C, component)


  def prepare_for_create_component(self):
    """
    Returns (None): preparation before creating component
    """
    type_ = self.info["type"]
    if type_ == 'UITableView' or type_ == 'UICollectionView':
      self.setup_set_properties()
    elif type_ == 'UINavBar':
      self.setup_navbar_items()

  def finish_creating_component(self, swift, component):
    """
    Returns (str): swift code with finishing touches to creating component
    """
    keys = ["id", "type", "rect", "filter"]
    id_, type_, rect, filter_ = utils.get_vals(keys, self.info)

    if rect is not None:
      swift += utils.setup_rect(id_, type_, rect)
      if rect.get("filter") is not None and not self.in_view:
        # move code for shadows to viewDidLayoutSubviews function
        shadow = utils.add_shadow(id_, type_, rect["filter"])
        swift = swift.replace(shadow, "")
        self.methods["viewDidLayoutSubviews"] = shadow

    if filter_ is not None:
      shadow = utils.add_shadow(id_, type_, filter_)
      if self.in_view:
        swift += shadow
      else:
        self.methods["viewDidLayoutSubviews"] = shadow

    if type_ == 'UIView' and self.info.get('components') is not None:
      # generate subcomponents
      id_ = self.info['id']
      components = self.info['components']
      swift += self.gen_subcomponents(id_, components, True)
    elif type_ == 'UITableView' or type_ == 'UICollectionView':
      # extract (table/collection) view methods
      self.methods["tc_methods"] = component.tc_methods
    elif type_ == 'UILabel':
      swift += utils.set_bg(id_, [0, 0, 0, 0]) # set label to clear background
    elif type_ == 'SliderView':
      self.methods["slider_content_methods"] = component.content_methods
      return swift
    elif type_ in {'UINavBar', 'UITabBar', 'UIActionSheet'}:
      if type_ == "UIActionSheet":
        # move UIActionSheet code to viewDidAppear function
        swift = swift.replace(component.swift, "")
        self.methods["viewDidAppear"] = component.swift
      return swift

    view = 'view' if not self.in_view else None
    swift += utils.add_subview(view, id_, type_)
    swift += self.gen_constraints(self.info)
    return swift

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
    if type_ == "UICollectionView":
      return ("let layout = UICollectionViewFlowLayout()\n"
              "{} = {}(frame: .zero, collectionViewLayout: layout)\n"
             ).format(id_, type_)
    elif type_ == "UITableView":
      return ("{} = {}(frame: .zero, style: .grouped)\n").format(id_, type_)
    elif "barButton" in id_ or "BarButton" in id_:
      return "{} = UIButton(type: .system)\n".format(id_)
    elif type_ in {"UINavBar", "UITabBar", "UIActionSheet"}:
      return "" # cannot initialize these components
    elif type_ == 'UILabel':
      type_ = "InsetLabel" # use our custom label
    elif type_ == "UISegmentedControl":
      items = ['"' + i.decode('utf-8') + '"' for i in self.info["items"]]
      return ("{} = {}(items: [{}])\n").format(id_, type_, ", ".join(items))
    return "{} = {}()\n".format(id_, type_)

  def setup_set_properties(self):
    """
    Returns (None):
      Adds code for setting properties of all cells/headers' subcomponents to
      the info instance variable.
    """
    if self.info.get('header') is not None:
      # set properties for components in header
      ids = []
      C = "case 0:\n"
      components = self.info['header']['components']
      ids = [comp.get('id') for comp in components]
      C += self.gen_subcomponents_properties("header", components, ids)
      self.info["header_set_prop"] = C

    # set properties for components in cells
    cells = self.info['cells']
    fst_cell_comps = cells[0].get('components')
    ids = [comp.get('id') for comp in fst_cell_comps]

    C = ""
    case = 0
    for cell in cells:
      components = cell.get('components')
      if len(components) != len(fst_cell_comps):
        continue
      C += '\ncase {}:\n'.format(case)
      C += self.gen_subcomponents_properties("cell", components, ids)
      C += 'return cell'
      case += 1

    self.info["cell_set_prop"] = C

  def gen_subcomponents(self, parent, components, add_constraints):
    """
    Returns (str): swift code to generate subcomponents of parent_id
    """
    C = ""

    for comp in components:
      type_ = comp.get('type')
      id_ = comp.get('id')
      C += self.init_comp(type_, id_)
      com = self.create_component(type_, id_, comp, {})
      C += com.swift
      C += utils.set_frame(comp) if not add_constraints else ""
      C += utils.add_subview(parent, id_, type_) if parent is not None else ""
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
    # cannot set properties of nested collection view
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
    C = ""
    if title is not None:
      C += self.init_comp(title['type'], title['id'])
      C += utils.set_frame(title)
      C += self.gen_subcomponents(title['id'], title.get('components'), False)
    self.info['title-code'] = C
