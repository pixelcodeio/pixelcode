from . import *

class UITableCollectionView(BaseComponent):
  """
  Class representing a UI(Table/Collection)View in swift
    tc_methods: (str) swift code of necessary (table/collection)view methods
  """
  def generate_swift(self):
    keys = ["cells", "header"]
    cells, header = utils.get_vals(keys, self.info)

    m = self.cell_for_row_item(cells)
    m += self.number_in_section(cells)
    m += self.size_for_row_item(cells)

    if header is not None:
      m += self.view_for_header(header)
      m += self.size_for_header(header)

    self.tc_methods = m
    return self.setup_component()

  def gen_comps_ch(self, ch, components, subview_ids):
    """
    Args:
      ch: (str) should either be "cell" or "header"
      components: (dict list) contains info of components
      subview_ids: (str list) contains ids of components

    Returns (str): swift code to generate components inside cell/header
    """
    C = ""
    for j, comp in enumerate(components):
      type_ = comp.get('type')
      if ch == "cell":
        ch_id = "cell.{}".format(subview_ids[j])
      else: # ch == "header"
        ch_id = "header.{}".format(subview_ids[j])

      if type_ == 'UICollectionView':
        continue
      elif type_ == 'UILabel':
        if ch == "cell":
          env = {"set_prop": True, "in_cell": True}
          com = utils.create_component(type_, ch_id, comp, env)
        else: # ch == "header"
          env = {"set_prop": True, "in_header": True}
          com = utils.create_component(type_, ch_id, comp, env)
      else:
        com = utils.create_component(type_, ch_id, comp, {"set_prop": True})
      C += com.swift
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
        ).format(self.id, self.id.capitalize())

    if self.info.get('type') == 'UICollectionView':
      C = C.replace("table", "collection")
      C = C.replace("Table", "Collection")
      C = C.replace("Row", "Item")
      C = C.replace("withIdentifier", "withReuseIdentifier")
      C = C.replace("cell.selectionStyle = .none\n", '')
      C = utils.ins_after_key(C, 'CellID"', ', for: indexPath')

    subview_ids = []
    fst_cell_comps = cells[0].get('components')
    for component in fst_cell_comps:
      subview_ids.append(component.get('id'))

    index = 0
    for cell in cells:
      components = cell.get('components')
      if len(components) != len(fst_cell_comps):
        continue
      C += '\ncase {}:\n'.format(index)
      C += self.gen_comps_ch("cell", components, subview_ids)
      C += 'return cell'
      index += 1

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
      sec = "section"
    else:
      func = ("func collectionView(_ collectionView: UICollectionView,"
              " viewForSupplementaryElementOfKind kind: String, at indexPath: "
              "IndexPath) -> UICollectionReusableView")
      deq = "dequeueReusableSupplementaryView(ofKind: kind, withReuseIdentifier"
      path = ", for: indexPath"
      sec = "indexPath.section"

    C = ('{0} {{\nlet header = {1}.{2}: "{1}Header"{3}) as! {4}HeaderView\n'
         'switch {5} {{\n'
         'case 0:\n'
        ).format(func, self.id, deq, path, self.id.capitalize(), sec)

    components = header.get('components')
    subview_ids = [comp.get('id') for comp in components]
    C += self.gen_comps_ch("header", components, subview_ids)
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
         ' "{0}Header")\n').format(id_, id_.capitalize())

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
    sep = self.info.get('separator')
    if len(sep) > 0:
      C = "layout.minimumInteritemSpacing = {}\n".format(sep[0])
      scroll = ("layout.scrollDirection = .horizontal\n"
                "{}.alwaysBounceHorizontal = true\n").format(self.id)
      if len(sep) == 2:
        scroll = scroll.replace('Horizontal', 'Vertical')
        scroll = scroll.replace('horizontal', 'vertical')
        C += "layout.minimumLineSpacing = {}\n".format(sep[1])
      C += scroll
    return C

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
         ).format(id_, id_.capitalize())

    if self.info.get('type') == 'UICollectionView':
      C = C.replace('CellReuse', 'CellWithReuse')

    return C
