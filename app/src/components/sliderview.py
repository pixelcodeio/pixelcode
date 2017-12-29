from . import *

class SliderView(BaseComponent):
  """
  Class representing a SliderView in swift
  """
  def generate_swift(self):
    return self.setup_component()

  def setup_component(self):
    """
    Returns: swift code to setup SliderView.
    """
    slider_options = self.info["slider_options"]
    C = ("let {} = SliderOptions(frame: .zero, names: [{}])\n"
         "view.addSubview(sliderOptions)\n\n"
         "sliderOptions.snp.updateConstraints{{ make in\n"
         "make.center.equalToSuperview()\n"
         "make.size.equalTo(CGSize(width: {}, height: {}))\n"
         "}}\n\n"
        ).format(slider_options["id"], self.get_names(), slider_options["rwidth"],
                 slider_options["rheight"])
    C += self.info["content_cv_swift"]
    #print(self.info["content_cv_swift"])
    #print(self.info["content_cv_methods"])
    print(C)
    print(self.info["content_cv_methods"])
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
