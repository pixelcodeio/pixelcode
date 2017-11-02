import interpreter

class UIButton:
  def __init__(self):
    global i
    i = interpreter.Interpreter()

  def set_title(self, elem, title):
    """
    Returns: The swift code to set title of a button
    """
    return elem + '.setTitle(' + title + ', for: .normal)'

  def set_title_color(self, elem, r, g, b):
    """
    Returns: The swift code to set title color of a button
    """
    color = 'UIColor(red: ' + r ', green: ' + g ', blue: ' + b + ', alpha: 1.0)'
    return elem + '.setTitleColor(' + color + ', for: .normal)'

  def set_font_size(self, elem, size):
    """
    Returns: The swift code to set the font size of a button
    """
    font = 'UIFont.systemFont(ofSize: ' + size + ')'
    return elem + '.titleLabel.font = ' + font

  def generate_button(self, info):
    """
    Returns: The swift code to generate a button 
    """
    vertical = info['vertical']
    horizontal = info['horizontal']
    verticalDir = vertical['direction']
    verticalID = vertical['id']
    verticalDist = vertical['distance']
    horizontalDir = horizontal['direction']
    horizontalID = horizontal['id']
    horizontalDist = horizontal['distance']
    centerX = info['x']
    centerY = info['y']
    width = info['width']
    height = info['height']
    fill = info['fill']
    r = fill[0]
    g = fill[1]
    b = fill[2]
    bid = info['id']
    title = info['title']
    button = 'var '+ bid + ' = UIImageView()\n'
    button += i.translates_false(bid)
    button += self.set_title(bid, title)
    button += i.set_bg(bid, r, g, b)
    button += i.add_subview('view', bid)
    button += i.wh_constraints(bid, width, height)
    button += i.position_constraints(bid, horizontalID, horizontalDir,
      horizontalDist, verticalID, verticalDir, verticalDist, centerX, centerY)
    print(button)
    return button
