import sys
import unittest
from pathlib import Path
from loguru import logger

current_folder = Path(__file__).absolute().parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)
