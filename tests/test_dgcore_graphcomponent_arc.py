import sys
from pathlib import Path

CURRENT_FOLDER = Path(__file__).absolute().parent.parent
CURRENT_FOLDER_PATH = str(CURRENT_FOLDER)
sys.path.append(CURRENT_FOLDER_PATH)
