import sqlite3

conn = sqlite3.connect('hoc_sinh.db')
cursor = conn.cursor()

print("=== CẬP NHẬT DỮ LIỆU ===\n")

# 1. Cập nhật điểm của học sinh có ID = 1
cursor.execute('''
    UPDATE hoc_sinh
    SET diem_tb = 9.5
    WHERE id = 1
''')
print("✅ Đã cập nhật điểm học sinh ID = 1")

# 2. Cập nhật NHIỀU cột
cursor.execute('''
    UPDATE hoc_sinh
    SET tuoi = 19, lop = '12A4'
    WHERE ten = 'Trần Thị B'
''')
print("✅ Đã cập nhật tuổi và lớp của Trần Thị B")

# 3. Tăng điểm cho TẤT CẢ học sinh 0.5 điểm
cursor.execute('''
    UPDATE hoc_sinh
    SET diem_tb = diem_tb + 0.5
''')
print("✅ Đã cộng 0.5 điểm cho tất cả học sinh")

conn.commit()
print("\n✅ Đã lưu thay đổi")

# Xem kết quả
cursor.execute('SELECT ten, diem_tb FROM hoc_sinh')
rows = cursor.fetchall()
print("\nDIỂM SAU KHI CẬP NHẬT:")
for row in rows:
    print(f"   {row[0]}: {row[1]} điểm")

conn.close()