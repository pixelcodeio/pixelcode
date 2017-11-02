import interpreter

class UIImageView:
    def __init__(self):
        global i
        i = interpreter.Interpreter()

    def generate_img_view(self, info):
      """
      Returns: The swift code to generate an image view
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
      imgID = info['id']
      imgView = 'var '+ imgID + ' = UIImageView()\n'
      imgView += i.translates_false(imgID)
      imgView += i.set_bg(imgID, r, g, b)
      imgView += i.add_subview('view', imgID)
      imgView += i.wh_constraints(imgID, width, height)
      imgView += i.position_constraints(imgID, horizontalID, horizontalDir,
          horizontalDist, verticalID, verticalDir, verticalDist, centerX, centerY)
      print(imgView)
      return imgView
