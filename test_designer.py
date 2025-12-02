import sys


from PyQt5 import QtWidgets, uic

class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('form_test.ui', self)

        self.pushButton.clicked.connect(self.on_click)
    def on_click(self):
        print("da click nut")
        QtWidgets.QMessageBox.information(self, "Thong bao", "ban vua click")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
