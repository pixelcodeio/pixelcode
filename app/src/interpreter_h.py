import utils

def init_g_var(comp):
  """
  Returns: swift code to generate/init one component.
  """
  if comp['type'] == 'UICollectionView': # do not init collection views
    return "var {}: UICollectionView!\n".format(comp['id'])
  elif comp['type'] == 'UINavBar': # cannot init navigation bars
    return ""
  else:
    return "var {} = {}()\n".format(comp['id'], comp['type'])

def init_g_vars(components):
  """
  Args:
    components: (dict list) contains info about components

  Returns (str): swift code to generate/init all glob vars of components
  """
  return "".join([init_g_var(c) for c in components])

def declare_g_vars(components):
  """
  Returns (str): swift code to declare global variables
  """
  navbar_items = [c.get("navbar-items") for c in components \
                  if c.get("navbar-items")]
  if navbar_items:
    if len(navbar_items) > 1:
      raise Exception("Interpreter_h: More than one navbar is present.")
    navbar_items = navbar_items[0] # only one nav bar per screen
    components.extend(navbar_items['left-buttons'])
    components.extend(navbar_items['right-buttons'])
    if navbar_items.get('title') is not None:
      components.append(navbar_items['title'])
      if navbar_items['title'].get('components') is not None:
        components.extend(navbar_items['title']['components'])

  # filter components to not include navigation bar
  ignore_comps = {'UINavBar', 'UIActionSheet'}
  filter_comps = [c for c in components if c['type'] not in ignore_comps]

  # one-liner to concat all variable names
  gvars = ["var {}: {}!\n".format(e['id'], e['type']) for e in filter_comps]
  return "".join(gvars)

def gen_global_colors(global_fills, swift):
  """
  Returns (dict): Updated dictionary of all generated files using global colors
  """
  C = ("import UIKit\n\nextension UIColor {\n\n")
  colors = [utils.create_uicolor(f) for f in global_fills]
  counter = 0
  for (filename, code) in swift.items():
    for color in colors:
      color_name = ("color{}").format(counter)
      code = code.replace(color, "UIColor." + color_name)
      C += "@nonobjc static let {}: UIColor = {}\n".format(color_name, color)
      counter += 1
    swift[filename] = code
  swift["UIColorExtension"] = C + "}\n"
  return swift

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

def gen_header_header(tc_id, header): # TODO: Rename this function.
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
  beg = swift.find('layout.')
  mid = swift.find('addSubview', beg)
  end = swift.find('\n', mid)
  cv = ("let layout = UICollectionViewFlowLayout()\n"
        "{} = {}(frame: .zero, collectionViewLayout: layout)\n"
        "{}\n"
       ).format(info['tc_elem']['id'], 'UICollectionView', swift[beg:end])
  swift = swift[:beg] + swift[end:]

  if 'reuseIdentifier)\n' in swift:
    swift = utils.ins_after_key(swift, 'reuseIdentifier)\n', cv)
  elif 'frame)\n' in swift:
    swift = utils.ins_after_key(swift, 'frame)\n', cv)

  return swift

def move_action_sheet(swift):
  """
  Returns (str):
    Returns swift code with UIActionSheet setup code moved to current file's
    viewDidAppear function.
  """
  beg = swift.find('let alertController')
  end = swift.find('completion: nil)\n', beg) + 17
  swift += ("\noverride func viewDidAppear(_ animated: Bool) {{\n"
            "{}\n}}\n").format(swift[beg:end])
  swift = swift[:beg] + swift[end:]
  return swift

def subclass_tc(swift, info):
  """
  Returns (str): adds necessary (table/collection)view parent classes to swift
  """
  ext = ", UITableViewDelegate, UITableViewDataSource"
  if info["tc_elem"]['type'] == 'UICollectionView':
    ext = ext.replace('Table', 'Collection')
    ext += ", UICollectionViewDelegateFlowLayout"

  if ": UIViewController" in swift:
    swift = utils.ins_after_key(swift, ": UIViewController", ext)
  elif ": UITableViewCell" in swift:
    swift = utils.ins_after_key(swift, ": UITableViewCell", ext)
  elif ": UITableViewHeaderFooterView" in swift:
    swift = utils.ins_after_key(swift, ": UITableViewHeaderFooterView", ext)
  elif ": UICollectionReusableView" in swift:
    swift = utils.ins_after_key(swift, ": UICollectionReusableView", ext)
  elif ": UICollectionViewCell" in swift:
    swift = utils.ins_after_key(swift, ": UICollectionViewCell", ext)
  else:
    raise Exception("Interpreter_h: invalid file in subclass_tc()")

  return swift

def gen_inset_label():
  """
  Returns (str): swift code of our custom UILabel
  """
  return ("import UIKit\n\n"
          "class InsetLabel: UILabel {\n"
          "let topInset = CGFloat(-10)\n"
          "let bottomInset = CGFloat(-10)\n"
          "let leftInset = CGFloat(0)\n"
          "let rightInset = CGFloat(0)\n\n"
          "override func drawText(in rect: CGRect) {\n"
          "let insets: UIEdgeInsets = UIEdgeInsets(top: topInset, left: "
          "leftInset, bottom: bottomInset, right: rightInset)\n"
          "super.drawText(in: UIEdgeInsetsInsetRect(rect, insets))\n"
          "}\n\n"
          "override public var intrinsicContentSize: CGSize {\n"
          "var intrinsicSuperViewContentSize = super.intrinsicContentSize\n"
          "intrinsicSuperViewContentSize.height += topInset + bottomInset\n"
          "intrinsicSuperViewContentSize.width += leftInset + rightInset\n"
          "return intrinsicSuperViewContentSize\n"
          "}\n"
          "}\n")
