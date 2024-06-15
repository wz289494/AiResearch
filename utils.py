import json
import re
import os

class Utils(object):
    @staticmethod
    def list_to_jsonstr(inputlist):
        # 创建一个空字典
        json_dict = {}

        # 遍历列表，并将每个元素添加到字典中
        for i, item in enumerate(inputlist):
            json_dict[item] = f"结果{i + 1}"

        # 将字典转换为JSON字符串
        json_str = json.dumps(json_dict, ensure_ascii=False)

        return json_str

    @staticmethod
    def json_to_listdict(json_str):
        # 设置空列表
        result_list =[]

        # 将JSON字符串转换为字典
        result_dict = json.loads(json_str)

        # 载入列表
        result_list.append(result_dict)

        return result_list

    @staticmethod
    def extract_json_strings(text):
        # 正则表达式匹配 JSON 对象
        json_pattern = re.compile(r'(\{.*?\})')

        # 查找所有匹配的 JSON 对象
        matches = json_pattern.findall(text)

        return matches[0]

    @staticmethod
    def string_to_list(str):
        # 使用正则表达式匹配英文逗号或中文逗号
        return [item.strip() for item in re.split(r'[，,]', str)]

    @staticmethod
    def create_new_file_path(file_path, new_file_name):
        # 获取文件目录和当前文件名
        directory = os.path.dirname(file_path)
        current_file_name = os.path.basename(file_path)

        # 分割文件名和扩展名
        name_part, extension = os.path.splitext(current_file_name)

        # 处理新的文件名，保留目录路径和扩展名
        new_file_base_name = os.path.splitext(new_file_name)[0]
        new_file_path = os.path.join(directory, f"{new_file_base_name}{extension}")

        return new_file_path