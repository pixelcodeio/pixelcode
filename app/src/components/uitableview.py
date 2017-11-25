from . import *

class UITableView(BaseComponent):
  """
  Class representing a UITableView in swift
    swift: (str) the swift code to create/set properties of a UITableView
    tv_methods: (str) the swift code of the necessary tableview methods
  """
  def __init__(self, id_, info, in_v=False, set_p=False):
    """
    Returns: A UITableView with the swift attribute set to the generated code
    """
    super(UITableView, self).__init__()
    cells = info.get('cells')
    header = info.get('header')
    tvm = self.cell_for_row_at(id_, cells)
    tvm += self.number_of_rows_in_section(cells)
    tvm += self.height_for_row_at(id_, cells)
    if header is not None:
      tvm += self.view_for_header(id_, header)
      tvm += self.height_for_header(id_, header)
    self.tv_methods = tvm
    self.swift = self.setup_component(id_, info, in_v=in_v)

  def gen_comps_ch(self, ch, components, subview_ids):
    """
    Args:
      ch: (str) should either be "cell" or "header"
      components: (dict list) contains information of all the components
      subview_ids: (str list) contains ids of the components

    Returns:
      (str) The swift code to generate components inside a cell or
      header of a tableview.
    """
    c = ""
    for j, comp in enumerate(components):
      type_ = comp.get('type')
      if ch == "cell":
        ch_id = "cell.{}".format(subview_ids[j])
      elif ch == "header":
        ch_id = "header.{}".format(subview_ids[j])

      if type_ == 'UILabel':
        if ch == "cell":
          com = utils.create_component(type_, ch_id, comp, set_p=True, c=True)
        elif ch == "header":
          com = utils.create_component(type_, ch_id, comp, set_p=True, h=True)
      else:
        com = utils.create_component(type_, ch_id, comp, set_p=True)
      c += com.swift
    return c

  def cell_for_row_at(self, elem, cells):
    """
    Args:
      elem: (str) id of the element
      cells: (dict list) see generate_component's docstring for more information

    Returns: (str) The swift code for the cellForRowAt function of a UITableView
    """
    c = ("func tableView(_ tableView: UITableView, cellForRowAt "
         "indexPath: IndexPath) -> UITableViewCell {{\n"
         'let cell = tableView.dequeueReusableCell(withIdentifier: "{}CellID")'
         ' as! {}Cell\n'
         'cell.selectionStyle = .none\n'
         "switch indexPath.row {{"
        ).format(elem, elem.capitalize())

    subview_ids = []
    fst_cell_comps = cells[0].get('components')
    for component in fst_cell_comps:
      subview_ids.append(component.get('id'))

    index = 0
    for cell in cells:
      components = cell.get('components')
      if len(components) != len(fst_cell_comps):
        continue
      c += '\ncase {}:\n'.format(index)
      c += self.gen_comps_ch("cell", components, subview_ids)
      c += '\nreturn cell'
      index += 1

    c += '\ndefault: return cell\n}\n}\n\n'
    return c

  def number_of_rows_in_section(self, cells):
    """
    Args:
      cells: (dict list) see generate_component's docstring for more information

    Returns:
      (str) The swift code for the numberOfRowsInSection func of a UITableView.
    """
    fst_cell_comps = cells[0].get('components')
    num_rows = 0
    for cell in cells:
      components = cell.get('components')
      if len(components) == len(fst_cell_comps):
        # all components are present
        num_rows += 1
    return ("func tableView(_ tableView: UITableView, "
            "numberOfRowsInSection section: Int) -> Int {{\n"
            "return {} \n"
            "}}\n"
           ).format(num_rows)

  def height_for_row_at(self, elem, cells):
    """
    Args:
      cells: (dict list) see generate_component's docstring for more information
      tvHeight: (float) height of the uitableview as percentage of screen's
                height

    Returns: (str) The swift code for the heightForRowAt func of a UITableView.
    """
    return ("func tableView(_ tableView: UITableView, heightForRowAt "
            "indexPath: IndexPath) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(elem, cells[0]['height'])

  def view_for_header(self, elem, header):
    """
    Args:
      elem: (str) the id of the element
      header: (dict) contains information about the header of a tableview.

    Returns:
      (str) The swift code for generating the viewForHeaderInSection function
    """
    c = ("func tableView(_ tableView: UITableView, viewForHeaderInSection "
         "section: Int) -> UIView? {{\n"
         'let header = {}.dequeueReusableHeaderFooterView(withIdentifier: '
         '"{}Header") as! {}HeaderView\n'
         'switch section {{\n'
         'case 0:\n'
        ).format(elem, elem, elem.capitalize())

    components = header.get('components')
    subview_ids = []
    for component in components:
      subview_ids.append(component.get('id'))
    c += self.gen_comps_ch("header", components, subview_ids)
    c += ('return header'
          '\ndefault:\nreturn header\n'
          '}\n}\n\n'
         )
    return c

  def height_for_header(self, elem, header):
    """
    Args:
      elem: (str) the id of the element
      header: (dict) contains information about the header of a tableview.

    Returns: (str) The swift code for heightForHeaderInSection function.
    """
    return ("func tableView(_ tableView: UITableView, heightForHeaderInSection "
            "section: Int) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(elem, header['height'])

  def setup_component(self, elem, info, in_v=False):
    """
    Args:
      elem: (str) id of the component
      cells: (dict list) see generate_component's docstring for more information
      header: (dict) see generate_component's docstring for more information

    Returns: (str) The swift code to setup a UITableView in viewDidLoad.
    """
    header = info.get('header')
    c = ""
    if header is not None:
      c += ('{}.register({}HeaderView.self, forHeaderFooterViewReuseIdentifier:'
            ' "{}Header")\n'
           ).format(elem, elem.capitalize(), elem)
    c += ('{}.register({}Cell.self, forCellReuseIdentifier: "{}CellID")\n'
          '{}.delegate = self\n'
          '{}.dataSource = self\n'
         ).format(elem, elem.capitalize(), elem, elem, elem)
    return c
