import interpreter

class UIView:
    def __init__(self):
        global i
        i = Interpreter()


     def generate_view(self, info):
       """
       Returns: Uses properties from info to generate swift code
       that creates a UIView.
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
       rid = info['id']
       view = 'var '+ rid + ' = UIView()\n'
       view += i.translates_false(rid)
       view += i.set_bg(rid, r, g, b)
       view += i.add_subview('view', rid)
       view += i.wh_constraints(rid, width, height)
       view += i.position_constraints(rid, horizontalID, horizontalDir,
           horizontalDist, verticalID, verticalDir, verticalDist, centerX, centerY)
       print(view)
       return view
