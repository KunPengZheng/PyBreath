import xlwings as xw


def calculate_formula(file_path):
    try:
        # 打开 Excel 应用程序（隐藏窗口）
        app = xw.App(visible=False)
        wb = xw.Book(file_path)  # 打开指定的 Excel 文件
        sheet = wb.sheets[0]  # 使用第一个工作表
    except Exception as e:
        raise Exception(f"错误: {e}")
