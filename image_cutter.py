#!/usr/bin/env python3
"""
图片切分工具
用于将一张图片按指定的行列数切分成多张小图片
"""

import os
import sys
from PIL import Image
import argparse


def cut_image(image_path, rows, cols, output_dir=None):
    """
    将图片切分成指定行列数的小图片
    
    Args:
        image_path (str): 输入图片路径
        rows (int): 切分行数
        cols (int): 切分列数
        output_dir (str): 输出目录，默认为输入图片同目录下的 'cut_images' 文件夹
    
    Returns:
        list: 生成的图片文件路径列表
    """
    # 检查输入文件是否存在
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"图片文件不存在: {image_path}")
    
    # 打开图片
    try:
        img = Image.open(image_path)
        print(f"原图尺寸: {img.size[0]} x {img.size[1]} 像素")
    except Exception as e:
        raise Exception(f"无法打开图片文件: {e}")
    
    # 设置输出目录
    if output_dir is None:
        base_dir = os.path.dirname(image_path)
        base_name = os.path.splitext(os.path.basename(image_path))[0]
        output_dir = os.path.join(base_dir, f"{base_name}_cut_images")
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    print(f"输出目录: {output_dir}")
    
    # 计算每个小图片的尺寸
    img_width, img_height = img.size
    piece_width = img_width // cols
    piece_height = img_height // rows
    
    print(f"切分为 {rows} 行 {cols} 列，每个小图片尺寸: {piece_width} x {piece_height} 像素")
    
    # 切分图片
    output_files = []
    for row in range(rows):
        for col in range(cols):
            # 计算切分区域
            left = col * piece_width
            top = row * piece_height
            right = left + piece_width
            bottom = top + piece_height
            
            # 如果是最后一列或最后一行，确保包含剩余像素
            if col == cols - 1:
                right = img_width
            if row == rows - 1:
                bottom = img_height
            
            # 切分图片
            piece = img.crop((left, top, right, bottom))
            
            # 生成输出文件名
            output_filename = f"piece_{row+1:02d}_{col+1:02d}.png"
            output_path = os.path.join(output_dir, output_filename)
            
            # 保存图片
            piece.save(output_path)
            output_files.append(output_path)
            
            print(f"已生成: {output_filename} (位置: 第{row+1}行第{col+1}列)")
    
    print(f"\n切分完成！共生成 {len(output_files)} 张图片")
    return output_files


def main():
    parser = argparse.ArgumentParser(description="图片切分工具")
    parser.add_argument("image_path", help="输入图片路径")
    parser.add_argument("rows", type=int, help="切分行数")
    parser.add_argument("cols", type=int, help="切分列数")
    parser.add_argument("-o", "--output", help="输出目录")
    
    args = parser.parse_args()
    
    try:
        output_files = cut_image(args.image_path, args.rows, args.cols, args.output)
        print(f"\n所有图片已保存到: {os.path.dirname(output_files[0])}")
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()