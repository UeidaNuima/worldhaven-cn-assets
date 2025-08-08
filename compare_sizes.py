#!/usr/bin/env python3
"""
比较 JPG 和 PNG 文件大小的脚本
"""

import os
import glob

def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def compare_files():
    """比较 character-mats 文件夹中的 JPG 和 PNG 文件"""
    base_dir = "assets/character-mats"
    
    # 查找所有 JPG 文件
    jpg_files = glob.glob(os.path.join(base_dir, "**/*.jpg"), recursive=True)
    
    print("=" * 80)
    print("JPG 到 PNG 转换结果比较")
    print("=" * 80)
    print(f"{'文件名':<30} {'JPG大小':<12} {'PNG大小':<12} {'变化':<10} {'比例':<8}")
    print("-" * 80)
    
    total_jpg_size = 0
    total_png_size = 0
    converted_count = 0
    
    for jpg_path in sorted(jpg_files):
        # 生成对应的 PNG 文件路径
        png_path = os.path.splitext(jpg_path)[0] + '.png'
        
        if os.path.exists(png_path):
            jpg_size = os.path.getsize(jpg_path)
            png_size = os.path.getsize(png_path)
            
            size_change = png_size - jpg_size
            size_ratio = (png_size / jpg_size) * 100
            
            filename = os.path.basename(jpg_path)
            
            print(f"{filename:<30} {format_size(jpg_size):<12} {format_size(png_size):<12} "
                  f"{format_size(size_change):<10} {size_ratio:.1f}%")
            
            total_jpg_size += jpg_size
            total_png_size += png_size
            converted_count += 1
    
    print("-" * 80)
    print(f"{'总计':<30} {format_size(total_jpg_size):<12} {format_size(total_png_size):<12} "
          f"{format_size(total_png_size - total_jpg_size):<10} {(total_png_size / total_jpg_size) * 100:.1f}%")
    
    print(f"\n转换统计:")
    print(f"  转换文件数: {converted_count}")
    print(f"  总 JPG 大小: {format_size(total_jpg_size)}")
    print(f"  总 PNG 大小: {format_size(total_png_size)}")
    print(f"  大小变化: {format_size(total_png_size - total_jpg_size)} ({((total_png_size / total_jpg_size) - 1) * 100:+.1f}%)")

if __name__ == "__main__":
    compare_files()