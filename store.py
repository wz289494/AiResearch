import pandas as pd
import os

from utils import Utils

class Store(object):
    def mode_excel(self, json_str,save_path):
        # 数据转为列表
        data_list = Utils.json_to_listdict(json_str)
        # 数据转为df
        df = pd.DataFrame(data_list)

        # 如果目标表格不存在，则创建
        if not os.path.exists(save_path):
            df.to_excel(save_path, index=False)
        else:
            with pd.ExcelWriter(save_path, mode='a', engine='openpyxl', if_sheet_exists='overlay') as writer:
                # 获取已存在的最大行数
                start_row = writer.sheets['Sheet1'].max_row
                # 如果已经写过内容（即最大行数大于1），则应避免再次写入表头
                if start_row > 1:
                    header = False
                else:
                    header = True
                # 写入DataFrame，避免额外表头
                df.to_excel(writer, sheet_name='Sheet1', startrow=start_row, index=False, header=header)
