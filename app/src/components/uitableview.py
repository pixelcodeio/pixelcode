import components.utils as utils
from . import UIView, UIButton, UIImageView, UILabel, UITextField, UITextView

class UITableView(object):
  """
  Class representing a UITableView in swift
  """

  def create_object(self, comp, bgc=None):
    """
    Args:
      comp: (str) the component to be created

    Returns: An instance of the component to be created
    """
    return {
        "UIButton": UIButton(),
        "UILabel": UILabel(bgc),
        "UIImageView": UIImageView(),
        "UITableView": UITableView(),
        "UITextField": UITextField(),
        "UITextView": UITextView(),
        "UIView": UIView(),
    }.get(comp, None)

  def cell_for_row_at(self, elem, cells):
    """
    Args:
      cells: see generate_component's docstring for more information

    Returns: The swift code for the cellForRowAt function of a UITableView.
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
      for j, component in enumerate(components):
        comp = component.get('type')
        cid = component.get('id')
        obj = self.create_object(comp)
        cell_comp = "cell.{}".format(subview_ids[j])

        if comp == 'UIButton':
          contents = component['text']['textspan'][0]['contents']
          if contents is not None:
            # assuming not varying text
            c += obj.set_title(cell_comp, contents)

        elif comp == 'UIImageView':
          path = component.get('path')
          if path is not None:
            c += obj.set_image(cell_comp, path)

        elif comp == 'UILabel':
          line_sp = component.get('line-spacing')
          char_sp = component.get('char-spacing')
          textspan = component.get('textspan')
          if line_sp is not None or char_sp is not None:
            c += obj.setup_cell_or_header_attr_text(subview_ids[j], textspan,
                                                    line_sp, char_sp)
          else:
            contents = component['textspan'][0]['contents']
            if contents is not None:
              c += obj.set_text(cell_comp, contents)

        elif comp == 'UITextField' or comp == 'UITextView':
          textspan = component['text']['textspan']
          placeholder = textspan[0]['contents']
          placeholder_c = textspan[0]['fill']
          c += obj.set_placeholder_text_and_color(cell_comp, placeholder,
                                                  placeholder_c)
      c += '\nreturn cell'
      index += 1

    c += '\ndefault: return cell\n}\n}\n\n'
    return c

  def number_of_rows_in_section(self, cells):
    """
    Args:
      cells: see generate_component's docstring for more information

    Returns: The swift code for the numberOfRowsInSection func of a UITableView.
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
      cells: see generate_component's docstring for more information
      tvHeight: (float) height of the uitableview as percentage of screen's
                height

    Returns: The swift code for the heightForRowAt func of a UITableView.
    """
    return ("func tableView(_ tableView: UITableView, heightForRowAt "
            "indexPath: IndexPath) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(elem, cells[0]['height'])

  def view_for_header(self, elem, header):
    """
    Returns: The swift code for generating the viewForHeaderInSection function
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

    for i, component in enumerate(components):
      comp = component.get('type')
      cid = component.get('id')
      obj = self.create_object(comp)
      header_comp = "header.{}".format(subview_ids[i])

      if comp == 'UIButton':
        contents = component['text']['textspan'][0]['contents']
        if contents is not None:
          # assuming not varying text
          c += obj.set_title(header_comp, contents)

      elif comp == 'UIImageView':
        path = component.get('path')
        if path is not None:
          c += obj.set_image(header_comp, path)

      elif comp == 'UILabel':
        line_sp = component.get('line-spacing')
        char_sp = component.get('char-spacing')
        textspan = component.get('textspan')
        if line_sp is not None or char_sp is not None:
          c += obj.setup_cell_or_header_attr_text(subview_ids[i], textspan,
                                                  line_sp, char_sp)
        else:
          contents = component['textspan'][0]['contents']
          if contents is not None:
            c += obj.set_text(header_comp, contents)

      elif comp == 'UITextField' or comp == 'UITextView':
        textspan = component['text']['textspan']
        placeholder = textspan[0]['contents']
        placeholder_c = textspan[0]['fill']
        c += obj.set_placeholder_text_and_color(header_comp, placeholder,
                                                placeholder_c)
    c += ('return header'
          '\ndefault:\nreturn header\n'
          '}\n}\n\n'
         )
    return c

  def height_for_header(self, elem, header):
    """
    Returns: The swift code for heightForHeaderInSection function.
    """
    return ("func tableView(_ tableView: UITableView, heightForHeaderInSection "
            "section: Int) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(elem, header['height'])

  def setup_uitableview(self, elem, cells, header):
    """
    Args:
      elem: (str) id of the component
      cells: see generate_component's docstring for more information
      header: see generate_component's docstring for more information

    Returns: The swift code to setup a UITableView in viewDidLoad.
    """
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
