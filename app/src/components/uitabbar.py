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
    tint_color = None # color of selected tabbar iitem

    for index, button in enumerate(self.info['tabbar-buttons']):
      if button.get('bg_img') is None:
        raise Exception("UITabbar: Tabbar button does not contain icon/image.")

      if button['active']:
        active_index = index
        vc_name = self.info['active_vc'].lower()
        C += 'let {} = {}()\n'.format(vc_name, self.info['active_vc'])
        if button['bg_img'].get('fill'):
          tint_color = button['bg_img']['fill']
      else:
        vc_name = 'viewController{}'.format(counter)
        C += 'let {} = UIViewController()\n'.format(vc_name)
        counter += 1

      view_controllers.append(vc_name)
      if button.get('text'):
        title = button['text']['textspan'][0]['contents'].decode('utf-8')
        title = ('"{}"').format(title)
      else:
        title = "nil"
      img_name = utils.str_before_key(button['bg_img']['path'], ".")
      image = 'UIImage(named: "{}")'.format(img_name)
      item = ('UITabBarItem(title: {}, image: {}, tag: {})'
             ).format(title, image, index)

      if title == "nil":
        item_name = ("item{}").format(index)
        item = ("let {0} = {1}\n{0}.imageInsets = UIEdgeInsets(top: 6, left: 0"
                ", bottom: -6, right: 0)").format(item_name, item)
        C += "{}\n{}.tabBarItem = {}\n".format(item, vc_name, item_name)
      else:
        C += '{}.tabBarItem = {}\n'.format(vc_name, item)

    C += ("let vcList = [{}]\nviewControllers = vcList\nselectedIndex = {}\n"
         ).format(", ".join(view_controllers), active_index)

    if tint_color:
      C += ("tabBar.tintColor = {}\n").format(utils.create_uicolor(tint_color))

    return C
