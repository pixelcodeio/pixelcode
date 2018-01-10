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
    self.info["content_swift"] = self.fix_content_swift()
    slider_options = self.info["slider_options"]
    C = ("{} = SliderOptions(frame: .zero, names: [{}], controller: self)\n"
         "view.addSubview(sliderOptions)\n\n{}\n"
        ).format(slider_options["id"], self.get_names(),
                 self.info["options_constraint"])
    C += self.info["content_swift"]
    return C

  def get_names(self):
    """
    Returns (str): The names array containing all the text/paths.
    """
    options = self.info["slider_options"]["options"]
    first_option = options[0]
    names = []
    if first_option.get("text") is not None:
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
    # Add scroll view function
    methods = self.info["content_methods"]
    methods = self.gen_scrollview_funcs() + methods
    # Adjust number of items in section
    num_cells = ("return {}").format(len(slider_options["options"]))
    methods = methods.replace("return 1", num_cells)
    # Adjust case for cellForItemAt
    beg = methods.find("cellForItemAt")
    end = methods.find("func", beg)
    mid = methods[beg:end]
    case = ("switch indexPath.row {{\ncase {}"
           ).format(slider_options["selected_index"])
    mid = mid.replace("switch indexPath.row {\ncase 0", case)
    methods = methods[:beg] + mid + methods[end:]
    # Adjust case for sizeForItemAt
    beg = methods.find("sizeForItemAt")
    end = methods.find("func", beg)
    mid = methods[beg:end]
    case = ("switch indexPath.row {{\ncase (0...{})"
           ).format(len(slider_options["options"]) - 1)
    mid = mid.replace("switch indexPath.row {\ncase 0", case)
    methods = methods[:beg] + mid + methods[end:]
    return methods

  def fix_content_swift(self):
    """
    Returns (str): swift code for content collection view with some additions.
    """
    content_swift = self.info["content_swift"]
    index = content_swift.find("view.addSubview")
    paging = ("{}.isPagingEnabled = true\n").format(self.info["content"]["id"])
    content_swift = content_swift[:index] + paging + content_swift[index:]
    index = content_swift.find("layout.scrollDirection = .horizontal")
    line_spacing = "layout.minimumLineSpacing = 0\n"
    return content_swift[:index] + line_spacing + content_swift[index:]

  def gen_scrollview_funcs(self):
    """
    Returns (str): The scrollViewDidScroll function for scrollbar.
    """
    options = self.info["slider_options"]["options"]
    return ("func scrollViewDidScroll(_ scrollView: UIScrollView) {{\n"
            "sliderOptions.sliderBarLeftConstraint.constant = "
            "scrollView.contentOffset.x / {}\n}}\n\n"
            "func scrollToIndex(index: Int) {{\n"
            "let indexPath = IndexPath(item: index, section: 0)\n"
            "{}.scrollToItem(at: indexPath, at: [], animated: true)\n}}\n\n"
           ).format(len(options), self.info["content"]["id"])
