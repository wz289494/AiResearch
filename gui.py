import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
import pandas as pd
import threading
import json
import os

from model import Model
from prompt import Prompt
from store import Store
from utils import Utils

class Gui:
    def __init__(self):
        # gui面板设置
        self.root = tk.Tk()
        self.root.title("AI研究工具")
        self.root.geometry("900x550")

        # 模块调用设置
        self.model = Model()
        self.prompt = Prompt()
        self.store = Store()
        self.utils = Utils()

        # 配置参数设置
        self.CONFIG_FILE = "config.json"
        self.__load_config()

        # 运行程序
        self.setup_ui()

    def setup_ui(self):
        # 左侧和右侧的框架
        left_frame = ttk.Frame(self.root, width=300, height=400)
        left_frame.pack(side=tk.LEFT, fill="y", padx=10, pady=10, expand=True)

        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill="both", padx=10, pady=10, expand=True)

        # 左侧打印流程信息
        ttk.Label(left_frame, text="流程信息:").pack(anchor="w")
        self.process_info_text = scrolledtext.ScrolledText(left_frame, width=40, height=35)
        self.process_info_text.pack(fill="both", expand=True)
        self.process_info_text.tag_config('red', foreground='red')
        self.process_info_text.tag_config('black', foreground='black')

        # 右侧的输入框架
        input_frame = ttk.Frame(right_frame)
        input_frame.pack(fill="both", expand=True)

        # 配置令牌和选择model输入框
        token_frame = ttk.LabelFrame(input_frame, text="配置")
        token_frame.pack(pady=5, fill="x")

        ttk.Label(token_frame, text="令牌:").grid(row=0, column=0, padx=5, pady=5)
        self.token_entry = ttk.Entry(token_frame, width=20)
        self.token_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(token_frame, text="模型:").grid(row=0, column=2, padx=5, pady=5)
        self.mode_entry = ttk.Entry(token_frame, width=20)
        self.mode_entry.grid(row=0, column=3, padx=5, pady=5)

        # 输入需求的框
        ttk.Label(input_frame, text="输入需求:").pack(anchor="w", pady=5)
        self.requirements_entry = scrolledtext.ScrolledText(input_frame, width=60, height=5)
        self.requirements_entry.pack(fill="x", pady=5)

        # 预想格式的框
        ttk.Label(input_frame, text="预想格式:").pack(anchor="w", pady=5)
        self.format_entry = scrolledtext.ScrolledText(input_frame, width=60, height=5)
        self.format_entry.pack(fill="x", pady=5)

        # 目标文件路径，从本地选择
        ttk.Label(input_frame, text="目标Excel文件路径:").pack(anchor="w", pady=5)
        folder_frame = ttk.Frame(input_frame)
        folder_frame.pack(fill="x", pady=5)
        self.folder_entry = ttk.Entry(folder_frame, width=50)
        self.folder_entry.pack(side=tk.LEFT, padx=5)
        folder_button = ttk.Button(folder_frame, text="选择", command=self.__select_file)
        folder_button.pack(side=tk.LEFT, padx=5)

        # 目标列，输入框
        ttk.Label(input_frame, text="目标列名:").pack(anchor="w", pady=5)
        self.target_column_entry = ttk.Entry(input_frame, width=60)
        self.target_column_entry.pack(fill="x", pady=5)

        # 保存位置，输入框
        ttk.Label(input_frame, text="保存Excel名:").pack(anchor="w", pady=5)
        self.save_location_entry = ttk.Entry(input_frame, width=60)
        self.save_location_entry.pack(fill="x", pady=5)

        # 恢复上次输入的内容
        self.__restore_last_inputs()

        # 开始分析按钮
        start_button = tk.Button(right_frame, text="开始分析", command=self.start_analysis_thread, bg="blue", fg="white")
        start_button.pack(side=tk.BOTTOM, pady=10, anchor="center")

    def __select_file(self):
        # 选择本地文件
        file_selected = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        self.folder_entry.delete(0, tk.END)
        self.folder_entry.insert(0, file_selected)

    def get_user_inputs(self):
        # 获取用户输入的值并存储在实例变量中
        self.token = self.token_entry.get().strip()
        self.modeluse = self.mode_entry.get().strip()
        self.requirements = self.requirements_entry.get("1.0", tk.END).strip()
        self.target_format = self.format_entry.get("1.0", tk.END).strip()
        self.target_path = self.folder_entry.get().strip()
        self.target_column = self.target_column_entry.get().strip()
        self.save_location = self.save_location_entry.get().strip()

        # 保存当前输入内容
        self.__save_config()

    def start_analysis_thread(self):
        # 使用线程来启动分析，避免阻塞GUI
        thread = threading.Thread(target=self.start_analysis)
        thread.start()

    def start_analysis(self):
        # 获取用户输入
        self.get_user_inputs()

        # 打印开始流程
        self.__update_process_info("开始处理流程...", "black")

        # 打印加载文件
        self.__update_process_info(f"加载目标文件: {self.target_path}", "black")

        # 加载目标文件
        try:
            target_df = pd.read_excel(self.target_path)
        except Exception as e:
            self.__update_process_info(f"加载目标文件失败: {str(e)}", "red")
            return

        # 加载目标列
        try:
            content_list = target_df[self.target_column].tolist()
        except KeyError as e:
            self.__update_process_info(f"加载目标列失败: {str(e)}", "red")
            return

        # 调整目标格式
        self.target_format = self.utils.string_to_list(self.target_format)

        # 打印令牌和模型
        self.__update_process_info(f"令牌={self.token}\n模型={self.modeluse}", "black")
        self.model.set_token_model(self.token, self.modeluse)

        # 设置保存位置
        self.save_location = Utils.create_new_file_path(self.target_path, self.save_location)

        # 设置分割线
        self.__update_process_info("------------", "black")

        # 进程
        num = 1
        for content in content_list:
            self.__update_process_info(f"当前为第 {num}/{len(content_list)} 项", "black")

            # 构造prompt
            prompt = self.prompt.prompt_generator(self.requirements, self.target_format, content)

            # 实际分析
            try:
                # 获取模型响应
                response = self.model.response(prompt)
                # 确保json格式
                response_json = self.utils.extract_json_strings(response)
                self.__update_process_info(f"模型响应:\n{response_json}", "black")

                # 保存
                self.store.mode_excel(response_json, self.save_location)
            except Exception as e:
                self.__update_process_info(f"处理第 {num} 项时出错: {str(e)}", "red")

            num += 1
            self.__update_process_info("\n", "black")

        # 打印结果
        self.__update_process_info("------------", "black")
        self.__update_process_info(f"结果保存至{self.save_location}", "black")

    def __update_process_info(self, message, color):
        # 在主线程中更新GUI，并设置文本颜色
        tag = 'black' if color == 'black' else 'red'
        self.root.after(0, lambda: self.process_info_text.insert(tk.END, message + "\n", (tag,)))
        self.root.after(0, lambda: self.process_info_text.see(tk.END))

    def __save_config(self):
        # 保存config设置
        config = {
            "token": self.token,
            "modeluse": self.modeluse,
            "requirements": self.requirements,
            "target_format": self.target_format,
            "target_path": self.target_path,
            "target_column": self.target_column,
            "save_location": self.save_location
        }
        with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=4)

    def __load_config(self):
        # 加载设置
        if os.path.exists(self.CONFIG_FILE):
            with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def __restore_last_inputs(self):
        # 重新保存config设置
        if self.config:
            self.token_entry.insert(0, self.config.get("token", ""))
            self.mode_entry.insert(0, self.config.get("modeluse", ""))
            self.requirements_entry.insert(tk.END, self.config.get("requirements", ""))
            self.format_entry.insert(tk.END, self.config.get("target_format", ""))
            self.folder_entry.insert(0, self.config.get("target_path", ""))
            self.target_column_entry.insert(0, self.config.get("target_column", ""))
            self.save_location_entry.insert(0, self.config.get("save_location", ""))

if __name__ == "__main__":
    app = Gui()
    app.root.mainloop()
