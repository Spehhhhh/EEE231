import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)


if __name__ == "__main__":
    # import unittest
    # from tests.test_dgcore_graphapplication import TestDirectedGraphApplication

    # unittest.main()
    # app = DirectedGraphApplication()
    pass
