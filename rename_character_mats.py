#!/usr/bin/env python3
"""
重命名 character-mats/frosthaven 文件夹下的文件
规则：
1. 只操作不是 fh- 开头的文件
2. char_mat_*_f.png -> fh-*.png (下划线换成中横线)
3. char_mat_*_b.png -> fh-*-back.png (下划线换成中横线)
"""

import os
import re

def rename_character_mats():
    # 目标目录
    target_dir = "/Users/bytedance/cutter/assets/character-mats/frosthaven"
    
    if not os.path.exists(target_dir):
        print(f"目录不存在: {target_dir}")
        return
    
    # 获取所有文件
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    
    # 过滤出需要重命名的文件（不是 fh- 开头的）
    files_to_rename = [f for f in files if not f.startswith('fh-')]
    
    print(f"找到 {len(files_to_rename)} 个需要重命名的文件:")
    for f in files_to_rename:
        print(f"  - {f}")
    
    print("\n开始重命名...")
    
    renamed_count = 0
    
    for filename in files_to_rename:
        old_path = os.path.join(target_dir, filename)
        
        # 匹配 char_mat_*_f.png 格式
        match_f = re.match(r'char_mat_(.+)_f\.(png|jpg)$', filename)
        if match_f:
            character_name = match_f.group(1).replace('_', '-')
            extension = match_f.group(2)
            new_filename = f"fh-{character_name}.{extension}"
            new_path = os.path.join(target_dir, new_filename)
            
            try:
                os.rename(old_path, new_path)
                print(f"✓ {filename} -> {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"✗ 重命名失败 {filename}: {e}")
            continue
        
        # 匹配 char_mat_*_b.png 格式
        match_b = re.match(r'char_mat_(.+)_b\.(png|jpg)$', filename)
        if match_b:
            character_name = match_b.group(1).replace('_', '-')
            extension = match_b.group(2)
            new_filename = f"fh-{character_name}-back.{extension}"
            new_path = os.path.join(target_dir, new_filename)
            
            try:
                os.rename(old_path, new_path)
                print(f"✓ {filename} -> {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"✗ 重命名失败 {filename}: {e}")
            continue
        
        print(f"? 跳过不匹配的文件: {filename}")
    
    print(f"\n重命名完成! 成功重命名了 {renamed_count} 个文件。")

if __name__ == "__main__":
    rename_character_mats()