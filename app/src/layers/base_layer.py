import utils

class BaseLayer(object):
  """
  Base class for layers
  """
  def __init__(self, elem, type_):
    """
    Args:
      elem (dict): represents a high-level layer of from sketch to be parsed.
      type_ (str): type of elem to set
    """
    elem["type"] = type_
    self.elem = self.parse_elem(elem)

  def init_optional_params(self, elem, params):
    """
    Returns: elem with params initialized to None, except for fill
    """
    for param in params:
      if param == "fill":
        if "fill" in elem.attrs and elem["fill"] != "none" and \
        elem["fill"][0] == '#':
          elem["fill"] = utils.convert_hex_to_rgb(elem["fill"])
        else:
          elem["fill"] = None
      elif param == "filter":
        if "filter" in elem.attrs and elem["filter"] != "none":
          elem["filter"] = elem["filter"][5:-1] # format is url(#[id])
        else:
          elem["filter"] = None
      elif param == "font-family":
        if "font-family" in elem.attrs:
          elem["font-family"] = elem["font-family"].split(",")[0]
      elif param == "opacity":
        if "fill-opacity" in elem.attrs and "opacity" in elem.attrs:
          elem["opacity"] = float(elem["opacity"]) * float(elem["fill-opacity"])
        elif "fill-opacity" in elem.attrs:
          elem["opacity"] = elem["fill-opacity"]
        elif "opacity" in elem.attrs:
          elem["opacity"] = elem["opacity"]
      elif param == "text-align":
        if "text_align" in elem.attrs:
          elem["text-align"] = elem["text_align"]
      elif param == "contents" and "contents" in elem.attrs:
        elem["contents"] = elem["contents"].encode('utf-8')
      elif param == "id" and "param" in elem.attrs:
        elem["id"] = elem["id"].replace("-", "")

      if param not in elem.attrs:
        elem[param] = None

    if elem["fill"] is not None:
      o = "1.0" if elem["opacity"] is None else elem["opacity"]
      elem["fill"] += (o,) # concat tuple
    if elem["stroke-color"] is not None:
      o = "1.0" if elem["stroke-opacity"] is None else elem["stroke-opacity"]
      elem["stroke-color"] += (o,) # concat tuple
    return elem

  def generate_object(self, elem):
    """
    Args:
      elem (dict): represents a high-level layer of from sketch to be parsed.

    Returns: object to be sent to the interpreter class
    """
    params = [
        "abs_x",
        "abs_y",
        "actions",
        "bg_img",
        "bookmark-icon",
        "border-radius",
        "cells",
        "char-spacing",
        "components",
        "content", # content of a SliderView
        "contents", # text of a label
        "cx",
        "cy",
        "fill",
        "filter",
        "font-family",
        "font-size",
        "header",
        "height",
        "horizontal",
        "id",
        "img",
        "img_fill",
        "items",
        "left-inset",
        "line-spacing",
        "navbar-items",
        "opacity",
        "options",
        "path",
        "progress_fill",
        "rect",
        "rwidth", # width in pixels
        "rheight", # height in pixels
        "search-icon",
        "sections",
        "selected_index",
        "separator",
        "slider_options",
        "stroke-color",
        "stroke-width",
        "stroke-opacity",
        "tabbar-buttons",
        "text",
        "textspan",
        "text-align",
        "thumb_fill",
        "tint_fill",
        "title",
        "title_fill",
        "type",
        "vertical",
        "width",
        "x",
        "y",
    ]
    elem = self.init_optional_params(elem, params)
    obj = {}
    for param in params:
      if elem[param] is not None:
        obj[param] = elem[param]
    return obj

  def parse_elem(self, elem):
    """
    Args:
      elem (dict): represents a high-level layer of from sketch to be parsed.

    Returns: object to be sent to the interpreter class
    """
    return self.generate_object(elem)
