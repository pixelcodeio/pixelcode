import components.utils as utils
from . import UIView, UIButton, UIImageView, UILabel, UITextField, UITextView

class UITableView(object):
  """
  Class representing a UITableView in swift
  """

  def create_object(self, comp, bgColor=None):
    """
    Args:
      comp: (str) the component to be created

    Returns: An instance of the component to be created
    """
    return {
        "UIButton": UIButton(),
        "UILabel": UILabel(bgColor),
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
    capElem = elem.capitalize()
    c = ("func tableView(_ tableView: UITableView, cellForRowAt "
         "indexPath: IndexPath) -> UITableViewCell {{\n"
         'let cell = tableView.dequeueReusableCell(withIdentifier: "{}CellID")'
         ' as! {}Cell\n'
         'cell.selectionStyle = .none\n'
         "switch indexPath.row {{"
        ).format(elem, capElem)

    cellSubviewIDs = []
    for component in cells[0].get('components'):
      cellSubviewIDs.append(component.get('id'))

    for i, cell in enumerate(cells):
      components = cell.get('components')
      c += '\ncase {}:\n'.format(i)
      for j, component in enumerate(components):
        comp = component.get('type')
        cid = component.get('id')
        obj = self.create_object(comp)
        cellComp = "cell.{}".format(cellSubviewIDs[j])

        if comp == 'UIButton':
          contents = component['text']['textspan'][0]['contents']
          if contents is not None:
            # assuming not varying text
            c += obj.set_title(cellComp, contents)

        elif comp == 'UIImageView':
          path = component.get('path')
          if path is not None:
            c += obj.set_image(cellComp, path)

        elif comp == 'UILabel':
          line_sp = component.get('line-spacing')
          char_sp = component.get('char-spacing')
          textspan = component.get('textspan')
          if line_sp is not None or char_sp is not None:
            c += obj.setup_cell_or_header_attr_text(cellSubviewIDs[j], textspan,
                                                    line_sp, char_sp)
          else:
            contents = component['textspan'][0]['contents']
            if contents is not None:
              c += obj.set_text(cellComp, contents)

        elif comp == 'UITextField' or comp == 'UITextView':
          textspan = component['text']['textspan']
          placeholder = textspan[0]['contents']
          placeholder_c = textspan[0]['fill']
          opacity = textspan[0]['opacity']
          c += obj.set_placeholder_text_and_color(cellComp, placeholder,
                                                  placeholder_c, opacity)
      c += '\nreturn cell'
    c += '\ndefault: return cell\n}\n}\n\n'
    return c

  def number_of_rows_in_section(self, cells):
    """
    Args:
      cells: see generate_component's docstring for more information

    Returns: The swift code for the numberOfRowsInSection func of a UITableView.
    """
    numRows = len(cells)
    return ("func tableView(_ tableView: UITableView, "
            "numberOfRowsInSection section: Int) -> Int {{\n"
            "return {} \n"
            "}}\n"
           ).format(numRows)

  def height_for_row_at(self, elem, cells):
    """
    Args:
      cells: see generate_component's docstring for more information
      tvHeight: (float) height of the uitableview as percentage of screen's
                height

    Returns: The swift code for the heightForRowAt func of a UITableView.
    """
    cellHeightPerc = cells[0]['height']
    return ("func tableView(_ tableView: UITableView, heightForRowAt "
            "indexPath: IndexPath) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(elem, cellHeightPerc)

  def view_for_header(self, elem, header):
    """
    Returns: The swift code for generating the viewForHeaderInSection function
    """
    capElem = elem.capitalize()
    c = ("func tableView(_ tableView: UITableView, viewForHeaderInSection "
         "section: Int) -> UIView? {{\n"
         'let header = {}.dequeueReusableHeaderFooterView(withIdentifier: '
         '"{}Header") as! {}HeaderView\n'
         'switch section {{\n'
         'case 0:\n'
        ).format(elem, elem, capElem)

    components = header.get('components')
    headerSubviewIDs = []
    for component in components:
      headerSubviewIDs.append(component.get('id'))

    for i, component in enumerate(components):
      comp = component.get('type')
      cid = component.get('id')
      obj = self.create_object(comp)
      headerComp = "header.{}".format(headerSubviewIDs[i])

      if comp == 'UIButton':
        contents = component['text']['textspan'][0]['contents']
        if contents is not None:
          # assuming not varying text
          c += obj.set_title(headerComp, contents)

      elif comp == 'UIImageView':
        path = component.get('path')
        if path is not None:
          c += obj.set_image(headerComp, path)

      elif comp == 'UILabel':
        line_sp = component.get('line-spacing')
        char_sp = component.get('char-spacing')
        textspan = component.get('textspan')
        if line_sp is not None or char_sp is not None:
          c += obj.setup_cell_or_header_attr_text(headerSubviewIDs[i], textspan,
                                                  line_sp, char_sp)
        else:
          contents = component['textspan'][0]['contents']
          if contents is not None:
            c += obj.set_text(headerComp, contents)

      elif comp == 'UITextField' or comp == 'UITextView':
        textspan = component['text']['textspan']
        placeholder = textspan[0]['contents']
        placeholder_c = textspan[0]['fill']
        opacity = textspan[0]['opacity']
        c += obj.set_placeholder_text_and_color(headerComp, placeholder,
                                                placeholder_c, opacity)
    c += ('return header'
          '\ndefault:\nreturn header\n'
          '}\n}\n\n'
         )
    return c

  def height_for_header(self, elem, header):
    """
    Returns: The swift code for heightForHeaderInSection function.
    """
    headerHeightPerc = header['height']
    return ("func tableView(_ tableView: UITableView, heightForHeaderInSection "
            "section: Int) -> CGFloat {{\n"
            "return {}.frame.height * {}\n}}\n\n"
           ).format(elem, headerHeightPerc)

  def setup_uitableview(self, elem, cells, header):
    """
    Args:
      elem: (str) id of the component
      cells: see generate_component's docstring for more information
      header: see generate_component's docstring for more information

    Returns: The swift code to setup a UITableView in viewDidLoad.
    """
    capElem = elem.capitalize()
    c = ""
    if header is not None:
      c += ('{}.register({}HeaderView.self, forHeaderFooterViewReuseIdentifier:'
            ' "{}Header")\n'
           ).format(elem, capElem, elem)
    c += ('{}.register({}Cell.self, forCellReuseIdentifier: "{}CellID")\n'
          '{}.delegate = self\n'
          '{}.dataSource = self\n'
         ).format(elem, capElem, elem, elem, elem)
    return c
