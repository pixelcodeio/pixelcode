from . import *

class UITableCollectionView(BaseComponent):
  """
  Class representing a UI(Table/Collection)View in swift
    tc_methods (str): swift code of necessary (table/collection)view methods
    table_separate (bool): whether type is UITableView and cells are separated
  """
  def generate_swift(self):
    methods = self.cell_for_row_item()
    methods += self.number_in_section()
    methods += self.size_for_row_item()
    methods += self.number_of_sections()

    if len(self.info["custom_headers"]) > 0:
      methods += self.view_for_header()
      methods += self.size_for_header()

    self.tc_methods = methods
    return self.setup_component()

  def setup_component(self):
    """
    Returns: (str) The swift code to setup a UITableView
    """
    C = self.gen_spacing()
    C += ('{0}.delegate = self\n'
          '{0}.dataSource = self\n'
          '{0}.showsVerticalScrollIndicator = false\n'
          '{0}.showsHorizontalScrollIndicator = false\n'
          '{0}.clipsToBounds = false\n').format(self.id)
    C += self.register_headers()
    C += self.register_custom_cells()

    if self.info['type'] == 'UICollectionView':
      C = C.replace('CellReuse', 'CellWithReuse')
    else: # type is UITableView
      if self.info["separator"]:
        footer_height = self.info["separator"][0]
      else:
        footer_height = 0
      C += ('{0}.tableHeaderView = UIView(frame: CGRect(x: 0, y: 0, width: 0, '
            'height: 0.01))\n'
            '{0}.sectionHeaderHeight = 0\n'
            '{0}.sectionFooterHeight = {1}\n').format(self.id, footer_height)

    return C

  def cell_for_row_item(self):
    """
    Returns (str): The swift code for the cellFor(Row/Item)At
    """
    C = ('func tableView(_ tableView: UITableView, cellForRowAt '
         'indexPath: IndexPath) -> UITableViewCell {\n')

    if self.info['type'] == 'UICollectionView':
      C = C.replace("table", "collection")
      C = C.replace("Table", "Collection")
      C = C.replace("Row", "Item")

    C += self.info['cell_set_prop']

    if self.info['type'] == 'UICollectionView':
      C = C.replace("withIdentifier", "withReuseIdentifier")
      C = C.replace("cell.selectionStyle = .none\n", '')
      C = utils.ins_after_key(C, 'ID"', ', for: indexPath')

    C += "}\n\n"
    return C

  def number_in_section(self):
    """
    Returns (str): swift code for numberOf(Rows/Items)InSection
    """
    if self.info['type'] == 'UITableView':
      C = "func tableView(_ tableView: UITableView, numberOfRows"
    else:
      C = ("func collectionView(_ collectionView: UICollectionView, "
           "numberOfItems")

    C += ("InSection section: Int) -> Int {\n"
          "switch section {\n")
    for index, section in enumerate(self.info["sections"]):
      C += ("case {}:\n").format(index)
      num_cells = len(section["cells"])
      if section["table_separate"]:
        C += ("return {}\n").format(num_cells * 2 - 1)
      else:
        C += ("return {}\n").format(num_cells)

    C += "default:\nreturn 0\n}\n}\n\n"
    return C

  def size_for_row_item(self):
    """
    Args:
      cells (dict list): contains info on cells

    Returns (str): swift code for heightForRowAt/sizeForItemAt
    """
    if self.info['type'] == 'UITableView':
      C = ("func tableView(_ tableView: UITableView, heightForRowAt "
           "indexPath: IndexPath) -> CGFloat {\n")
    else:
      C = ("func collectionView(_ collectionView: UICollectionView, layout "
           "collectionViewLayout: UICollectionViewLayout, sizeForItemAt "
           "indexPath: IndexPath) -> CGSize {\n")
    C += "switch indexPath.section {\n"

    for section_index, section in enumerate(self.info["sections"]):
      C += ("case {}:\n").format(section_index)
      if section["table_separate"]:
        C += ("if (indexPath.row % 2 == 1) {{\n"
              "return {}\n}}\n").format(section["separator"][0])
      C += "switch indexPath.row {\n"
      for cell_index, cell in enumerate(section["cells"]):
        index = cell_index * 2 if section["table_separate"] else cell_index
        C += ("case {}:\n").format(index)
        width = section["width"] * cell["width"]
        height = section["height"] * cell["height"]
        if self.info["type"] == "UITableView":
          C += ("return {}.frame.height * {}\n").format(self.id, height)
        else:
          C += ("return CGSize(width: {0}.frame.width*{1}, height: {0}.frame."
                "height*{2})\n").format(self.id, width, height)
      C += ("default:\nreturn 0\n}\n")
    C += ("default:\nreturn 0\n}\n}\n\n")

    return C

  def view_for_header(self):
    """
    Args:
      header: (dict) contains info about the header

    Returns: (str) swift code for the viewForHeaderInSection
    """
    if self.info['type'] == 'UITableView':
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
    C += self.info["header_set_prop"]
    C += "}\n\n"

    if self.info['type'] == "UICollectionView":
      C = C.replace("switch section", "switch indexPath.section")
      deq = "dequeueReusableSupplementaryView(ofKind: kind, withReuseIdentifier"
      C = C.replace("dequeueReusableHeaderFooterView(withIdentifier", deq)

    return C

  def size_for_header(self):
    """
    Args:
      header (dict): contains info about header

    Returns (str): swift code for setting size of header
    """
    if self.info["type"] == "UITableView":
      C = ("func tableView(_ tableView: UITableView, heightForHeaderIn"
           "Section section: Int) -> CGFloat {\n")
    else:
      C = ("func collectionView(_ collectionView: UICollectionView, layout "
           "collectionViewLayout: UICollectionViewLayout, referenceSizeFor"
           "HeaderInSection section: Int) -> CGSize {\n")

    C += "switch section {\n"
    for index, section in enumerate(self.info["sections"]):
      if section.get("header") is not None:
        C += ("case {}:\n").format(index)
        width = section["width"] * section["header"]["width"]
        height = section["height"] * section["header"]["height"]
        if self.info["type"] == "UITableView":
          C += ("return {}.frame.height * {}\n").format(self.id, height)
        else:
          C += ("return CGSize(width: {0}.frame.width*{1}, height: {0}.frame."
                "height*{2})\n").format(self.id, width, height)

    C += "default:\nreturn 0\n}\n}\n\n"
    return C

  def register_headers(self):
    """
    Returns (str): Swift code to register headers
    """
    if len(self.info["custom_headers"]) == 0:
      return ""

    header_names = self.info["custom_headers"].keys()
    C = ""
    for name in header_names:
      C += ('{}.register({}.self, forHeaderFooterViewReuseIdentifier: "{}ID")\n'
           ).format(self.id, name, utils.lowercase(name))

    if self.info['type'] == 'UICollectionView':
      for_ = ("forSupplementaryViewOfKind: UICollectionElementKindSectionHeader"
              ", withReuseIdentifier")
      C = C.replace("forHeaderFooterViewReuseIdentifier", for_)

    return C

  def register_custom_cells(self):
    """
    Returns (str): Swift code to register custom cell classes.
    """
    C = ""
    for section in self.info["sections"]:
      for cell_name in section["custom_cells"]:
        C += ('{}.register({}.self, forCellReuseIdentifier: "{}ID")\n'
             ).format(self.id, cell_name, utils.lowercase(cell_name))
    return C

  def gen_spacing(self):
    """
    Returns (str): swift code to set cell spacing
    """
    if self.info['type'] != 'UICollectionView':
      return ""

    C = ""
    sep = self.info['sections'][0]['separator'] # Use separator of first section
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

  def number_of_sections(self):
    """
    Returns (str): swift code to set height of sections for UITableView
    """
    return ("func numberOfSections(in tableView: UITableView) -> Int {{\n"
            "return {}\n}}\n\n").format(len(self.info["sections"]))
