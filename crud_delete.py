import sqlite3

conn = sqlite3.connect('hoc_sinh.db')
cursor = conn.cursor()

print("=== XÓA DỮ LIỆU ===\n")

# 1. Xóa học sinh có ID = 1
cursor.execute('DELETE FROM hoc_sinh WHERE id = 1')
print("✅ Đã xóa học sinh ID = 1")

# 2. Xóa học sinh có điểm < 7.0
cursor.execute('DELETE FROM hoc_sinh WHERE diem_tb < 7.0')
deleted = cursor.rowcount  # Số dòng bị xóa
print(f"✅ Đã xóa {deleted} học sinh có điểm < 7.0")

conn.commit()

# Xem còn lại ai
cursor.execute('SELECT * FROM hoc_sinh')
rows = cursor.fetchall()
print(f"\nCÒN LẠI {len(rows)} HỌC SINH:")
for row in rows:
    print(f"   {row[1]} - {row[4]} điểm")

conn.close()
