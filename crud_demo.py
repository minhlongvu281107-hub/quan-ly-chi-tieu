import sqlite3

conn = sqlite3.connect('hoc_sinh.db')
cursor = conn.cursor()

# Tạo bảng
cursor.execute('''
    CREATE TABLE IF NOT EXISTS hoc_sinh (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ten TEXT NOT NULL,
        tuoi INTEGER,
        lop TEXT,
        diem_tb REAL
    )
''')

print("=== THÊM HỌC SINH ===\n")

# Cách 1: Thêm 1 người
cursor.execute('''
    INSERT INTO hoc_sinh (ten, tuoi, lop, diem_tb)
    VALUES ('Nguyễn Văn A', 18, '12A1', 8.5)
''')
print("✅ Đã thêm: Nguyễn Văn A")

# Cách 2: Dùng placeholder (?) - AN TOÀN HƠN
ten = "Trần Thị B"
tuoi = 17
lop = "12A2"
diem = 9.0

cursor.execute('''
    INSERT INTO hoc_sinh (ten, tuoi, lop, diem_tb)
    VALUES (?, ?, ?, ?)
''', (ten, tuoi, lop, diem))
print(f"✅ Đã thêm: {ten}")

# Cách 3: Thêm NHIỀU người cùng lúc
danh_sach = [
    ('Lê Văn C', 18, '12A1', 7.5),
    ('Phạm Thị D', 17, '12A3', 8.0),
    ('Hoàng Văn E', 18, '12A2', 6.5)
]

cursor.executemany('''
    INSERT INTO hoc_sinh (ten, tuoi, lop, diem_tb)
    VALUES (?, ?, ?, ?)
''', danh_sach)
print(f"✅ Đã thêm {len(danh_sach)} học sinh")

conn.commit()
print("\n✅ Đã lưu tất cả vào database")

conn.close()
# Mở lại kết nối
conn = sqlite3.connect('hoc_sinh.db')
cursor = conn.cursor()

print("\n=== ĐỌC DỮ LIỆU ===\n")

# 1. Đọc TẤT CẢ
print("1. TẤT CẢ HỌC SINH:")
cursor.execute('SELECT * FROM hoc_sinh')
rows = cursor.fetchall()
for row in rows:
    print(f"   ID: {row[0]}, Tên: {row[1]}, Tuổi: {row[2]}, Lớp: {row[3]}, Điểm: {row[4]}")

# 2. Chỉ lấy TÊN và ĐIỂM
print("\n2. TÊN VÀ ĐIỂM:")
cursor.execute('SELECT ten, diem_tb FROM hoc_sinh')
rows = cursor.fetchall()
for row in rows:
    print(f"   {row[0]}: {row[1]} điểm")

# 3. LỌC: Học sinh có điểm >= 8.0
print("\n3. HỌC SINH GIỎI (>= 8.0):")
cursor.execute('SELECT ten, diem_tb FROM hoc_sinh WHERE diem_tb >= 8.0')
rows = cursor.fetchall()
for row in rows:
    print(f"   {row[0]}: {row[1]} điểm")

# 4. SẮP XẾP theo điểm (cao → thấp)
print("\n4. XẾP HẠNG THEO ĐIỂM:")
cursor.execute('SELECT ten, diem_tb FROM hoc_sinh ORDER BY diem_tb DESC')
rows = cursor.fetchall()
for i, row in enumerate(rows, 1):
    print(f"   #{i}: {row[0]} - {row[1]} điểm")

# 5. ĐẾM số học sinh
cursor.execute('SELECT COUNT(*) FROM hoc_sinh')
count = cursor.fetchone()[0]
print(f"\n5. TỔNG SỐ: {count} học sinh")

# 6. ĐIỂM TRUNG BÌNH của cả lớp
cursor.execute('SELECT AVG(diem_tb) FROM hoc_sinh')
avg = cursor.fetchone()[0]
print(f"6. ĐIỂM TB CẢ LỚP: {avg:.2f}")

conn.close()