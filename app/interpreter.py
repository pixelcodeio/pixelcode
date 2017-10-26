class Interpreter:
  """
  Takes output from Parser one at a time and generates swift file
  """
  def __init__(self):
    pass

  def generate_header(self):
    """
    TODO: Fill in arguments necessary to generate any headers
    """
    pass

  def generate_rect(self, info):
    """
    TODO: Fill in arguments necessary to create a rectangle
    """
    vertical = info['vertical']
    horizontal = info['horizontal']
    verticalDir = vertical['direction']
    horizontalDir = horizontal['direction']
    isUp = True
    isLeft = True
    if (verticalDir == 'down'):
        isUp = false
    if (horizontalDir == 'right'):
        isLeft = false
    verticalID = vertical['id']
    verticalDist = str(vertical['distance']) 
    horizontalID = horizontal['id']
    horizontalDist = str(horizontal['distance'])
    centerX = str(info['x'])
    centerY = str(info['y'])
    width = str(info['width'])
    height = str(info['height'])
    fill = info['fill']
    r = str(fill[0])
    g = str(fill[1])
    b = str(fill[2])
    rid = info['id']
    rect = 'var '+ rid + ' = UIView()\n'  
    rect += rid + '.translatesAutoresizingMaskIntoConstraints = false\n'
    rect += rid + '.backgroundColor = UIColor(red: ' + r + ', green: ' + g 
    rect += ', blue: ' + b + ', alpha: 1.0)\n'
    rect += 'view.addSubview(' + rid + ')\n\n'
    rect += rid + '.widthAnchor.constraint(equalToConstant: view.frame.width*' 
    rect += width + ').isActive = true\n' 
    rect += rid + '.heightAnchor.constraint(equalToConstant: view.frame.height*' 
    rect += height + ').isActive = true\n' 
    rect += rid + '.centerXAnchor.constraint(equalTo: view.'
    if isLeft:
        rect += 'left'
    else:
        rect += 'right'
    rect += 'Anchor, constant: view.frame.width*' + centerX + ').isActive = true\n' 
    rect += rid + '.centerYAnchor.constraint(equalTo: view.' 
    if isUp:
        rect += 'top'
    else:
        rect += 'bottom'
    rect += 'Anchor, constant: view.frame.height*' + centerY + ').isActive = true\n' 
    return rect

