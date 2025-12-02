import sys
import sqlite3
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QListWidgetItem


class TodoApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('todo_ui.ui', self)
        self.setWindowTitle('📝 Todo App - Designer')

        self.conn = sqlite3.connect('todo.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS todos
                            (
                                id
                                INTEGER
                                PRIMARY
                                KEY
                                AUTOINCREMENT,
                                task
                                TEXT
                                NOT
                                NULL,
                                completed
                                INTEGER
                                DEFAULT
                                0
                            )
                            ''')
        self.conn.commit()

        self.input_task.returnPressed.connect(self.add_todo)
        self.btn_add.clicked.connect(self.add_todo)
        self.btn_delete.clicked.connect(self.delete_todo)
        self.list_widget.itemClicked.connect(self.toggle_complete)

        self.load_todos()

    def load_todos(self):
        self.list_widget.clear()
        self.cursor.execute('SELECT id, task, completed FROM todos')
        for row in self.cursor.fetchall():
            todo_id, task, completed = row
            item = QListWidgetItem(task)
            item.setData(Qt.UserRole, todo_id)
            item.setCheckState(Qt.Checked if completed else Qt.Unchecked)
            if completed:
                font = item.font()
                font.setStrikeOut(True)
                item.setFont(font)
            self.list_widget.addItem(item)
        self.update_stats()

    def add_todo(self):
        task = self.input_task.text().strip()
        if not task:
            QMessageBox.warning(self, 'Lỗi', 'Nhập công việc!')
            return
        self.cursor.execute('INSERT INTO todos (task) VALUES (?)', (task,))
        self.conn.commit()
        self.input_task.clear()
        self.load_todos()

    def delete_todo(self):
        item = self.list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, 'Lỗi', 'Chọn công việc cần xóa!')
            return
        reply = QMessageBox.question(self, 'Xác nhận', 'Xóa?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            todo_id = item.data(Qt.UserRole)
            self.cursor.execute('DELETE FROM todos WHERE id = ?', (todo_id,))
            self.conn.commit()
            self.load_todos()

    def toggle_complete(self, item):
        todo_id = item.data(Qt.UserRole)
        new_state = 0 if item.checkState() == Qt.Checked else 1
        self.cursor.execute('UPDATE todos SET completed = ? WHERE id = ?',
                            (new_state, todo_id))
        self.conn.commit()
        self.load_todos()

    def update_stats(self):
        self.cursor.execute('SELECT COUNT(*) FROM todos')
        total = self.cursor.fetchone()[0]
        self.cursor.execute('SELECT COUNT(*) FROM todos WHERE completed = 1')
        done = self.cursor.fetchone()[0]
        self.label_stats.setText(f"📊 Tổng: {total} | ✅ Xong: {done} | ⏳ Chưa: {total - done}")

    def closeEvent(self, event):
        self.conn.close()
        event.accept()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = TodoApp()
    window.show()
    sys.exit(app.exec_())