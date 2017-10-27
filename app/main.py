from parser import Parser
from interpreter import Interpreter
import os

class Main:
  """
  Takes a SVG file and returns a swift file representing the same code.
  """
  def __init__(self, filepath):
    self.filepath = filepath

  def convert_file(self):
    p = Parser(self.filepath)
    p.parse_svg()
    i = Interpreter()

    parsed_globals = p.globals
    parsed_elements = p.elements

    labels = []
    ret = ""
    for elem in parsed_elements:
      labels.append({"id": elem["id"], "type": elem["type"]})
      ret += i.generate_rect(elem)
    return ret

if __name__ == "__main__":
  files = os.listdir("./tests")
  svg = []
  out = []
  for f in files:
    if ".svg" in f:
      svg.append(f.split(".svg")[0])
    else:
      out.append(f.split(".out")[0])
  for f in svg:
    if f not in out:
      m = Main("./tests/" + f + ".svg")
      o = open("./tests/" + f + ".out", "w+")
      o.write(m.convert_file())
      o.close()
