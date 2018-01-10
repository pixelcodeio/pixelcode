import os
import sys
from zipfile import *
from pixelcode.plugin.parser import Parser
from pixelcode.plugin.interpreter import Interpreter

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
    p = Parser(self.path, self.artboard, True, debug=False)
    p.parse_artboard()

    i = Interpreter(p.globals)
    i.gen_code(p.elements)
    return i.swift

def update_test_dir(path, zip_):
  """
  Generates ".out" files for any files in "./tests"
  """
  print("Directory: " + path)
  files = os.listdir(path)
  svg = []
  for f in files:
    if ".svg" in f and f[0] != ".": # ignore temp files
      svg.append(f.split(".svg")[0])
  for f in svg:
    print("Generating from file: " + f + ".svg")
    m = Main(path, f)
    swift_files = []
    for (filename, code) in m.convert_artboard().items():
      swift_file = filename + ".swift"
      swift_files.append(swift_file)
      o = open(path + swift_file, "w+")
      o.write(code)
      o.close()
    if zip_:
      with ZipFile(path + f + '.zip', 'w', ZIP_DEFLATED) as myzip:
        for swift_file in swift_files:
          myzip.write(path + swift_file)
          os.remove(path + swift_file)

if __name__ == "__main__":
  if len(sys.argv) == 2:
    if sys.argv[1] == 'zip':
      update_test_dir("../exports/", True)
    elif sys.argv[1] == 'staging':
      m = Main("https://s3.amazonaws.com/pixelcode/dev/assets/b94b77403cc4bbaf45ee86bc28173b0a/", "longArtboardView")
      print(m.convert_artboard())
    else:
      update_test_dir(sys.argv[1], False)
  else:
    update_test_dir("../exports/", False)
