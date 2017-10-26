import parser
import interpreter

"""
Takes a SVG file and returns a swift file representing the same code.
"""
class Main:
  def __init__(self, filepath):
    self.filepath = filepath

  def convert_file():
    p = Parser(self.filepath)
    i = Interpreter()
    result = p.parse_svg()

if __name__ == "__main__":
  m = Main("./tests/red_on_white_rect.svg")
