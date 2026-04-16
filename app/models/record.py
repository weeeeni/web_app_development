import sqlite3
import os

# 根據架構設計，資料庫存放在 instance 之下
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db_connection():
    """取得資料庫連線，若目錄不存在則自動建立"""
    db_dir = os.path.dirname(DB_PATH)
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)
        
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # 讓結果像 dict 一樣可用 key 存取
    return conn

class RecordModel:
    @staticmethod
    def create_table_if_not_exists():
        """執行 schema.sql 以確保表格存在"""
        schema_path = os.path.join(BASE_DIR, 'database', 'schema.sql')
        if os.path.exists(schema_path):
            with open(schema_path, 'r', encoding='utf-8') as f:
                schema_sql = f.read()
            with get_db_connection() as conn:
                conn.executescript(schema_sql)

    @staticmethod
    def create_record(type_, amount, date, note=None):
        """新增一筆紀錄"""
        with get_db_connection() as conn:
            conn.execute(
                'INSERT INTO records (type, amount, date, note) VALUES (?, ?, ?, ?)',
                (type_, amount, date, note)
            )
            conn.commit()

    @staticmethod
    def get_all_records():
        """取得所有記錄（依日期與 ID 倒序排列）"""
        with get_db_connection() as conn:
            records = conn.execute(
                'SELECT * FROM records ORDER BY date DESC, id DESC'
            ).fetchall()
            return [dict(r) for r in records]

    @staticmethod
    def get_by_id(record_id):
        """根據 ID 取得單筆記錄"""
        with get_db_connection() as conn:
            record = conn.execute(
                'SELECT * FROM records WHERE id = ?', (record_id,)
            ).fetchone()
            return dict(record) if record else None

    @staticmethod
    def update_record(record_id, type_, amount, date, note=None):
        """更新一筆記錄"""
        with get_db_connection() as conn:
            conn.execute(
                'UPDATE records SET type = ?, amount = ?, date = ?, note = ? WHERE id = ?',
                (type_, amount, date, note, record_id)
            )
            conn.commit()

    @staticmethod
    def delete_record(record_id):
        """根據 ID 刪除單筆紀錄"""
        with get_db_connection() as conn:
            conn.execute('DELETE FROM records WHERE id = ?', (record_id,))
            conn.commit()

    @staticmethod
    def get_balance_summary():
        """計算總收入、總支出與目前結餘"""
        with get_db_connection() as conn:
            income_row = conn.execute(
                'SELECT SUM(amount) as total FROM records WHERE type = "income"'
            ).fetchone()
            expense_row = conn.execute(
                'SELECT SUM(amount) as total FROM records WHERE type = "expense"'
            ).fetchone()
            
            total_income = income_row['total'] if income_row['total'] else 0
            total_expense = expense_row['total'] if expense_row['total'] else 0
            balance = total_income - total_expense
            
            return {
                "total_income": total_income,
                "total_expense": total_expense,
                "balance": balance
            }
