import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal
from xinshili.pdf_split import split_pdf, extract_text_from_pdf


def ensure_directory_exists(dir_path):
    """
    确保文件夹存在，不存在则创建
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"文件夹已创建: {dir_path}")
    else:
        print(f"文件夹已存在: {dir_path}")


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
            matches = extract_text_from_pdf(self.input_pdf_path)

            if not matches:
                self.warning.emit("未找到任何匹配的面单号！")
                return

            # 裁剪为单独的 PDF
            split_pdf(self.input_pdf_path, self.output_folder_path, matches)
            self.success.emit(f"PDF 处理完成！文件已保存在：\n{self.output_folder_path}")
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
        QMessageBox.information(self, "成功", message)

    def show_error_message(self, message):
        QMessageBox.critical(self, "错误", message)

    def show_warning_message(self, message):
        QMessageBox.warning(self, "警告", message)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = PDFTool()
    window.show()
    sys.exit(app.exec_())
