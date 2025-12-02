import sqlite3
from datetime import datetime


def init_database():
    """Tạo database và các bảng"""
    conn = sqlite3.connect('chi_tieu.db')
    cursor = conn.cursor()

    print("🔧 Đang tạo database...")

    # Bảng danh mục
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS categories
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       name
                       TEXT
                       NOT
                       NULL,
                       type
                       TEXT
                       NOT
                       NULL
                   )
                   ''')
    print("✅ Đã tạo bảng 'categories'")

    # Bảng giao dịch
    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS transactions
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       amount
                       REAL
                       NOT
                       NULL,
                       category_id
                       INTEGER,
                       date
                       TEXT
                       NOT
                       NULL,
                       note
                       TEXT,
                       type
                       TEXT
                       NOT
                       NULL,
                       FOREIGN
                       KEY
                   (
                       category_id
                   ) REFERENCES categories
                   (
                       id
                   )
                       )
                   ''')
    print("✅ Đã tạo bảng 'transactions'")

    # Thêm danh mục mặc định (nếu chưa có)
    cursor.execute('SELECT COUNT(*) FROM categories')
    count = cursor.fetchone()[0]

    if count == 0:
        default_categories = [
            ('Lương', 'Thu'),
            ('Tiền thưởng', 'Thu'),
            ('Thu khác', 'Thu'),
            ('Ăn uống', 'Chi'),
            ('Đi lại', 'Chi'),
            ('Giải trí', 'Chi'),
            ('Mua sắm', 'Chi'),
            ('Học tập', 'Chi'),
            ('Sức khỏe', 'Chi'),
            ('Chi khác', 'Chi')
        ]

        cursor.executemany('''
                           INSERT INTO categories (name, type)
                           VALUES (?, ?)
                           ''', default_categories)

        print("✅ Đã thêm 10 danh mục mặc định")

        # Hiển thị danh sách danh mục
        print("\n📋 DANH MỤC ĐÃ TẠO:")
        cursor.execute('SELECT id, name, type FROM categories')
        for row in cursor.fetchall():
            icon = "💰" if row[2] == "thu" else "💸"
            print(f"   {icon} {row[0]}. {row[1]} ({row[2]})")
    else:
        print(f"ℹ️  Database đã có {count} danh mục")

    conn.commit()
    conn.close()
    print("\n🎉 Database đã sẵn sàng! File: chi_tieu.db")


def view_database():
    """Xem nội dung database (dùng để kiểm tra)"""
    try:
        conn = sqlite3.connect('chi_tieu.db')
        cursor = conn.cursor()

        print("\n" + "=" * 50)
        print("📊 NỘI DUNG DATABASE")
        print("=" * 50)

        # Xem danh mục
        print("\n📁 BẢNG CATEGORIES:")
        cursor.execute('SELECT * FROM categories')
        categories = cursor.fetchall()
        if categories:
            print(f"{'ID':<5} {'Tên':<20} {'Loại':<10}")
            print("-" * 35)
            for cat in categories:
                print(f"{cat[0]:<5} {cat[1]:<20} {cat[2]:<10}")
        else:
            print("   (Chưa có dữ liệu)")

        # Xem giao dịch
        print("\n💳 BẢNG TRANSACTIONS:")
        cursor.execute('SELECT * FROM transactions')
        transactions = cursor.fetchall()
        if transactions:
            print(f"{'ID':<5} {'Số tiền':<15} {'Danh mục ID':<12} {'Ngày':<12} {'Ghi chú':<20} {'Loại':<10}")
            print("-" * 80)
            for trans in transactions:
                amount_str = f"{trans[1]:,.0f}đ"
                print(
                    f"{trans[0]:<5} {amount_str:<15} {trans[2]:<12} {trans[3]:<12} {trans[4] or '':<20} {trans[5]:<10}")
        else:
            print("   (Chưa có dữ liệu)")

        conn.close()
        print("\n" + "=" * 50)

    except sqlite3.Error as e:
        print(f"❌ Lỗi khi đọc database: {e}")


if __name__ == '__main__':

    init_database()


    view_database()
