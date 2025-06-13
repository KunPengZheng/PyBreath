import random
import string


def generate_wifi_names_with_numbers(start=1, end=10):
    wifi_names = []

    numbers = list(range(start, end + 1))
    for number in numbers:
        # 随机生成一个 6~10 位的随机字母串
        name_length = random.randint(6, 10)
        base_name = ''.join(random.choices(string.ascii_lowercase, k=name_length))

        # 随机插入数字到任意位置
        insert_index = random.randint(0, len(base_name))
        name_with_number = base_name[:insert_index] + str(number) + base_name[insert_index:]

        wifi_names.append(name_with_number)

    return wifi_names


# 示例调用
if __name__ == "__main__":
    wifi_list = generate_wifi_names_with_numbers(1, 10)
    for wifi in wifi_list:
        print(wifi)
