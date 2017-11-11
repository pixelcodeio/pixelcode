import unittest

class TestStringMethods(unittest.TestCase):

  def filename_helper(self, filename):
    f1 = open("./tests/" + filename, "r+")
    f2 = open("./app/tests/" + filename, "r+")
    self.assertEqual(f1.read(), f2.read())

  def test_images(self):
    self.filename_helper("images.out")

  def test_text(self):
    self.filename_helper("text.out")

  def test_rect_borders(self):
    self.filename_helper("rectBorders.out")

  def test_input(self):
    self.filename_helper("input.out")

if __name__ == '__main__':
  unittest.main()
