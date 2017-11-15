import unittest

class TestStringMethods(unittest.TestCase):

  def filename_helper(self, filename):
    f1 = open("./tests/" + filename, "r+")
    with open("./app/tests/" + filename, "r+") as f2:
      for line in f2:
        self.assertEqual(f1.readline(), line)

  def test_images(self):
    self.filename_helper("images.out")

  def test_text(self):
    self.filename_helper("text.out")

  def test_rect_borders(self):
    self.filename_helper("rectBorders.out")

  def test_input(self):
    self.filename_helper("input.out")

  def test_main(self):
    self.filename_helper("Main.out")

if __name__ == '__main__':
  unittest.main()
