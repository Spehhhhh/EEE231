import sys
from pathlib import Path

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
current_folder = Path(__file__).absolute().parent.parent
father_folder = str(current_folder.parent)
sys.path.append(father_folder)

from directedgraph.dggui.grapheditorgui import DirectedGraphMainWindow
from threading import Timer

# 循环定时器
class RepeatingTimer(Timer):
    def run(self):
        while not self.finished.is_set():
            self.function(*self.args, **self.kwargs)
            self.finished.wait(self.interval)


t = RepeatingTimer(600.0, DirectedGraphMainWindow().file_save())  # 10分钟运行一次file_save
t.start()
