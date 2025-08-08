#!/usr/bin/env python3
"""
JPG 到 PNG 转换工具
递归转换 character-mats 文件夹中的 JPG 文件为 PNG 格式
优化文件大小的同时保持细节质量
"""

import os
import sys
from PIL import Image, ImageOps
import argparse
from pathlib import Path


def optimize_png(image, quality_level='high'):
    """
    优化 PNG 图像以减小文件大小同时保持质量
    
    Args:
        image (PIL.Image): 输入图像
        quality_level (str): 质量级别 ('high', 'medium', 'low', 'palette')
    
    Returns:
        PIL.Image: 优化后的图像
    """
    # 如果是 RGBA 模式但没有透明度，转换为 RGB
    if image.mode == 'RGBA':
        # 检查是否有真正的透明像素
        if image.getextrema()[3][0] == 255:  # Alpha 通道最小值为 255，说明没有透明度
            # 创建白色背景并合成
            background = Image.new('RGB', image.size, (255, 255, 255))
            image = Image.alpha_composite(background.convert('RGBA'), image).convert('RGB')
    
    # 根据质量级别进行不同的优化
    if quality_level == 'high':
        # 高质量：保持原始质量，只做基本优化
        pass
    elif quality_level == 'medium':
        # 中等质量：使用调色板模式以减小文件大小
        if image.mode == 'RGB':
            # 转换为调色板模式，保留更多颜色
            image = image.quantize(colors=256, method=Image.MEDIANCUT)
    elif quality_level == 'low':
        # 低质量：更激进的压缩
        if image.mode == 'RGB':
            image = image.quantize(colors=128, method=Image.MEDIANCUT)
    elif quality_level == 'palette':
        # 调色板模式：最小文件大小
        if image.mode in ['RGB', 'RGBA']:
            # 先转换为 RGB（如果需要）
            if image.mode == 'RGBA':
                background = Image.new('RGB', image.size, (255, 255, 255))
                image = Image.alpha_composite(background.convert('RGBA'), image).convert('RGB')
            # 转换为调色板模式
            image = image.quantize(colors=256, method=Image.MEDIANCUT)
    
    return image


def convert_jpg_to_png(input_path, output_path, quality_level='high', overwrite=False):
    """
    将 JPG 文件转换为优化的 PNG 文件
    
    Args:
        input_path (str): 输入 JPG 文件路径
        output_path (str): 输出 PNG 文件路径
        quality_level (str): 质量级别
        overwrite (bool): 是否覆盖已存在的文件
    
    Returns:
        dict: 转换结果信息
    """
    try:
        # 检查输出文件是否已存在
        if os.path.exists(output_path) and not overwrite:
            return {
                'success': False,
                'message': f'文件已存在，跳过: {output_path}',
                'skipped': True
            }
        
        # 打开并处理图像
        with Image.open(input_path) as img:
            # 自动旋转图像（基于 EXIF 数据）
            img = ImageOps.exif_transpose(img)
            
            # 优化图像
            optimized_img = optimize_png(img, quality_level)
            
            # 确保输出目录存在
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            # 保存为 PNG，使用优化参数
            save_kwargs = {
                'format': 'PNG',
                'optimize': True,
            }
            
            # 根据图像模式选择最佳压缩
            if optimized_img.mode in ['RGB', 'L']:
                save_kwargs['compress_level'] = 9  # 最高压缩级别
            
            optimized_img.save(output_path, **save_kwargs)
            
            # 获取文件大小信息
            input_size = os.path.getsize(input_path)
            output_size = os.path.getsize(output_path)
            compression_ratio = (1 - output_size / input_size) * 100
            
            return {
                'success': True,
                'input_size': input_size,
                'output_size': output_size,
                'compression_ratio': compression_ratio,
                'message': f'转换成功: {os.path.basename(input_path)} -> {os.path.basename(output_path)}'
            }
            
    except Exception as e:
        return {
            'success': False,
            'message': f'转换失败 {input_path}: {str(e)}',
            'error': str(e)
        }


def find_jpg_files(directory):
    """
    递归查找目录中的所有 JPG 文件
    
    Args:
        directory (str): 搜索目录
    
    Returns:
        list: JPG 文件路径列表
    """
    jpg_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(('.jpg', '.jpeg')):
                jpg_files.append(os.path.join(root, file))
    return jpg_files


def convert_directory(input_dir, output_dir=None, quality_level='high', overwrite=False):
    """
    转换目录中的所有 JPG 文件
    
    Args:
        input_dir (str): 输入目录
        output_dir (str): 输出目录，如果为 None 则在原位置转换
        quality_level (str): 质量级别
        overwrite (bool): 是否覆盖已存在的文件
    
    Returns:
        dict: 转换统计信息
    """
    # 查找所有 JPG 文件
    jpg_files = find_jpg_files(input_dir)
    
    if not jpg_files:
        return {
            'total_files': 0,
            'converted': 0,
            'skipped': 0,
            'failed': 0,
            'message': f'在 {input_dir} 中未找到 JPG 文件'
        }
    
    print(f"找到 {len(jpg_files)} 个 JPG 文件")
    print(f"质量级别: {quality_level}")
    print(f"{'覆盖模式' if overwrite else '跳过已存在文件'}")
    print("-" * 60)
    
    converted = 0
    skipped = 0
    failed = 0
    total_input_size = 0
    total_output_size = 0
    
    for i, jpg_path in enumerate(jpg_files, 1):
        # 生成输出路径
        if output_dir:
            # 保持相对路径结构
            rel_path = os.path.relpath(jpg_path, input_dir)
            png_filename = os.path.splitext(rel_path)[0] + '.png'
            output_path = os.path.join(output_dir, png_filename)
        else:
            # 在原位置转换
            output_path = os.path.splitext(jpg_path)[0] + '.png'
        
        print(f"[{i}/{len(jpg_files)}] 处理: {os.path.basename(jpg_path)}")
        
        # 转换文件
        result = convert_jpg_to_png(jpg_path, output_path, quality_level, overwrite)
        
        if result['success']:
            converted += 1
            total_input_size += result['input_size']
            total_output_size += result['output_size']
            print(f"  ✓ {result['message']}")
            print(f"    大小: {result['input_size']:,} -> {result['output_size']:,} 字节 "
                  f"({result['compression_ratio']:+.1f}%)")
        elif result.get('skipped'):
            skipped += 1
            print(f"  - {result['message']}")
        else:
            failed += 1
            print(f"  ✗ {result['message']}")
    
    print("-" * 60)
    print("转换完成!")
    print(f"总文件数: {len(jpg_files)}")
    print(f"成功转换: {converted}")
    print(f"跳过文件: {skipped}")
    print(f"失败文件: {failed}")
    
    if converted > 0:
        overall_compression = (1 - total_output_size / total_input_size) * 100
        print(f"总大小变化: {total_input_size:,} -> {total_output_size:,} 字节 "
              f"({overall_compression:+.1f}%)")
    
    return {
        'total_files': len(jpg_files),
        'converted': converted,
        'skipped': skipped,
        'failed': failed,
        'total_input_size': total_input_size,
        'total_output_size': total_output_size
    }


def main():
    parser = argparse.ArgumentParser(description="JPG 到 PNG 转换工具")
    parser.add_argument("input_dir", nargs='?', default="assets/character-mats",
                       help="输入目录路径 (默认: assets/character-mats)")
    parser.add_argument("-o", "--output", help="输出目录 (默认: 在原位置转换)")
    parser.add_argument("-q", "--quality", choices=['high', 'medium', 'low', 'palette'], 
                       default='palette', help="质量级别 (默认: palette - 最小文件大小)")
    parser.add_argument("--overwrite", action='store_true', 
                       help="覆盖已存在的 PNG 文件")
    parser.add_argument("--preview", action='store_true',
                       help="预览模式：只显示将要转换的文件，不实际转换")
    
    args = parser.parse_args()
    
    # 检查输入目录
    if not os.path.exists(args.input_dir):
        print(f"错误: 输入目录不存在: {args.input_dir}")
        sys.exit(1)
    
    if not os.path.isdir(args.input_dir):
        print(f"错误: 输入路径不是目录: {args.input_dir}")
        sys.exit(1)
    
    print("=" * 60)
    print("JPG 到 PNG 转换工具")
    print("=" * 60)
    print(f"输入目录: {args.input_dir}")
    print(f"输出目录: {args.output or '原位置'}")
    
    if args.preview:
        # 预览模式
        jpg_files = find_jpg_files(args.input_dir)
        if not jpg_files:
            print(f"在 {args.input_dir} 中未找到 JPG 文件")
            return
        
        print(f"\n找到 {len(jpg_files)} 个 JPG 文件:")
        for jpg_path in jpg_files:
            if args.output:
                rel_path = os.path.relpath(jpg_path, args.input_dir)
                png_filename = os.path.splitext(rel_path)[0] + '.png'
                output_path = os.path.join(args.output, png_filename)
            else:
                output_path = os.path.splitext(jpg_path)[0] + '.png'
            
            size = os.path.getsize(jpg_path)
            print(f"  {jpg_path} ({size:,} 字节) -> {output_path}")
        
        print(f"\n使用 --quality {args.quality} 运行转换")
        return
    
    # 执行转换
    try:
        result = convert_directory(args.input_dir, args.output, args.quality, args.overwrite)
        
        if result['failed'] > 0:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n转换被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()