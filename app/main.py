import os
import sys
from parser import Parser
from interpreter import Interpreter

class Main(object):
  """
  Takes a SVG file and returns a swift file representing the same code.
  """
  def __init__(self, path, artboard):
    """
    Args:
      path: path to directory
      artboard: artboard name
    """
    self.path = path
    self.artboard = artboard

  def convert_artboard(self):
    p = Parser(self.path, self.artboard)
    p.parse_artboard()

    i = Interpreter(p.globals)
    i.generate_code(p.elements)
    return i.swift

def update_test_dir(path):
  """
  Generates ".out" files for any files in "./tests"
  """
  files = os.listdir(path)
  svg = []
  for f in files:
    if ".svg" in f and f[0] != ".": # ignore temp files
      svg.append(f.split(".svg")[0])
  for f in svg:
    print "Generating from file: " + f + ".svg"
    m = Main(path, f)
    o = open(path + f + ".out", "w+")
    o.write(m.convert_artboard())
    o.close()

if __name__ == "__main__":
  update_test_dir("./exports/")
