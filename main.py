import time, sys
from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtUiTools import *
from PySide2.QtGui import *
import brightestSpot, cameraControll


NUMBER_SECONDS_TO_WAIT = 1


class WindowApp:
    #QT INIT
    app = QApplication([])
    ui_file = QFile('form_main.ui')
    ui_file.open(QFile.ReadOnly)
    loader = QUiLoader()
    window = loader.load(ui_file)
    button = window.Button_1
    label = window.Label_1
    image_label = window.Label_image


    def button_click(self):
        start_time = time.time()
        while ((time.time() - start_time) <= NUMBER_SECONDS_TO_WAIT):
            time.sleep(0.3)
            self.button.setEnabled(False)
            print(NUMBER_SECONDS_TO_WAIT - (time.time() - start_time))
            self.label.setText(str(round(NUMBER_SECONDS_TO_WAIT - (time.time() - start_time))))
            self.app.processEvents()
        self.button.setEnabled(True)
        image_src = cameraControll.capture_image()
        image_marked = brightestSpot.mark_brightest_spots(image_src)
        new_pixmap = QPixmap(image_marked)
        self.image_label.setPixmap(new_pixmap)


    def __init__(self):

        self.button.clicked.connect(self.button_click)
        self.window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)


        self.show_window()

    def show_window(self):
        self.window.show()





if __name__ == "__main__":
    window_application = WindowApp()

    sys.exit(window_application.app.exec_())
