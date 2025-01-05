import tkinter as tk
from tkinter import filedialog, messagebox
import pikepdf
import pdfplumber
import re
import os

from xinshili.pdf_split import split_pdf
from xinshili.pdf_split_tk import extract_text_from_pdf
from xinshili.utils import ensure_directory_exists


def upload_file():
    global input_pdf_path
    input_pdf_path = filedialog.askopenfilename(filetypes=[("PDF 文件", "*.pdf")])
    if input_pdf_path:
        input_label.config(text=f"已选择文件：{input_pdf_path}")
    else:
        input_label.config(text="未选择任何文件")


def select_output_folder():
    global output_folder_path
    output_folder_path = filedialog.askdirectory()
    if output_folder_path:
        output_label.config(text=f"输出目录：{output_folder_path}")
    else:
        output_label.config(text="未选择输出目录")


def process_pdf():
    if not input_pdf_path or not output_folder_path:
        messagebox.showerror("错误", "请先选择 PDF 文件和输出目录！")
        return

    ensure_directory_exists(input_pdf_path)
    matches = extract_text_from_pdf(input_pdf_path)

    if not matches:
        messagebox.showwarning("警告", "未找到任何匹配的面单号！")
        return

    # 裁剪为单独的 PDF
    split_pdf(input_pdf_path, output_folder_path, matches)
    messagebox.showinfo("成功", f"PDF 处理完成！文件已保存在：\n{output_folder_path}")


# GUI 界面
root = tk.Tk()
root.title("PDF 面单裁剪工具")
root.geometry("500x300")

# 初始化全局变量
input_pdf_path = None
output_folder_path = None

# 文件选择按钮和标签
tk.Button(root, text="上传 PDF 文件", command=upload_file).pack(pady=10)
input_label = tk.Label(root, text="未选择任何文件", wraplength=400)
input_label.pack()

# 输出目录选择按钮和标签
tk.Button(root, text="选择输出目录", command=select_output_folder).pack(pady=10)
output_label = tk.Label(root, text="未选择输出目录", wraplength=400)
output_label.pack()

# 开始处理按钮
tk.Button(root, text="开始处理 PDF", command=process_pdf, bg="green", fg="white").pack(pady=20)

# 运行主循环
root.mainloop()
