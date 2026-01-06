import pandas as pd

# 读取 parquet 文件
df = pd.read_parquet('datasets/react-llama.parquet')

# 查看第一个完整的 trajectory
print("=" * 80)
print("示例 1:")
print("=" * 80)
print(f"问题: {df.iloc[0]['question']}")
print(f"\n正确答案: {df.iloc[0]['correct_answer']}")
print(f"\nTrajectory:\n{df.iloc[0]['trajectory']}")

print("\n" + "=" * 80)
print("示例 2:")
print("=" * 80)
print(f"问题: {df.iloc[1]['question']}")
print(f"\n正确答案: {df.iloc[1]['correct_answer']}")
print(f"\nTrajectory:\n{df.iloc[1]['trajectory']}")
