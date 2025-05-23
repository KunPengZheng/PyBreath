import re
import os

from xinshili import utils
from xinshili.utils import rename_images_by_filename


def extract_folder_info(path):
    folder_name = os.path.basename(os.path.normpath(path))

    # 兼容多种命名格式的正则匹配：
    # 1. 起始部分：字母+起始数字（例如 B1002 或 AB1002）
    # 2. 中间连接符：-、~、—
    # 3. 结束部分：可能是数字，也可能是字母+数字（如 B1200）
    match = re.search(r'^([A-Za-z]+)(\d+)[-_~—]+([A-Za-z]*)(\d+)', folder_name)

    if match:
        start_letter = match.group(1).upper()
        start_number = int(match.group(2))
        end_letter = match.group(3).upper() if match.group(3) else start_letter  # 如果没写则默认与起始一致
        end_number = int(match.group(4))
        print(start_letter, start_number, end_letter, end_number)
        return start_letter, start_number, end_letter, end_number
    else:
        return None, None, None, None


if __name__ == '__main__':
    source_file = input("请输入源文件夹的绝对路径：")
    start_letter, start_number, end_letter, end_number = extract_folder_info(source_file)
    rename_images_by_filename(source_file, start_letter, start_number, end_number)
    utils.open_dir(utils.get_file_dir(source_file))
