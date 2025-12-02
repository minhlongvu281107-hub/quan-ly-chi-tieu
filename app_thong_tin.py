import sys
from PyQt5 import QtWidgets, uic

class ThongtinWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('form_thong_tin.ui', self)

        self.combo_gioitinh.addItems([ 'Khác'])
        self.btn_luu.clicked.connect(self.luu_thong_tin)
        self.btn_xoa.clicked.connect(self.xoa_thong_tin)
    def luu_thong_tin(self):
        hoten = self.input_hoten.text()
        tuoi = self.input_tuoi.text()
        gioitinh = self.combo_gioitinh.currentText()
        if not hoten:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập họ tên.")
            return
        if not tuoi.isdigit() or int(tuoi) <= 0:
            QtWidgets.QMessageBox.warning(self, "Lỗi", "Vui lòng nhập tuổi hợp lệ.")
            return
        ketqua = f"Họ tên: {hoten}\nTuổi: {tuoi}\nGiới tính: {gioitinh}"
        self.text_ketqua.setPlainText(ketqua)
        QtWidgets.QMessageBox.information(self, "Thông tin đã lưu", ketqua)
    def xoa_thong_tin(self):
        self.input_hoten.clear()
        self.input_tuoi.clear()
        self.combo_gioitinh.setCurrentIndex(0)
        self.text_ketqua.clear()
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = ThongtinWindow()
    window.show()
    sys.exit(app.exec_())

