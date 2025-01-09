import os
import sys

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QMessageBox, QLabel
)

from xinshili.excel_combined import merge_based_on_largest_header
from xinshili.pdf_split import split_pdf, extract_text_from_pdf
from xinshili.utils import ensure_directory_exists, open_dir


# PDF 处理线程
class PDFProcessingThread(QThread):
    success = pyqtSignal(str)
    error = pyqtSignal(str)
    warning = pyqtSignal(str)

    def __init__(self, input_pdf_path, output_folder_path):
        super().__init__()
        self.input_pdf_path = input_pdf_path
        self.output_folder_path = output_folder_path

    def run(self):
        try:
            ensure_directory_exists(self.output_folder_path)

            # 裁剪为单独的 PDF
            split_pdf(self.input_pdf_path, self.output_folder_path)
            extract_text_from_pdf(self.output_folder_path)
            self.success.emit(
                f"PDF 裁剪完成！"
                f"\n文件已保存在：{self.output_folder_path}"
                f"\n⚠注意：如果存在没有以面单号命名的文件则需要手动重命名，并手动添加到 '运单号列表.xlsx' 中")
        except Exception as e:
            self.error.emit(f"处理 PDF 时出现问题：{str(e)}")


class PDFTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PDF 面单裁剪工具")
        self.setGeometry(100, 100, 500, 300)

        # 初始化全局变量
        self.input_pdf_path = None
        self.output_folder_path = None
        self.file_name_without_extension = None

        # 布局
        layout = QVBoxLayout()

        # 文件选择按钮和标签
        self.upload_btn = QPushButton("上传 PDF 文件", self)
        self.upload_btn.setFixedSize(200, 50)
        self.upload_btn.clicked.connect(self.upload_file)
        layout.addWidget(self.upload_btn)

        self.input_label = QLabel("未选择任何文件", self)
        layout.addWidget(self.input_label)

        # 输出目录选择按钮和标签
        self.output_btn = QPushButton("选择输出目录", self)
        self.output_btn.setFixedSize(200, 50)
        self.output_btn.clicked.connect(self.select_output_folder)
        layout.addWidget(self.output_btn)

        self.output_label = QLabel("未选择输出目录", self)
        layout.addWidget(self.output_label)

        # 开始处理按钮
        self.process_btn = QPushButton("开始处理 PDF", self)
        self.process_btn.setFixedSize(200, 50)
        self.process_btn.clicked.connect(self.process_pdf)
        layout.addWidget(self.process_btn)

        # 设置窗口布局
        self.setLayout(layout)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择 PDF 文件", "", "PDF 文件 (*.pdf)")
        if file_path:
            self.input_pdf_path = file_path
            self.file_name_without_extension = os.path.splitext(os.path.basename(file_path))[0]
            self.input_label.setText(f"已选择文件：{file_path}")
        else:
            self.input_label.setText("未选择任何文件")

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder_path:
            if self.file_name_without_extension:
                # 拼接输出路径
                folder_path = os.path.join(folder_path, self.file_name_without_extension)
                ensure_directory_exists(folder_path)  # 确保拼接后的目录存在

            self.output_folder_path = folder_path
            self.output_label.setText(f"输出目录：{folder_path}")
        else:
            self.output_label.setText("未选择输出目录")

    def process_pdf(self):
        if not self.input_pdf_path or not self.output_folder_path:
            QMessageBox.critical(self, "错误", "请先选择 PDF 文件和输出目录！")
            return

        # 创建后台线程
        self.thread = PDFProcessingThread(self.input_pdf_path, self.output_folder_path)
        self.thread.success.connect(self.show_success_message)
        self.thread.error.connect(self.show_error_message)
        self.thread.warning.connect(self.show_warning_message)
        self.thread.start()

    def show_success_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setWindowTitle("成功")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Ok)

        # 绑定自定义逻辑到 OK 按钮点击事件
        msg_box.accepted.connect(self.custom_logic_after_success)
        msg_box.exec_()

    def custom_logic_after_success(self):
        if self.output_folder_path:
            open_dir(self.output_folder_path)

    def show_error_message(self, message):
        QMessageBox.critical(self, "错误", message)

    def show_warning_message(self, message):
        QMessageBox.warning(self, "警告", message)


# Excel 文件合并功能窗口
class ExcelMergeTool(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Excel 文件合并工具")
        self.setGeometry(100, 100, 500, 300)
        self.input_folder = None
        self.output_file = None

        layout = QVBoxLayout()

        # 选择输入文件夹按钮
        self.input_btn = QPushButton("选择输入目录", self)
        self.input_btn.setFixedSize(200, 50)
        self.input_btn.clicked.connect(self.select_input_folder)
        layout.addWidget(self.input_btn)

        self.input_label = QLabel("未选择输入目录", self)
        layout.addWidget(self.input_label)

        # 选择输出文件按钮
        self.output_btn = QPushButton("选择输出目录", self)
        self.output_btn.setFixedSize(200, 50)
        self.output_btn.clicked.connect(self.select_output_folder)
        layout.addWidget(self.output_btn)

        self.output_label = QLabel("未选择输出目录", self)
        layout.addWidget(self.output_label)

        # 开始合并按钮
        self.merge_btn = QPushButton("开始合并 Excel", self)
        self.merge_btn.setFixedSize(200, 50)
        self.merge_btn.clicked.connect(self.merge_excel_files)
        layout.addWidget(self.merge_btn)

        self.setLayout(layout)

    def select_input_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输入目录")
        if folder:
            self.input_folder = folder
            self.input_label.setText(f"输入目录：{folder}")
        else:
            self.input_label.setText("未选择任何文件夹")

    def select_output_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择输出目录")
        if folder:
            self.output_file = folder
            self.output_label.setText(f"输入目录：{folder}")
        else:
            self.output_label.setText("未选择任何文件夹")

    def merge_excel_files(self):
        if not self.input_folder or not self.output_file:
            QMessageBox.critical(self, "错误", "请先选择输入文件夹和输出文件夹！")
            return
        try:
            result_output_file = self.output_file + "/combined.xlsx"
            merge_based_on_largest_header(self.input_folder, result_output_file)

            # 创建消息框
            msg_box = QMessageBox(self)
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("成功")
            msg_box.setText(f"Excel 合并完成！\n文件已保存到：{result_output_file}")
            msg_box.setStandardButtons(QMessageBox.Ok)

            # 绑定自定义逻辑到 OK 按钮点击事件
            msg_box.accepted.connect(lambda: self.custom_logic_after_merge(self.output_file))
            msg_box.exec_()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"Excel 合并过程中发生错误：{str(e)}")

    def custom_logic_after_merge(self, file_path):
        open_dir(file_path)


# 主窗口
class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("XYL-小工具")
        self.setGeometry(100, 100, 400, 200)

        layout = QVBoxLayout()

        # PDF 切分功能入口按钮
        self.pdf_tool_btn = QPushButton("PDF 切分工具", self)
        self.pdf_tool_btn.setFixedSize(200, 50)
        self.pdf_tool_btn.clicked.connect(self.open_pdf_tool)
        layout.addWidget(self.pdf_tool_btn)

        # Excel 合并功能入口按钮
        self.excel_merge_btn = QPushButton("Excel 合并工具", self)
        self.excel_merge_btn.setFixedSize(200, 50)
        self.excel_merge_btn.clicked.connect(self.open_excel_merge_tool)
        layout.addWidget(self.excel_merge_btn)

        self.setLayout(layout)

    def open_pdf_tool(self):
        self.pdf_tool = PDFTool()
        self.pdf_tool.show()

    def open_excel_merge_tool(self):
        self.excel_merge_tool = ExcelMergeTool()
        self.excel_merge_tool.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
