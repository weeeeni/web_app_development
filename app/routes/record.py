from flask import Blueprint, request, redirect, url_for, flash, render_template

# 定義紀錄操作的 Blueprint，統一以 /record 為 URL 前綴
bp = Blueprint('record', __name__, url_prefix='/record')

@bp.route('/create', methods=['GET'])
def create_page():
    """
    顯示新增收支記錄的表單頁面。
    渲染 create.html 模板供使用者填寫。
    """
    pass

@bp.route('/create', methods=['POST'])
def create():
    """
    接收新增表單的資料並存入資料庫。
    
    1. 從 request.form 取得 type, amount, date, note。
    2. 驗證資料是否齊全與格式正確（如：金額是否過低）。
    3. 條件符合後，呼叫 RecordModel.create_record 寫入紀錄。
    4. 寫入完畢後 Redirect 回首頁 (home.index)；驗證錯誤則回傳錯誤訊息並重畫表單。
    """
    pass

@bp.route('/<int:record_id>/delete', methods=['POST'])
def delete(record_id):
    """
    刪除指定 ID 的收支記錄。
    
    1. 呼叫 RecordModel.delete_record 進行刪除。
    2. 刪除完成後 Redirect 回首頁 (home.index)。
    """
    pass
