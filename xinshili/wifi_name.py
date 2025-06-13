import random
import string

def generate_wifi_names_with_numbers(start=1, end=10):
    wifi_names = set()
    result = []

    for number in range(start, end + 1):
        attempts = 0
        while attempts < 100:
            # 最大基础字符串长度：确保插入数字后总长 ≤ 10
            max_base_len = 10 - len(str(number))
            base_len = random.randint(3, max_base_len)  # 最小长度为 3，增强随机性
            base_name = ''.join(random.choices(string.ascii_lowercase, k=base_len))

            # 随机插入数字
            insert_index = random.randint(0, len(base_name))
            wifi_name = base_name[:insert_index] + str(number) + base_name[insert_index:]

            if wifi_name not in wifi_names and len(wifi_name) <= 10:
                wifi_names.add(wifi_name)
                result.append(wifi_name)
                break

            attempts += 1
        else:
            raise ValueError(f"⚠️ 无法生成满足条件的 WiFi 名字：数字 {number}")

    return result

# 示例调用
if __name__ == "__main__":
    wifi_list = generate_wifi_names_with_numbers(1, 10)
    for wifi in wifi_list:
        print(wifi)