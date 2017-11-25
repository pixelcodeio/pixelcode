from . import *

class UITableView(BaseComponent):
  """
  Class representing a UITableView in swift
    swift: (str) the swift code to create/set properties of a UITableView
    tv_methods: (str) the swift code of the necessary tableview methods
  """
  def generate_swift(self):
    cells = self.info.get('cells')
    header = self.info.get('header')
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
      ch: (str) should either be "cell" or "header" # TODO: change to bool
      components: (dict list) contains info of all the components
      subview_ids: (str list) contains ids of the components

    Returns:
      (str) The swift code to generate components inside a cell or
      header of a tableview.
    """
    C = ""
    for j, comp in enumerate(components):
      type_ = comp.get('type')
      if ch == "cell":
        ch_id = "cell.{}".format(subview_ids[j])
      elif ch == "header":
        ch_id = "header.{}".format(subview_ids[j])

      if type_ == 'UILabel':
        if ch == "cell":
          env = {"set_prop": True, "in_cell": True}
          com = utils.create_component(type_, ch_id, comp, env)
        elif ch == "header":
          env = {"set_prop": True, "in_header": True}
          com = utils.create_component(type_, ch_id, comp, env)
      else:
        com = utils.create_component(type_, ch_id, comp, {"set_prop": True})
      C += com.swift
    return C

  def cell_for_row_at(self, cells):
    """
    Args:
      cells: (dict list) see generate_component's docstring for more information

    Returns: (str) The swift code for the cellForRowAt function of a UITableView
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
      cells: (dict list) see generate_component's docstring for more info

    Returns: (str) swift code for numberOfRowsInSection in a UITableView.
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
      cells: (dict list) see generate_component's docstring for more info
      tvHeight: (float) height of the tableview in percent

    Returns: (str) The swift code for the heightForRowAt func of a UITableView.
    """
    return ("func tableView(_ tableView: UITableView, heightForRowAt "
            "indexPath: IndexPath) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(self.id, cells[0]['height'])

  def view_for_header(self, header):
    """
    Args:
      header: (dict) contains information about the header of a tableview.

    Returns: (str) swift code for the viewForHeaderInSection function
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
      header: (dict) contains information about the header of a tableview.

    Returns: (str) The swift code for heightForHeaderInSection function.
    """
    return ("func tableView(_ tableView: UITableView, heightForHeaderInSection "
            "section: Int) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(self.id, header['height'])

  def setup_component(self):
    """
    Returns: (str) The swift code to setup a UITableView in viewDidLoad.
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
