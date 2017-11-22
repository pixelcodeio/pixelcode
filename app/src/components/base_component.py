import utils
from . import *

class BaseComponent(object):
  """
  Base class for components
  """

  def create_component(self, typ, bgc=None):
    """
    Args:
      typ: (str) the type of the component to be created

    Returns: (obj) An instance of the component to be created
    """
    return {
        "UIButton": UIButton(),
        "UILabel": UILabel(bgc),
        "UIImageView": UIImageView(),
        "UITableView": UITableView(),
        "UITextField": UITextField(),
        "UITextView": UITextView(),
        "UIView": UIView(),
    }.get(typ, None)
