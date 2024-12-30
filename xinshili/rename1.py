import os


def remove_parentheses_in_filenames(folder_path):
    """
    遍历文件夹，移除文件名中包含 "(1)" 的部分。

    :param folder_path: 要遍历的文件夹路径
    """
    try:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                # 检查文件名是否包含 "(1)"
                if "(1)" in file_name:
                    # 创建新的文件名
                    new_name = file_name.replace("(1)", "")
                    # 获取完整路径
                    old_file_path = os.path.join(root, file_name)
                    new_file_path = os.path.join(root, new_name)
                    # 重命名文件
                    os.rename(old_file_path, new_file_path)
                    print(f"重命名: {old_file_path} -> {new_file_path}")
    except Exception as e:
        print(f"发生错误: {e}")


# 示例调用
folder_to_process = "/Users/zkp/Library/Containers/com.tencent.xinWeChat/Data/Library/Application Support/com.tencent.xinWeChat/2.0b4.0.9/aee968804ccf60699f2aada7c6e578a8/Message/MessageTemp/0fcc718cb6d90044125b0e41b4080b43/File/运单文件"  # 替换为你的文件夹路径
remove_parentheses_in_filenames(folder_to_process)
