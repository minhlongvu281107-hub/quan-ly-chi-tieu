import sqlite3

print("=== DEMO SQLite ===\n")

# 1. KẾT NỐI DATABASE (tự động tạo file demo.db nếu chưa có)
conn = sqlite3.connect('demo.db')
print("✅ Đã kết nối database: demo.db")

# 2. TẠO CURSOR (con trỏ để thực thi lệnh SQL)
cursor = conn.cursor()
print("✅ Đã tạo cursor")

# 3. TẠO BẢNG
cursor.execute('''
    CREATE TABLE IF NOT EXISTS hoc_sinh (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT NOT NULL,
        tuoi INTEGER,
        lop TEXT
    )
''')
print("✅ Đã tạo bảng 'hoc_sinh'")

# 4. THÊM DỮ LIỆU
cursor.execute('''
    INSERT INTO hoc_sinh (ten, tuoi, lop)
    VALUES ('Nguyễn Văn A', 18, '12A1')
''')
print("✅ Đã thêm học sinh: Nguyễn Văn A")

# 5. LƯU THAY ĐỔI (QUAN TRỌNG!)
conn.commit()
print("✅ Đã lưu thay đổi vào database")

# 6. ĐỌC DỮ LIỆU
cursor.execute('SELECT * FROM hoc_sinh')
rows = cursor.fetchall()

print("\n=== DANH SÁCH HỌC SINH ===")
for row in rows:
    print(f"ID: {row[0]}, Tên: {row[1]}, Tuổi: {row[2]}, Lớp: {row[3]}")

# 7. ĐÓNG KẾT NỐI
conn.close()
print("\n✅ Đã đóng kết nối database")