import os
import shutil

# 获取当前工作目录
current_directory = os.getcwd()

# 获取硬盘空间信息
total, used, free = shutil.disk_usage(current_directory)

# 打印硬盘空间信息
print(f"总硬盘空间: {total / (2**30):.2f} GB")
print(f"已使用硬盘空间: {used / (2**30):.2f} GB")
print(f"剩余硬盘空间: {free / (2**30):.2f} GB")

print(f"使用量: {used/total*100:.2f}%")