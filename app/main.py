from parser import Parser
from interpreter import Interpreter

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
    for elem in parsed_elements:
      labels.append({"id": elem["id"], "type": elem["type"]})
      print i.generate_rect(elem)

if __name__ == "__main__":
  m = Main("./tests/testrects.svg")
  m.convert_file()
