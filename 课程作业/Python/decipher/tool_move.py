import os
import shutil

# 指定移动到的目标一级子目录
target_dir = 'lfw'

# 遍历当前目录及其所有二级子目录
for root, dirs, files in os.walk('.'):
    # 忽略隐藏目录
    dirs[:] = [d for d in dirs if not d.startswith('.')]
    
    # 遍历文件
    for file in files:
        # 获取文件完整路径
        src_file = os.path.join(root, file)
        # 如果文件，而不是目录
        if os.path.isfile(src_file):
            # 移动文件到目标目录
            dst_file = os.path.join(target_dir, file)
            try:
                shutil.move(src_file, dst_file)
                # print(f"Moved {src_file} to {dst_file}")
            except Exception as e:
                print(f"Error moving {src_file}: {e}")

# 提醒用户任务完成
print("All non-directory files have been moved to the target directory.")