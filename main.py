import sys
import csv
from datetime import datetime
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

class UngDungQuanLy(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('chi_tieu_ui.ui', self)

        self.thiet_lap_giao_dien()
        self.ket_noi_su_kien()
        self.tai_danh_muc()
        self.tai_bang_giao_dich()
        self.tinh_thong_ke()

    def thiet_lap_giao_dien(self):
        self.date_edit.setDate(datetime.now())
        self.date_edit.setDisplayFormat("dd/MM/yyyy")
        self.radio_chi.setChecked(True)
        self.table_transactions.setColumnWidth(0,138)
        self.table_transactions.setColumnWidth(1, 322)
        self.table_transactions.setColumnWidth(2, 230)
        self.table_transactions.setColumnWidth(3, 460)

        self.combo_month.addItem("Tất cả")
        hom_nay=datetime.now()
        for i in range(12):
            thang = hom_nay.month - i
            nam = hom_nay.year
            if thang <= 0:
                thang +=12
                nam -=1
            self.combo_month.addItem(f'{thang:02d}/{nam}')
        self.combo_month.setCurrentIndex(1)

    def ket_noi_su_kien(self):
        self.btn_add.clicked.connect(self.them_giao_dich)
        self.btn_edit.clicked.connect(self.sua_giao_dich)
        self.btn_delete.clicked.connect(self.xoa_giao_dich)
        self.radio_thu.toggled.connect(self.tai_danh_muc)
        self.combo_month.currentIndexChanged.connect(self.tai_bang_giao_dich)
        self.table_transactions.clicked.connect(self.chon_dong_de_sua)

    def doc_csv(self,ten_file):
        try:
            with open(ten_file,"r",encoding="utf-8") as f:
                return list(csv.DictReader(f))
        except:
            return []

    def ghi_csv(self,ten_file,du_lieu,cot_names):
        with open(ten_file,"w",encoding="utf-8",newline="") as f:
            writer = csv.DictWriter(f,fieldnames=cot_names)
            writer.writeheader()
            writer.writerows(du_lieu)

    def lay_id_moi(self,danh_sach):
        if not danh_sach:
            return 1
        return max(int(dong['id']) for dong in danh_sach) +1

    def loc_theo_thang(self,giao_dich,thang_chon):
        if thang_chon == "Tất cả":
            return giao_dich

        thang,nam=thang_chon.split("/")
        ket_qua=[]
        for gd in giao_dich:
            ngay_gd=datetime.strptime(gd['ngay'],"%Y-%m-%d")
            if ngay_gd.month==int(thang) and ngay_gd.year==int(nam):
                ket_qua.append(gd)
        return ket_qua

    def dinh_dang_tien(self,so_tien):
        return f"${int(so_tien):,}"

    def tai_danh_muc(self):
        self.combo_category.clear()
        loai = "thu" if self.radio_thu.isChecked() else "chi"
        danh_muc = self.doc_csv("danh_muc.csv")
        for dm in danh_muc:
            if dm['loai'] == loai:
                self.combo_category.addItem(dm['ten'],dm['id'])

    def them_giao_dich(self):
        try:
            so_tien = self.input_amount.text().strip()
            if not so_tien:
                QMessageBox.warning(self,"Lỗi","Chưa nhập số tiền")
                return
            so_tien = float(so_tien)

            ma_danh_muc = self.combo_category.currentData()
            if not ma_danh_muc:
                QMessageBox.warning(self,"Lỗi","Chưa chọn danh mục")
                return

            ngay = self.date_edit.date().toString("yyyy-MM-dd")
            ghi_chu = self.input_note.text().strip()
            loai = 'thu' if self.radio_thu.isChecked() else 'chi'
            giao_dich = self.doc_csv("giao_dich.csv")
            giao_dich_moi={
                'id': str(self.lay_id_moi(giao_dich)),
                 "so_tien": str(so_tien),
                 "ma_danh_muc": str(ma_danh_muc),
                 "ngay": ngay,
                 "ghi_chu": ghi_chu,
                 "loai": loai
            }
            giao_dich.append(giao_dich_moi)

            self.ghi_csv("giao_dich.csv", giao_dich,
                         ["id","so_tien","ma_danh_muc","ngay","ghi_chu","loai"])
            QMessageBox.information(self,"Thành công","Đã thêm giao dịch")

            self.xoa_form()
            self.tai_bang_giao_dich()
            self.tinh_thong_ke()
        except ValueError:
            QMessageBox.warning(self,"Lỗi","Số tiền không hợp lệ")
        except Exception as e:
            QMessageBox.critical(self,"Lỗi",f"Đã xảy ra lỗi: {str(e)}")

    def tai_bang_giao_dich(self):
        self.table_transactions.setRowCount(0)

        giao_dich =self.doc_csv("giao_dich.csv")
        danh_muc = self.doc_csv("danh_muc.csv")
        ten_danh_muc = {dm['id']:dm['ten'] for dm in danh_muc}

        danh_sach_loc=self.loc_theo_thang(giao_dich,self.combo_month.currentText())

        danh_sach_loc.sort(key=lambda x: x['ngay'],reverse=True)

        for so_dong,gd in enumerate(danh_sach_loc):
            self.table_transactions.insertRow(so_dong)

            ngay= datetime.strptime(gd['ngay'],"%Y-%m-%d").strftime("%Y/%m/%d")
            o_ngay=QTableWidgetItem(ngay)
            o_ngay.setData(Qt.UserRole, gd['id'])
            self.table_transactions.setItem(so_dong,0,o_ngay)

            ten = ten_danh_muc.get(gd['ma_danh_muc'],"Không rõ")
            self.table_transactions.setItem(so_dong,1,QTableWidgetItem(ten))

            so_tien = float(gd['so_tien'])
            chu_so_tien = self.dinh_dang_tien(so_tien)
            if gd['loai']=="chi":
                chu_so_tien = f"- {chu_so_tien}"
            else:
                chu_so_tien = f"+ {chu_so_tien}"
            o_so_tien = QTableWidgetItem(chu_so_tien)

            if gd['loai'] == 'chi':
                o_so_tien.setForeground(QColor('#e74c3c'))
            else:
                o_so_tien.setForeground(QColor('#27ae60'))
            self.table_transactions.setItem(so_dong,2,o_so_tien)

            self.table_transactions.setItem(so_dong,3,QTableWidgetItem(gd['ghi_chu']))

    def tinh_thong_ke(self):
        giao_dich = self.doc_csv("giao_dich.csv")

        danh_sach_loc = self.loc_theo_thang(giao_dich,self.combo_month.currentText())

        tong_thu = sum(float(gd['so_tien']) for gd in danh_sach_loc if gd['loai']=="thu")
        tong_chi = sum(float(gd['so_tien']) for gd in danh_sach_loc if gd['loai']=="chi")
        con_lai = tong_thu - tong_chi

        self.label_total_income.setText(f'Tổng thu :{self.dinh_dang_tien(tong_thu)}')
        self.label_total_expense.setText(f'Tổng chi :{self.dinh_dang_tien(tong_chi)}')
        self.label_balance.setText(f'Còn lại :{self.dinh_dang_tien(con_lai)}')

    def chon_dong_de_sua(self):
        dong_chon = self.table_transactions.currentRow()
        if dong_chon < 0:
            return

        id_giao_dich = self.table_transactions.item(dong_chon, 0).data(Qt.UserRole)
        giao_dich = self.doc_csv("giao_dich.csv")

        for gd in giao_dich:
            if gd['id'] == id_giao_dich:
                self.input_amount.setText(str(int(float(gd['so_tien']))))
                self.date_edit.setDate(datetime.strptime(gd['ngay'], '%Y-%m-%d'))
                self.input_note.setText(gd['ghi_chu'])

                if gd['loai']=="thu":
                    self.radio_thu.setChecked(True)
                else:
                    self.radio_chi.setChecked(True)
                vi_tri = self.combo_category.findData(gd["ma_danh_muc"])

                if vi_tri >=0:
                    self.combo_category.setCurrentIndex(vi_tri)
                break
    def sua_giao_dich(self):
        dong_chon = self.table_transactions.currentRow()
        if dong_chon <0:
            QMessageBox.warning(self,"Lỗi", "Chưa chọn giao dịch cần sửa")
            return
        try:
            id_giao_dich = self.table_transactions.item(dong_chon,0).data(Qt.UserRole)

            so_tien = float(self.input_amount.text().strip())
            ma_danh_muc =self.combo_category.currentData()
            ngay= self.date_edit.date().toString("yyyy-MM-dd")
            ghi_chu= self.input_note.text().strip()
            loai= "thu" if self.radio_thu.isChecked() else "chi"

            giao_dich = self.doc_csv("giao_dich.csv")

            for gd in giao_dich:
                if gd['id'] == id_giao_dich:
                    gd['so_tien'] = str(so_tien)
                    gd['ma_danh_muc'] = ma_danh_muc
                    gd['ngay'] = ngay
                    gd['ghi_chu'] = ghi_chu
                    gd['loai'] = loai
                    break

            self.ghi_csv('giao_dich.csv', giao_dich,
                         ['id', 'so_tien', 'ma_danh_muc', 'ngay', 'ghi_chu', 'loai'])
            QMessageBox.information(self, "Thành công", "Đã sửa giao dịch.")

            self.xoa_form()
            self.tai_bang_giao_dich()
            self.tinh_thong_ke()
        except ValueError:
            QMessageBox.warning(self, "Lỗi", "Số tiền không hợp lệ")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Lỗi: {e}")

    def xoa_giao_dich(self):
        dong_chon= self.table_transactions.currentRow()
        if dong_chon < 0:
            QMessageBox.warning(self, "Lỗi", "Chưa chọn giao dịch cần xóa")
            return

        tra_loi = QMessageBox.question(self, "Xác nhận",
                                        "Bạn có chắc muốn xóa giao dịch này?",
                                        QMessageBox.Yes | QMessageBox.No)
        if tra_loi == QMessageBox.Yes:
            try:
                id_giao_dich = self.table_transactions.item(dong_chon, 0).data(Qt.UserRole)
                giao_dich = self.doc_csv("giao_dich.csv")
                giao_dich =[gd for gd in giao_dich if gd['id'] != id_giao_dich]
                self.ghi_csv('giao_dich.csv', giao_dich,
                             ['id', 'so_tien', 'ma_danh_muc', 'ngay', 'ghi_chu', 'loai'])
                QMessageBox.information(self, "Thành công", "Đã xóa giao dịch thành công")

                self.xoa_form()
                self.tai_bang_giao_dich()
                self.tinh_thong_ke()
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Lỗi: {e}")
    def xoa_form(self):
        self.input_amount.clear()
        self.input_note.clear()
        self.date_edit.setDate(datetime.now())
        self.radio_chi.setChecked(True)
        if self.combo_category.count()>0:
            self.combo_category.setCurrentIndex(0)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    cua_so = UngDungQuanLy()
    cua_so.show()
    sys.exit(app.exec_())


























































