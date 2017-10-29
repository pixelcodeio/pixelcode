from parser import Parser
from interpreter import Interpreter
import os, sys

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

def update_test_dir():
  path = "./tests/"
  files = os.listdir(path)
  svg = []
  out = []
  for f in files:
    if ".svg" in f:
      svg.append(f.split(".svg")[0])
    else:
      out.append(f.split(".out")[0])
  for f in svg:
    if f not in out:
      m = Main(path + f + ".svg")
      o = open(path + f + ".out", "w+")
      o.write(m.convert_file())
      o.close()

if __name__ == "__main__":
  if len(sys.argv) == 2 and sys.argv[1] == "update":
    update_test_dir()
  m = Main("./tests/testrects.svg")
  m.convert_file()
