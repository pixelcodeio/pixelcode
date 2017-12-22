from . import *

class UITabBar(BaseComponent):
  """
  Class representing a UITabBar in swift
  """
  def generate_swift(self):
    return self.setup_component()

  def setup_component(self):
    """
    Returns: (str) swift code to setup uinavbar items
    """
    C = ""
    counter = 0 # counter used to name empty view controllers
    active_index = -1 # index of selected tabbar item
    view_controllers = [] # ids of viewcontrollers in tabbar

    for index, button in enumerate(self.info['tabbar-buttons']):
      if button['active']:
        active_index = index
        vc_name = self.info['active_vc'].lower()
        C += 'let {} = {}()\n'.format(vc_name, self.info['active_vc'])
      else:
        vc_name = 'viewController{}'.format(counter)
        C += 'let {} = UIViewController()\n'.format(vc_name)
        counter += 1

      if button['bg_img'] is None:
        raise Exception("UITabbar: Tabbar button does not contain icon/image.")

      view_controllers.append(vc_name)
      if button.get('text'):
        title = button['text']['textspan'][0]['contents'].decode('utf-8')
        title = ('"{}"').format(title)
      else:
        title = "nil"
      image = 'UIImage(named: "{}")'.format(button['bg_img']['path'])
      item = ('UITabBarItem(title: {}, image: {}, tag: {})'
             ).format(title, image, index)
      C += '{}.tabBarItem = {}\n'.format(vc_name, item)

    C += ("let vcList = [{}]\nviewControllers = vcList\nselectedIndex = {}\n"
         ).format(", ".join(view_controllers), active_index)
    return C
