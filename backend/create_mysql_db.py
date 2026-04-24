import pymysql
import os
from sqlalchemy.engine import make_url

# Định dạng: mysql+pymysql://user:password@host:port/dbname
# Lấy từ biến môi trường hoặc dùng mặc định giống database.py của bạn
DATABASE_URL = "mysql+pymysql://root:123456@localhost:3306/wellbeing"

def create_db_if_not_exists():
    url = make_url(DATABASE_URL)
    
    # Kết nối không chọn database để tạo database mới
    connection = pymysql.connect(
        host=url.host,
        user=url.username,
        password=url.password,
        port=url.port or 3306
    )
    
    try:
        with connection.cursor() as cursor:
            print(f"🚀 Đang kiểm tra database '{url.database}'...")
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {url.database} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"✅ Đã đảm bảo database '{url.database}' tồn tại.")
    finally:
        connection.close()

if __name__ == "__main__":
    try:
        create_db_if_not_exists()
    except Exception as e:
        print(f"❌ Lỗi khi tạo database: {e}")
        print("\n👉 Gợi ý: Hãy đảm bảo MySQL đang chạy và User/Password trong file database.py là chính xác.")
