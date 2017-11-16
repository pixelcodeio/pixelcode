import unittest

class TestStringMethods(unittest.TestCase):

  def filename_helper(self, filename):
    f1 = open("./src/tests/" + filename + ".out", "r+")
    with open("./src/tests/" + filename + ".correct", "r+") as f2:
      for line in f2:
        self.assertEqual(f1.readline(), line)

  def test_images(self):
    self.filename_helper("images")

  def test_text(self):
    self.filename_helper("text")

  def test_rect_borders(self):
    self.filename_helper("rectBorders")

  def test_input(self):
    self.filename_helper("input")

  def test_main(self):
    self.filename_helper("Main")

if __name__ == '__main__':
  unittest.main()
