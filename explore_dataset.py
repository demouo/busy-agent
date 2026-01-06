import pandas as pd

# 读取 parquet 文件
df = pd.read_parquet('datasets/react-llama.parquet')

# 查看基本信息
print("数据集形状:", df.shape)
print("\n列名:")
print(df.columns.tolist())
print("\n前几行数据:")
print(df.head(2))
print("\n数据类型:")
print(df.dtypes)
