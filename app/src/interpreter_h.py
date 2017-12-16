import utils

def init_g_vars(components):
  """
  Args:
    components: (dict list) contains info about components

  Returns (str): swift code to generate/init all glob vars of components
  """
  C = ""
  for comp in components:
    if comp['type'] == 'UICollectionView': # do not init collection views
      C += "var {}: UICollectionView!\n".format(comp['id'])
    elif comp['type'] == 'UINavBar': # cannot init navigation bars
      continue
    else:
      C += "var {} = {}()\n".format(comp['id'], comp['type'])
  return C

def declare_g_vars(components):
  """
  Returns (str): swift code to declare global variables
  """
  #components = list(self.info["components"]) # get copy of components
  navbar_items = [c.get("navbar-items") for c in components]
  navbar_items = [n for n in navbar_items if n is not None]
  if navbar_items:
    navbar_items = navbar_items[0] # only one nav bar per screen
    components.extend(navbar_items['left-buttons'])
    components.extend(navbar_items['right-buttons'])
    if navbar_items.get('title') is not None:
      components.append(navbar_items['title'])
      if navbar_items['title'].get('components') is not None:
        components.extend(navbar_items['title']['components'])

  # filter components to not include navigation bar
  filter_comps = [c for c in components if c['type'] != 'UINavBar']

  # one-liner to concat all variable names
  gvars = ["var {}: {}!\n".format(e['id'], e['type']) for e in filter_comps]
  return "".join(gvars)

def gen_cell_header(tc_id, cell):
  """
  Args:
    tc_id (str): id of the parent (table/collection)view
    cell (dict): info of cell being generated

  Returns (str): swift code to generate the header of a cell
  """
  tc_id = utils.uppercase(tc_id)
  C = ("import UIKit\nimport SnapKit\n\nclass {}Cell: UITableViewCell "
       "{{\n\n{}"
       "\noverride init(style: UITableViewCellStyle, reuseIdentifier: "
       "String?) {{\n"
       "super.init(style: style, reuseIdentifier: reuseIdentifier)\n"
       "layoutSubviews()\n}}\n\n"
       "override func layoutSubviews() {{\n"
       "super.layoutSubviews()\n\n"
      ).format(tc_id, init_g_vars(cell.get('components')))

  if utils.word_in_str('collection', tc_id):
    C = C.replace('style: UITableViewCellStyle, reuseIdentifier: String?',
                  'frame: CGRect')
    C = C.replace('style: style, reuseIdentifier: reuseIdentifier',
                  'frame: frame')
    C = C.replace('Table', 'Collection')

  return C

def gen_header_header(tc_id, header):
  """
  Args:
    tc_id (str): id of the parent (table/collection)view
    header: (dict) info of header being generated

  Returns (str): swift code for generating the header of a header
  """
  tc_id = utils.uppercase(tc_id)
  C = ("import UIKit\nimport SnapKit\n\nclass {}HeaderView: "
       "UITableViewHeaderFooterView {{\n\n{}"
       "\noverride init(reuseIdentifier: String?) {{\n"
       "super.init(reuseIdentifier: reuseIdentifier)\n"
       "layoutSubviews()\n}}\n\n"
       "override func layoutSubviews() {{"
       "\nsuper.layoutSubviews()\n\n"
      ).format(tc_id, init_g_vars(header.get('components')))

  if utils.word_in_str('collection', tc_id):
    C = C.replace('reuseIdentifier: String?', 'frame: CGRect')
    C = C.replace('reuseIdentifier: reuseIdentifier', 'frame: frame')
    C = C.replace('UITableViewHeaderFooterView', 'UICollectionReusableView')

  return C

def gen_viewcontroller_header(view_controller, info, declare_vars):
  """
  Args:
    view_controller (str): name of viewcontroller
    declare_vars (bool): whether or not to declare global variables.

  Returns (str): swift code of the view controller header
  """
  header = ("import UIKit\nimport SnapKit\n\n"
            "class {}: UIViewController {{\n\n"
           ).format(view_controller)
  header += declare_g_vars(info["components"]) if declare_vars else ""
  header += "\noverride func viewDidLoad() {\nsuper.viewDidLoad()\n"
  return header

def gen_tabbar_vc(view_controller, swift, info):
  """
  Args:
    swift (str): code generated for the tabbar

  Returns (str): code to generate tabbar view controller.
  """
  C = gen_viewcontroller_header(view_controller, info, False)
  C = C.replace(': UIViewController', ': UITabBarController')
  C += ("{}}}\n}}\n").format(swift)
  return C

def move_collection_view(swift, info):
  """
  Returns (str):
    Returns swift code with UICollectionView setup code moved to current file's
    init function.
  """
  C = swift
  beg = C.find('layout.')
  mid = C.find('addSubview', beg)
  end = C.find('\n', mid)
  cv = ("let layout = UICollectionViewFlowLayout()\n"
        "{} = {}(frame: .zero, collectionViewLayout: layout)\n"
        "{}\n"
       ).format(info['tc_elem']['id'], 'UICollectionView', C[beg:end])
  C = C[:beg] + C[end:]

  if 'reuseIdentifier)\n' in C:
    C = utils.ins_after_key(C, 'reuseIdentifier)\n', cv)
  elif 'frame)\n' in C:
    C = utils.ins_after_key(C, 'frame)\n', cv)

  return C

def subclass_tc(swift, info):
  """
  Returns (str): adds necessary (table/collection)view parent classes to swift
  """
  C = swift
  ext = ", UITableViewDelegate, UITableViewDataSource"
  if info["tc_elem"]['type'] == 'UICollectionView':
    ext = ext.replace('Table', 'Collection')
    ext += ", UICollectionViewDelegateFlowLayout"

  if ": UIViewController" in C:
    C = utils.ins_after_key(C, ": UIViewController", ext)
  elif ": UITableViewCell" in C:
    C = utils.ins_after_key(C, ": UITableViewCell", ext)
  elif ": UITableViewHeaderFooterView" in C:
    C = utils.ins_after_key(C, ": UITableViewHeaderFooterView", ext)
  elif ": UICollectionReusableView" in C:
    C = utils.ins_after_key(C, ": UICollectionReusableView", ext)
  elif ": UICollectionViewCell" in C:
    C = utils.ins_after_key(C, ": UICollectionViewCell", ext)
  else:
    raise Exception("Interpreter_h: invalid file in subclass_tc()")

  return C
