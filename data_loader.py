import pandas as pd

def load_transactions(file_path):
    """
    读取消费账单 CSV 文件。

    参数：
        file_path：CSV 文件路径

    返回：
        读取后的 Pandas DataFrame
    """
    try:
        data = pd.read_csv(file_path, encoding="utf-8-sig")
        return data

    except FileNotFoundError:
        print("错误：找不到指定的文件！")
        return None

    except Exception as e:
        print(f"读取文件时发生错误：{e}")
        return None