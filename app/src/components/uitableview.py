from . import *

class UITableView(BaseComponent):
  """
  Class representing a UITableView in swift
    tv_methods: (str) swift code of the necessary tableview methods
  """
  def generate_swift(self):
    keys = ["cells", "header"]
    cells, header = utils.get_vals(keys, self.info)

    tvm = self.cell_for_row_at(cells)
    tvm += self.number_of_rows_in_section(cells)
    tvm += self.height_for_row_at(cells)

    if header is not None:
      tvm += self.view_for_header(header)
      tvm += self.height_for_header(header)

    self.tv_methods = tvm
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

      if type_ == 'UILabel':
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

  def cell_for_row_at(self, cells):
    """
    Args:
      cells (dict list): contains info on cells

    Returns (str): The swift code for the cellForRowAt
    """
    C = ("func tableView(_ tableView: UITableView, cellForRowAt "
         "indexPath: IndexPath) -> UITableViewCell {{\n"
         'let cell = tableView.dequeueReusableCell(withIdentifier: "{}CellID")'
         ' as! {}Cell\n'
         'cell.selectionStyle = .none\n'
         "switch indexPath.row {{"
        ).format(self.id, self.id.capitalize())

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
      C += '\nreturn cell'
      index += 1

    C += '\ndefault: return cell\n}\n}\n\n'
    return C

  def number_of_rows_in_section(self, cells):
    """
    Args:
      cells (dict list): contains info on cells

    Returns (str): swift code for numberOfRowsInSection
    """
    fst_cell_comps = cells[0].get('components')
    num_rows = 0
    for cell in cells:
      components = cell.get('components')
      if len(components) == len(fst_cell_comps): # all components are present
        num_rows += 1
    return ("func tableView(_ tableView: UITableView, "
            "numberOfRowsInSection section: Int) -> Int {{\n"
            "return {} \n"
            "}}\n"
           ).format(num_rows)

  def height_for_row_at(self, cells):
    """
    Args:
      cells (dict list): contains info on cells

    Returns (str): swift code for heightForRowAt
    """
    return ("func tableView(_ tableView: UITableView, heightForRowAt "
            "indexPath: IndexPath) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(self.id, cells[0]['height'])

  def view_for_header(self, header):
    """
    Args:
      header: (dict) contains info about the header

    Returns: (str) swift code for the viewForHeaderInSection
    """
    C = ("func tableView(_ tableView: UITableView, viewForHeaderInSection "
         "section: Int) -> UIView? {{\n"
         'let header = {}.dequeueReusableHeaderFooterView(withIdentifier: '
         '"{}Header") as! {}HeaderView\n'
         'switch section {{\n'
         'case 0:\n'
        ).format(self.id, self.id, self.id.capitalize())

    components = header.get('components')
    subview_ids = [comp.get('id') for comp in components]
    C += self.gen_comps_ch("header", components, subview_ids)
    C += ('return header'
          '\ndefault:\nreturn header\n'
          '}\n}\n\n'
         )
    return C

  def height_for_header(self, header):
    """
    Args:
      header (dict): contains info about header

    Returns (str): swift code for heightForHeaderInSection
    """
    return ("func tableView(_ tableView: UITableView, heightForHeaderInSection "
            "section: Int) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(self.id, header['height'])

  def setup_component(self):
    """
    Returns: (str) The swift code to setup a UITableView
    """
    C = ""
    header = self.info.get('header')
    id_ = self.id
    if header is not None:
      C += ('{}.register({}HeaderView.self, forHeaderFooterViewReuseIdentifier:'
            ' "{}Header")\n'
           ).format(id_, id_.capitalize(), id_)
    C += ('{}.register({}Cell.self, forCellReuseIdentifier: "{}CellID")\n'
          '{}.delegate = self\n'
          '{}.dataSource = self\n'
         ).format(id_, id_.capitalize(), id_, id_, id_)
    return C
