import sys
import threading
import keyboard
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QTimer
from ui.widget import ScriptEaseWidget

def start_hotkey(widget):
    keyboard.add_hotkey(
        "ctrl+shift+a",
        lambda: QTimer.singleShot(0, widget.show_and_focus)
    )
    keyboard.wait()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = ScriptEaseWidget()
    widget.hide()  # start hidden

    hotkey_thread = threading.Thread(
        target=start_hotkey,
        args=(widget,),
        daemon=True
    )
    hotkey_thread.start()

    sys.exit(app.exec_())
