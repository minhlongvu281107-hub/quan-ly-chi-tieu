import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox


class HelloWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Thiết lập cửa sổ
        self.setWindowTitle('Ứng dụng đầu tiên của tôi')
        self.setGeometry(100, 100, 400, 200)

        # Tạo widget trung tâm
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Tạo layout
        layout = QVBoxLayout()

        # Thêm label
        label = QLabel('Chào mừng đến với PyQt5!')
        label.setStyleSheet('font-size: 20px; color: blue;')

        # Thêm nút
        button = QPushButton('Bấm vào đây!')
        button.setStyleSheet('font-size: 14px; padding: 10px;')
        button.clicked.connect(self.show_message)
        button_exit = QPushButton('Thoát')
        button_exit.setStyleSheet('font-size: 14px; padding: 10px; background-color: #e74c3c; color: white;')
        button_exit.clicked.connect(self.close)  # Đóng cửa sổ
        layout.addWidget(button_exit)

        # Thêm vào layout
        layout.addWidget(label)
        layout.addWidget(button)

        central_widget.setLayout(layout)

    def show_message(self):
        QMessageBox.information(self, 'Thông báo', 'Hello World! 🎉\nBạn vừa tạo ứng dụng PyQt5 đầu tiên!')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HelloWindow()
    window.show()
    sys.exit(app.exec_())