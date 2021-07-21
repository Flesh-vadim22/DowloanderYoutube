from Design_app import Design_app
from PyQt5 import QtCore, QtWidgets
from Models.ProccessorModel import ProccessorModel
from PyQt5.QtGui import QImage, QPixmap
import threading
import requests
import os

class MainController(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Design_app()
        self.ui.setupUi(self)
        self.ui.check_btn.clicked.connect(self.check_video)
        self.ui.review_btn.clicked.connect(self.review_video)
        self.ui.dowload_btn.clicked.connect(self.dowload_video)
        
    def check_video(self):
        self.name_video = self.ui.name_video_edit.text()
        self.url = self.ui.link_edit.text()
        self.path = self.ui.fold_video_line_edit.text()
        if   self.url !='':
            self.th = ProccessorModel(self.name_video, self.url, self.path)
            threading.Thread(target=self.th.run).start()
            self.th.length.connect(self.append_video)
        else:
            QtWidgets.QMessageBox.warning(self, 'Предупреждение', 'Укажите ссылку на видео!')

    def review_video(self):
        self.file = QtWidgets.QFileDialog.getExistingDirectory(self)
        if self.file !="":
            self.ui.fold_video_line_edit.setText(self.file)
        else:
            pass

    def dowload_video(self):
        self.name_video = self.ui.name_video_edit.text()
        self.url = self.ui.link_edit.text()
        self.path = self.ui.fold_video_line_edit.text()
        if self.url ==''or self.path =='':
            QtWidgets.QMessageBox.critical(self, 'Ошибка', 'Введите путь видео и выбирите место его сохранения')
        else:
            name_video = str(self.path) + '/'+ str(self.name_video) + '.mp4'
            print(name_video)
            if os.path.isfile(name_video):
                QtWidgets.QMessageBox.warning(self, 'Внимание!', 'Данное видео уже загружено')
            else:
                self.th = ProccessorModel(self.name_video, self.url, self.path)
                threading.Thread(target=self.th.download).start()
                self.th.rec.connect(self.progress_bar)

    def append_video(self, title, description, thumbnail):
        if description == '': description = 'Описание видео отсутствует'
        self.ui.name_video_edit.setText(title)
        self.ui.description_video_lab.setText(description)
        img = QImage()
        img.loadFromData(requests.get(thumbnail).content)
        self.ui.img_lab.setPixmap(QPixmap(img))
        self.ui.img_lab.show()

    def progress_bar(self, size):
        self.ui.dowload_ProgBar.setValue(size)
        val = int(self.ui.dowload_ProgBar.value())
        if val == 100:
            QtWidgets.QMessageBox.about(self, 'Сообщение', 'Поздравляем, видео скачано!')
            self.ui.dowload_ProgBar.setValue(0)
