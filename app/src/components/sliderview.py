from . import *

class SliderView(BaseComponent):
  """
  Class representing a SliderView in swift
    - content_methods (str): swift code of content collection view methods
  """
  def __init__(self, id_, info, env):
    self.content_methods = ""
    super().__init__(id_, info, env)

  def generate_swift(self):
    return self.setup_component()

  def setup_component(self):
    """
    Returns: swift code to setup SliderView.
    """
    self.content_methods = self.fix_content_methods()
    slider_options = self.info["slider_options"]
    C = ("let {} = SliderOptions(frame: .zero, names: [{}])\n"
         "view.addSubview(sliderOptions)\n\n"
         "sliderOptions.snp.updateConstraints{{ make in\n"
         "make.center.equalToSuperview()\n"
         "make.size.equalTo(CGSize(width: {}, height: {}))\n"
         "}}\n\n"
        ).format(slider_options["id"], self.get_names(),
                 slider_options["rwidth"], slider_options["rheight"])
    C += self.info["content_swift"]
    return C

  def get_names(self):
    """
    Returns (str): The names array containing all the text/paths.
    """
    options = self.info["slider_options"]["options"]
    option = options[0]
    names = []
    if option.get("text") is not None:
      for option in options:
        text = option["text"]["textspan"][0]["contents"].decode('utf-8')
        text = ('"{}"').format(text)
        names.append(text)
    else: # option["img"] is not None
      for option in options:
        path = utils.str_before_key(option["img"]["path"], ".")
        names.append(path)
    return ", ".join(names)

  def fix_content_methods(self):
    """
    Returns (str): Methods for content collection view with correct values.
    """
    slider_options = self.info["slider_options"]
    content_methods = self.info["content_methods"]
    num_cells = ("return {}").format(len(slider_options["options"]))
    content_methods = content_methods.replace("return 1", num_cells)
    case_number = ("case {}").format(slider_options["selected_index"])
    content_methods = content_methods.replace("case 0", case_number)
    return content_methods
