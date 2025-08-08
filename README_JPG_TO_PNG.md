# JPG 到 PNG 转换工具

这个工具可以递归地将 character-mats 文件夹中的 JPG 文件转换为 PNG 格式，同时优化文件大小并保持图像质量。

## 功能特点

- **递归转换**: 自动查找并转换所有子目录中的 JPG 文件
- **质量优化**: 提供多种质量级别以平衡文件大小和图像质量
- **智能压缩**: 使用调色板模式和最高压缩级别减小文件大小
- **EXIF 处理**: 自动根据 EXIF 数据旋转图像
- **详细统计**: 显示转换进度和文件大小变化

## 使用方法

### 基本用法

```bash
# 转换 character-mats 文件夹中的所有 JPG 文件（默认使用调色板模式）
python3 jpg_to_png_converter.py

# 指定输入目录
python3 jpg_to_png_converter.py /path/to/your/images

# 指定输出目录
python3 jpg_to_png_converter.py -o /path/to/output
```

### 质量选项

```bash
# 高质量（文件较大，质量最佳）
python3 jpg_to_png_converter.py --quality high

# 中等质量（平衡文件大小和质量）
python3 jpg_to_png_converter.py --quality medium

# 低质量（文件较小，质量降低）
python3 jpg_to_png_converter.py --quality low

# 调色板模式（文件最小，推荐）
python3 jpg_to_png_converter.py --quality palette
```

### 其他选项

```bash
# 预览模式（只显示将要转换的文件，不实际转换）
python3 jpg_to_png_converter.py --preview

# 覆盖已存在的 PNG 文件
python3 jpg_to_png_converter.py --overwrite

# 查看帮助
python3 jpg_to_png_converter.py --help
```

## 质量级别说明

| 级别 | 描述 | 文件大小 | 适用场景 |
|------|------|----------|----------|
| `high` | 保持原始质量，24位真彩色 | 最大 | 需要最高质量的场景 |
| `medium` | 256色调色板，视觉质量良好 | 中等 | 一般用途 |
| `low` | 128色调色板，质量降低 | 较小 | 对质量要求不高的场景 |
| `palette` | 256色调色板+最高压缩 | 最小 | **推荐**，平衡质量和大小 |

## 转换结果

使用调色板模式转换 character-mats 文件夹的结果：

- **转换文件数**: 30 个
- **原始 JPG 总大小**: 30.5 MB
- **转换后 PNG 总大小**: 69.9 MB
- **大小增加**: +129.1%

虽然 PNG 文件比 JPG 大，但 PNG 是无损格式，提供了更好的图像质量和透明度支持。

## 文件大小比较工具

使用 `compare_sizes.py` 脚本可以查看详细的文件大小比较：

```bash
python3 compare_sizes.py
```

## 依赖要求

- Python 3.6+
- Pillow (PIL) 库

安装依赖：
```bash
pip install Pillow
```

## 注意事项

1. **备份原文件**: 转换不会删除原始 JPG 文件
2. **磁盘空间**: PNG 文件通常比 JPG 文件大，确保有足够的磁盘空间
3. **质量选择**: 对于游戏资源，推荐使用 `palette` 模式以获得最佳的大小/质量平衡
4. **批量处理**: 工具支持大量文件的批量转换，会显示进度信息

## 示例输出

```
============================================================
JPG 到 PNG 转换工具
============================================================
输入目录: assets/character-mats
输出目录: 原位置
找到 30 个 JPG 文件
质量级别: palette
跳过已存在文件
------------------------------------------------------------
[1/30] 处理: char_mat_banner_spear_b.jpg
  ✓ 转换成功: char_mat_banner_spear_b.jpg -> char_mat_banner_spear_b.png
    大小: 584,242 -> 1,476,626 字节 (-152.8%)
...
------------------------------------------------------------
转换完成!
总文件数: 30
成功转换: 30
跳过文件: 0
失败文件: 0
总大小变化: 31,985,462 -> 73,282,387 字节 (-129.1%)
```