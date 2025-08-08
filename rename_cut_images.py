#!/usr/bin/env python3
"""
通用的切片图片重命名工具
支持将 piece_XX_YY.png 格式重命名为 fh-{prefix}-{number}-{suffix}.png 格式
"""

import os
import re
import argparse

def rename_cut_images(target_dir, prefix, suffix, start_number=1):
    """
    重命名切片图片
    
    Args:
        target_dir: 目标目录
        prefix: 前缀 (如 'be' 表示 boat event)
        suffix: 后缀 (如 'f' 表示 front, 'b' 表示 back)
        start_number: 起始编号 (默认为1)
    """
    
    if not os.path.exists(target_dir):
        print(f"目录不存在: {target_dir}")
        return
    
    # 获取所有文件
    files = [f for f in os.listdir(target_dir) if os.path.isfile(os.path.join(target_dir, f))]
    
    # 过滤出需要重命名的文件（piece_XX_XX.png 格式）
    files_to_rename = [f for f in files if f.startswith('piece_') and f.endswith('.png')]
    
    print(f"找到 {len(files_to_rename)} 个需要重命名的文件:")
    for f in sorted(files_to_rename):
        print(f"  - {f}")
    
    print(f"\n开始重命名为 fh-{prefix}-XX-{suffix}.png 格式...")
    
    renamed_count = 0
    
    for filename in sorted(files_to_rename):
        old_path = os.path.join(target_dir, filename)
        
        # 匹配 piece_XX_YY.png 格式
        match = re.match(r'piece_(\d+)_(\d+)\.png$', filename)
        if match:
            row = int(match.group(1))
            col = int(match.group(2))
            
            # 根据规则计算新的编号
            # 通用公式：piece_XX_YY.png -> fh-{prefix}-(start_number+(XX-1)*10+YY-1)-{suffix}.png
            new_number = start_number + (row - 1) * 10 + col - 1
            
            new_filename = f"fh-{prefix}-{new_number:02d}-{suffix}.png"
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

def main():
    parser = argparse.ArgumentParser(description='重命名切片图片文件')
    parser.add_argument('directory', help='目标目录路径')
    parser.add_argument('prefix', help='文件名前缀 (如: be, oe, re)')
    parser.add_argument('suffix', help='文件名后缀 (如: f, b)')
    parser.add_argument('--start', type=int, default=1, help='起始编号 (默认为1)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("通用切片图片重命名工具")
    print("=" * 60)
    print(f"目标目录: {args.directory}")
    print(f"前缀: {args.prefix}")
    print(f"后缀: {args.suffix}")
    print(f"起始编号: {args.start}")
    print(f"格式: piece_XX_YY.png -> fh-{args.prefix}-{args.start}+-{args.suffix}.png")
    print("-" * 60)
    
    rename_cut_images(args.directory, args.prefix, args.suffix, args.start)

if __name__ == "__main__":
    main()