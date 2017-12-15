from . import *

class UITableCollectionView(BaseComponent):
  """
  Class representing a UI(Table/Collection)View in swift
    tc_methods: (str) swift code of necessary (table/collection)view methods
  """
  def generate_swift(self):
    keys = ["cells", "header"]
    cells, header = utils.get_vals(keys, self.info)

    methods = self.cell_for_row_item(cells)
    methods += self.number_in_section(cells)
    methods += self.size_for_row_item(cells)

    if header is not None:
      methods += self.view_for_header(header)
      methods += self.size_for_header(header)

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

    if self.info.get('type') == 'UICollectionView':
      C = C.replace("table", "collection")
      C = C.replace("Table", "Collection")
      C = C.replace("Row", "Item")
      C = C.replace("withIdentifier", "withReuseIdentifier")
      C = C.replace("cell.selectionStyle = .none\n", '')
      C = utils.ins_after_key(C, 'CellID"', ', for: indexPath')

    C += self.info.get('cell_set_prop')
    C += '\ndefault: return cell\n}\n}\n\n'
    return C

  def number_in_section(self, cells):
    """
    Args:
      cells (dict list): contains info on cells

    Returns (str): swift code for numberOf(Rows/Items)InSection
    """
    fst_cell_comps = cells[0].get('components')
    num_rows = 0
    for cell in cells:
      components = cell.get('components')
      if len(components) == len(fst_cell_comps): # all components are present
        num_rows += 1

    if self.info.get('type') == 'UITableView':
      func = "func tableView(_ tableView: UITableView, numberOfRows"
    else:
      func = ("func collectionView(_ collectionView: UICollectionView, "
              "numberOfItems")

    return ("{}InSection section: Int) -> Int {{\n"
            "return {} \n"
            "}}\n"
           ).format(func, num_rows)

  def size_for_row_item(self, cells):
    """
    Args:
      cells (dict list): contains info on cells

    Returns (str): swift code for heightForRowAt/sizeForItemAt
    """
    width = cells[0].get('width')
    height = cells[0].get('height')

    if self.info.get('type') == 'UITableView':
      return ("func tableView(_ tableView: UITableView, heightForRowAt "
              "indexPath: IndexPath) -> CGFloat {{\n"
              "return {}.frame.height * {}\n}}\n\n"
             ).format(self.id, height)

    return ("func collectionView(_ collectionView: UICollectionView, layout "
            "collectionViewLayout: UICollectionViewLayout, sizeForItemAt "
            "indexPath: IndexPath) -> CGSize {{\nreturn "
            "CGSize(width: {0}.frame.width*{1}, height: {0}.frame.height*{2}"
            ")\n}}\n"
           ).format(self.id, width, height)

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

    C = ('{0} {{\nlet header = {1}.{2}: "{1}Header"{3}) as! {4}HeaderView\n'
         'switch {5} {{\n'
        ).format(func, self.id, deq, path, utils.uppercase(self.id), section)

    C += self.info.get('header_set_prop')
    C += ('return header'
          '\ndefault:\nreturn header\n'
          '}\n}\n\n')
    return C

  def size_for_header(self, header):
    """
    Args:
      header (dict): contains info about header

    Returns (str): swift code for setting size of header
    """
    width = header.get('width')
    height = header.get('height')

    if self.info.get('type') == 'UITableView':
      return ("func tableView(_ tableView: UITableView, heightForHeaderIn"
              "Section section: Int) -> CGFloat {{\n"
              "return {}.frame.height * {}\n}}\n\n"
             ).format(self.id, height)

    return ("func collectionView(_ collectionView: UICollectionView, layout "
            "collectionViewLayout: UICollectionViewLayout, referenceSizeFor"
            "HeaderInSection section: Int) -> CGSize {{\n"
            "return CGSize(width: {0}.frame.width*{1}, height: {0}.frame."
            "height*{2})\n}}\n"
           ).format(self.id, width, height)

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
