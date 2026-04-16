from flask import Blueprint, render_template

# 定義首頁 Blueprint
bp = Blueprint('home', __name__)

@bp.route('/', methods=['GET'])
def index():
    """
    處理首頁請求。
    
    1. 透過 RecordModel (get_all_records) 取回所有記錄。
    2. 透過 RecordModel (get_balance_summary) 取得加總過後的餘額統計。
    3. 夾帶獲取的資料渲染 index.html 模板。
    """
    pass
