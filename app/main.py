import parser
import interpreter

class Main:
  """
  Takes a SVG file and returns a swift file representing the same code.
  """
  def __init__(self, filepath):
    self.filepath = filepath

  def convert_file():
    p = Parser(self.filepath)
    p.parse_svg()
    i = Interpreter()

    parsed_globals = p.globals

if __name__ == "__main__":
  m = Main("./tests/red_on_white_rect.svg")
