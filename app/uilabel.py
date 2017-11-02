import interpreter

class UILabel:
    def __init__(self):
        global i
        i = interpreter.Interpreter()

    def set_text(self, elem, txt):
        return elem + '.text = ' + txt

    def set_font(self, elem, fontSize):
        size = str(fontSize)
        return elem + '.font = UIFont.systemFont(ofSize: ' + size + ')'

    def generate_text(self, info):
      """
      Returns: The swift code to generate a label with a text
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
      lid = info['id']
      txt = info['text']
      fontSize = info['fontSize']
      label = 'var '+ lid + ' = UILabel()\n'
      label += i.translates_false(lid)
      label += self.set_text(lid, txt)
      label += self.set_font(lid, fontSize)
      label += i.set_bg(lid, r, g, b)
      label += i.add_subview('view', lid)
      label += i.wh_constraints(lid, width, height)
      label += i.position_constraints(lid, horizontalID, horizontalDir,
          horizontalDist, verticalID, verticalDir, verticalDist, centerX, centerY)
      print(label)
      return label
