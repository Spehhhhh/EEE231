import unittest
from Code1 import NodeItem
from PySide6.QtGui import QColor


class Test_NodeItem(unittest.TestCase):
    def setUp(self):
        self.qcolor = QColor(0, 170, 243)
        self.node_item = NodeItem(250,250,self.qcolor)
    def tearDown(self):
        pass

    def test_init(self):
        text = "Test Node"
        self.assertEqual(self.node_item.x, 250)
        self.assertEqual(self.node_item.y, 250)

if __name__ == "__main__":
     unittest.main()


