import platform
import subprocess
import sys

def get_computer_model():
    system = platform.system()

    try:
        if system == "Windows":
            result = subprocess.check_output(["wmic", "computersystem", "get", "model"], shell=True)
            return result.decode().split("\n")[1].strip()

        elif system == "Darwin":  # macOS
            result = subprocess.check_output(["system_profiler", "SPHardwareDataType"])
            for line in result.decode().splitlines():
                if "Model Identifier" in line:
                    return line.split(":")[1].strip()

        elif system == "Linux":
            try:
                # 尝试读取 product_name 文件
                with open("/sys/devices/virtual/dmi/id/product_name", "r") as f:
                    return f.read().strip()
            except FileNotFoundError:
                # 使用 dmidecode（需要 root 权限）
                result = subprocess.check_output(["sudo", "dmidecode", "-s", "system-product-name"])
                return result.decode().strip()

        else:
            return f"Unsupported OS: {system}"

    except Exception as e:
        return f"Error retrieving model: {e}"

# 示例用法
if __name__ == "__main__":
    print("💻 电脑型号:", get_computer_model())