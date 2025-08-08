#!/usr/bin/env python3
"""
重命名 character-perks/frosthaven 文件夹下的文件
规则：
把 char_perk_*.png 转换为 fh-*-perks.png，把下划线都转换为中横线
"""

import os
import re

def rename_character_perks():
    # 目标目录
    target_dir = "/Users/bytedance/cutter/assets/character-perks/frosthaven"
    
    if not os.path.exists(target_dir):
        print(f"目录不存在: {target_dir}")
        return
    
    # 获取所有文件
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    
    # 过滤出需要重命名的文件（char_perk_*.png 格式）
    files_to_rename = [f for f in files if f.startswith('char_perk_') and f.endswith('.png')]
    
    print(f"找到 {len(files_to_rename)} 个需要重命名的文件:")
    for f in files_to_rename:
        print(f"  - {f}")
    
    print("\n开始重命名...")
    
    renamed_count = 0
    
    for filename in files_to_rename:
        old_path = os.path.join(target_dir, filename)
        
        # 匹配 char_perk_*.png 格式
        match = re.match(r'char_perk_(.+)\.png$', filename)
        if match:
            character_name = match.group(1).replace('_', '-')
            new_filename = f"fh-{character_name}-perks.png"
            new_path = os.path.join(target_dir, new_filename)
            
            try:
                os.rename(old_path, new_path)
                print(f"✓ {filename} -> {new_filename}")
                renamed_count += 1
            except Exception as e:
                print(f"✗ 重命名失败 {filename}: {e}")
        else:
            print(f"? 跳过不匹配的文件: {filename}")
    
    print(f"\n重命名完成! 成功重命名了 {renamed_count} 个文件。")

if __name__ == "__main__":
    rename_character_perks()