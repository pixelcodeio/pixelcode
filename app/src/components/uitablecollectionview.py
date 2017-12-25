from . import *

class UITableCollectionView(BaseComponent):
  """
  Class representing a UI(Table/Collection)View in swift
    tc_methods (str): swift code of necessary (table/collection)view methods
    tv_separate (bool): whether type is UITableView and cells are separated
  """
  def __init__(self, id_, info, env):
    keys = ["type", "separator"]
    type_, separator = utils.get_vals(keys, info)
    self.tv_separate = (type_ == 'UITableView' and len(separator) == 1)
    super().__init__(id_, info, env)


  def generate_swift(self):
    keys = ["cells", "header"]
    cells, header = utils.get_vals(keys, self.info)

    methods = self.cell_for_row_item(cells)
    methods += self.number_in_section(cells)
    methods += self.size_for_row_item(cells)

    if header is not None or self.tv_separate:
      methods += self.view_for_header(header)
      methods += self.size_for_header(header)

    if self.tv_separate:
      methods += self.number_of_sections(cells)

    self.tc_methods = methods
    return self.setup_component()

  def setup_component(self):
    """
    Returns: (str) The swift code to setup a UITableView
    """
    C = self.gen_spacing()
    header = self.info.get('header')
    id_ = self.id

    if header is not None:
      C += self.reg_header()

    C += ('{0}.register({1}Cell.self, forCellReuseIdentifier: "{0}CellID")\n'
          '{0}.delegate = self\n'
          '{0}.dataSource = self\n'
          '{0}.showsVerticalScrollIndicator = false\n'
          '{0}.showsHorizontalScrollIndicator = false\n'
          '{0}.clipsToBounds = false\n'
          '{0}.sectionHeaderHeight = 0\n'
          '{0}.sectionFooterHeight = 0\n'
         ).format(id_, utils.uppercase(id_))

    if self.info.get('type') == 'UICollectionView':
      C = C.replace('CellReuse', 'CellWithReuse')

    return C

  def cell_for_row_item(self, cells):
    """
    Args:
      cells (dict list): contains info on cells

    Returns (str): The swift code for the cellFor(Row/Item)At
    """
    C = ('func tableView(_ tableView: UITableView, cellForRowAt '
         'indexPath: IndexPath) -> UITableViewCell {{\n'
         'let cell = tableView.dequeueReusableCell(withIdentifier: "{}CellID")'
         ' as! {}Cell\n'
         'cell.selectionStyle = .none\n'
         "switch indexPath.row {{"
        ).format(self.id, utils.uppercase(self.id))

    if self.info['type'] == 'UICollectionView':
      C = C.replace("table", "collection")
      C = C.replace("Table", "Collection")
      C = C.replace("Row", "Item")
      C = C.replace("withIdentifier", "withReuseIdentifier")
      C = C.replace("cell.selectionStyle = .none\n", '')
      C = utils.ins_after_key(C, 'CellID"', ', for: indexPath')
    elif self.tv_separate:
      C = C.replace("indexPath.row", "indexPath.section")

    C += self.info.get('cell_set_prop')
    C += '\ndefault: return cell\n}\n}\n\n'
    return C

  def number_in_section(self, cells):
    """
    Args:
      cells (dict list): contains info on cells

    Returns (str): swift code for numberOf(Rows/Items)InSection
    """
    if self.info.get('type') == 'UITableView':
      func = "func tableView(_ tableView: UITableView, numberOfRows"
    else:
      func = ("func collectionView(_ collectionView: UICollectionView, "
              "numberOfItems")

    if self.tv_separate:
      return ("{}InSection section: Int) -> Int {{\n"
              "return 1 \n"
              "}}\n\n"
             ).format(func)

    num_cells = self.get_number_cells(cells)
    return ("{}InSection section: Int) -> Int {{\n"
            "return {} \n"
            "}}\n\n"
           ).format(func, num_cells)

  def size_for_row_item(self, cells):
    """
    Args:
      cells (dict list): contains info on cells

    Returns (str): swift code for heightForRowAt/sizeForItemAt
    """
    width = cells[0]['rwidth']
    height = cells[0]['rheight']

    if self.info.get('type') == 'UITableView':
      return ("func tableView(_ tableView: UITableView, heightForRowAt "
              "indexPath: IndexPath) -> CGFloat {{\n"
              "return {}\n}}\n\n"
             ).format(width)

    return ("func collectionView(_ collectionView: UICollectionView, layout "
            "collectionViewLayout: UICollectionViewLayout, sizeForItemAt "
            "indexPath: IndexPath) -> CGSize {{\nreturn "
            "CGSize(width: {}, height: {})\n}}\n"
           ).format(width, height)

  def view_for_header(self, header):
    """
    Args:
      header: (dict) contains info about the header

    Returns: (str) swift code for the viewForHeaderInSection
    """
    if self.info.get('type') == 'UITableView':
      func = ("func tableView(_ tableView: UITableView, viewForHeaderInSection "
              "section: Int) -> UIView?")
      deq = "dequeueReusableHeaderFooterView(withIdentifier"
      path = ""
      section = "section"
    else:
      func = ("func collectionView(_ collectionView: UICollectionView,"
              " viewForSupplementaryElementOfKind kind: String, at indexPath: "
              "IndexPath) -> UICollectionReusableView")
      deq = "dequeueReusableSupplementaryView(ofKind: kind, withReuseIdentifier"
      path = ", for: indexPath"
      section = "indexPath.section"

    C = ("{} {{\n").format(func)
    if header is not None:
      C += ('let header = {0}.{1}: "{0}Header"{2}) as! {3}HeaderView\n'
            'switch {4} {{\n'
           ).format(self.id, deq, path, utils.uppercase(self.id), section)

      C += self.info.get('header_set_prop')
      C += ('return header'
            '\ndefault:\n')

    if self.tv_separate:
      C += ("let view = UIView()\n"
            "view.backgroundColor = .clear\n"
            "return view\n")
    else:
      C += "return header\n"

    C += '}\n\n' if header is None else '}\n}\n\n'
    return C

  def size_for_header(self, header):
    """
    Args:
      header (dict): contains info about header

    Returns (str): swift code for setting size of header
    """
    if header is not None:
      width = header['rwidth']
      height = header['rheight']

    if self.info['type'] == 'UITableView':
      if header is None: # means tv_separate is True
        body = ("return {}\n").format(self.info["separator"][0])
      else:
        body = ("return {}\n").format(height)
        if self.tv_separate:
          body = ("switch section {{\n"
                  "case 0:\n{}\n"
                  "default:\nreturn {}\n}}"
                 ).format(body, self.info['separator'][0])
      return ("func tableView(_ tableView: UITableView, heightForHeaderIn"
              "Section section: Int) -> CGFloat {{\n"
              "{}}}\n\n").format(body)

    return ("func collectionView(_ collectionView: UICollectionView, layout "
            "collectionViewLayout: UICollectionViewLayout, referenceSizeFor"
            "HeaderInSection section: Int) -> CGSize {{\n"
            "return CGSize(width: {}, height: {})\n}}\n").format(width, height)

  def reg_header(self):
    """
    Returns (str): swift code to register header view class
    """
    id_ = self.id
    type_ = self.info.get('type')
    C = ('{0}.register({1}HeaderView.self, forHeaderFooterViewReuseIdentifier:'
         ' "{0}Header")\n').format(id_, utils.uppercase(id_))

    if type_ == 'UICollectionView':
      ins = ("forSupplementaryViewOfKind: UICollectionElementKindSectionHeader,"
             " withReuseIdentifier")
      C = C.replace("forHeaderFooterViewReuseIdentifier", ins)

    return C

  def gen_spacing(self):
    """
    Returns (str): swift code to set cell spacing
    """
    if self.info.get('type') != 'UICollectionView':
      return ""

    C = ""
    sep = self.info['separator']
    if sep:
      C = "layout.minimumInteritemSpacing = {}\n".format(sep[0])
      scroll = ("layout.scrollDirection = .horizontal\n"
                "{}.alwaysBounceHorizontal = true\n").format(self.id)
      if len(sep) == 2:
        scroll = scroll.replace('Horizontal', 'Vertical')
        scroll = scroll.replace('horizontal', 'vertical')
        C += "layout.minimumLineSpacing = {}\n".format(sep[1])
      C += scroll
    return C

  def number_of_sections(self, cells):
    """
    Returns (str): swift code to set height of sections for UITableView
    """
    return ("func numberOfSections(in tableView: UITableView) -> Int {{\n"
            "return {}\n}}\n").format(self.get_number_cells(cells))

  def get_number_cells(self, cells):
    """
    Returns (int): number of cells
    """
    fst_cell_comps = cells[0]['components']
    num_cells = 0
    for cell in cells:
      components = cell['components']
      if len(components) == len(fst_cell_comps): # all components are present
        num_cells += 1
    return num_cells
