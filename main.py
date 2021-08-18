import sys
import time
import os

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *

import brightestSpot
import cameraControll

NUMBER_SECONDS_TO_WAIT = 0


class WindowApp:
    # QT INIT
    app = QApplication([])
    ui_file = QFile('form_main.ui')
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()
    window = loader.load(ui_file)
    button = window.Button_1
    label = window.Label_1
    label_summ = window.Label_summary
    image_label = window.Label_image
    combo_sh = window.comboBox_sh

    def button_click(self):
        is_fatal = False
        start_time = time.time()
        while (time.time() - start_time) <= NUMBER_SECONDS_TO_WAIT:
            time.sleep(0.3)
            self.button.setEnabled(False)
            print(NUMBER_SECONDS_TO_WAIT - (time.time() - start_time))
            self.label.setText(str(round(NUMBER_SECONDS_TO_WAIT - (time.time() - start_time))))
            self.app.processEvents()
        self.button.setEnabled(True)
        sh_from_combo = self.combo_sh.currentText()

        image_src = cameraControll.capture_image(sh_from_combo, "200")
        image_marked, is_fatal = brightestSpot.mark_brightest_spots(image_src)
        new_pixmap = QPixmap(image_marked)
        self.image_label.setPixmap(new_pixmap)
        if is_fatal:
            self.label_summ.setText("Test NOT OK")
        else:
            self.label_summ.setText("Test OK")

    def __init__(self):

        self.button.clicked.connect(self.button_click)
        self.window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.show_window()

    def show_window(self):
        self.window.show()


if __name__ == "__main__":
    window_application = WindowApp()
    os.system("pkill vfsd-gphoto2")

    sys.exit(window_application.app.exec_())
