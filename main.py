from PyQt5 import QtWidgets
import sys
from Controllers.MainController import MainController

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MainController()
    form.show()
    sys.exit(app.exec_())
