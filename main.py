import sys
import time
import os
import numpy as np
import cv2

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
    button_takePicture = window.Button_2
    button_test_n_compare = window.Button_3
    label = window.Label_1
    label_summ = window.Label_summary
    image_label = window.Label_image
    combo_sh = window.comboBox_sh
    diode_label = window.num_of_diode
    label_data = window.Label_data
    label_info = window.Label_info

    curr_template_image = ""#"/home/cezos/Pictures/Canon_700D/PIC_20-08-21--09:31:33.jpg"


    def display_data(self, data):
        text = ""
        isPassed = data["isPassed"]

        for i in range(0, len(data["R"])):


            text += str(i + 1) + " => "
            if(isPassed[i]):
                text += "Dioda sprawna\n"
            else:
                text += "!!Dioda NIEsprawna!!\n"
        self.label_data.setText(text)

    def button_click(self):
        try:
            x = int(self.diode_label.text())
            self.label_info.setText("")
        except:
            self.label_info.setText("Wypełnij wszystkie pola")
            return
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

        image_src = cameraControll.capture_image(sh_from_combo, "200")#'/home/cezos/Pictures/Canon_700D/PIC_20-08-21--09:34:16.jpg'
        image_marked, is_fatal = brightestSpot.mark_brightest_spots(image_src, self.diode_label.text())
        new_pixmap = QPixmap(image_marked)
        self.image_label.setPixmap(new_pixmap)
        if is_fatal:
            self.label_summ.setText("Test NOT OK")
        else:
            self.label_summ.setText("Test OK")

        data = brightestSpot.return_data()
        self.display_data(data)

    def button_takePicture_click(self):
        self.curr_template_image = cameraControll.capture_image("1/500", "200")

    def button_test_n_compare_click(self):
        self.button_click()
        data = brightestSpot.return_data()
        img = cv2.imread(self.curr_template_image)
        width, height = 100, 100
        cropped_imgs = []
        ile = 0
        for i in range(0, len(data["R"])):

            if(data["isPassed"][i] == False):
                if(ile>=3):
                    images = np.concatenate(cropped_imgs)
                    cv2.imshow("Wadliwe diody", images)
                    cv2.waitKey(0)
                    cropped_imgs = []
                    ile=0
                x = int(round(data["X"][i],1))
                y = int(round(data["Y"][i],1))
                cropped_imgs.append(img[y - height:y + height, x - width:x + width])
                ile+=1
        try:
            images = np.concatenate(cropped_imgs)
            cv2.imshow("Wadliwe diody2", images)
            cv2.waitKey(0)
        except:
            return


    def __init__(self):

        self.button.clicked.connect(self.button_click)
        self.button_takePicture.clicked.connect(self.button_takePicture_click)
        self.button_test_n_compare.clicked.connect(self.button_test_n_compare_click)
        self.window.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)

        self.show_window()

    def show_window(self):
        self.window.show()




if __name__ == "__main__":
    window_application = WindowApp()
    os.system("pkill vfsd-gphoto2")

    sys.exit(window_application.app.exec_())
