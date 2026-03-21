#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数据加载工具模块
"""

import pandas as pd
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent.parent))
from config.settings import RAW_DATA_DIR, PROCESSED_DATA_DIR, EXPORTS_DIR

class DataLoader:
    """数据加载器类"""
    
    def __init__(self):
        self.raw_data_dir = RAW_DATA_DIR
        self.processed_data_dir = PROCESSED_DATA_DIR
        self.exports_dir = EXPORTS_DIR
    
    def load_csv(self, filename: str, data_type: str = "processed") -> pd.DataFrame:
        """
        加载CSV文件
        
        Args:
            filename: 文件名
            data_type: 数据类型 ('raw', 'processed', 'exports')
        
        Returns:
            pandas DataFrame
        """
        if data_type == "raw":
            filepath = self.raw_data_dir / filename
        elif data_type == "processed":
            filepath = self.processed_data_dir / filename
        elif data_type == "exports":
            filepath = self.exports_dir / filename
        else:
            raise ValueError("data_type must be 'raw', 'processed', or 'exports'")
        
        if not filepath.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        return pd.read_csv(filepath, encoding='utf-8-sig')
    
    def save_csv(self, df: pd.DataFrame, filename: str, data_type: str = "processed"):
        """
        保存DataFrame为CSV文件
        
        Args:
            df: pandas DataFrame
            filename: 文件名
            data_type: 数据类型 ('processed', 'exports')
        """
        if data_type == "processed":
            filepath = self.processed_data_dir / filename
        elif data_type == "exports":
            filepath = self.exports_dir / filename
        else:
            raise ValueError("data_type must be 'processed' or 'exports'")
        
        # 确保目录存在
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(filepath, index=False, encoding='utf-8-sig')
        print(f"数据已保存到: {filepath}")
    
    def load_json(self, filename: str, data_type: str = "processed") -> Dict:
        """
        加载JSON文件
        
        Args:
            filename: 文件名
            data_type: 数据类型 ('raw', 'processed')
        
        Returns:
            字典数据
        """
        if data_type == "raw":
            filepath = self.raw_data_dir / filename
        elif data_type == "processed":
            filepath = self.processed_data_dir / filename
        else:
            raise ValueError("data_type must be 'raw' or 'processed'")
        
        if not filepath.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save_json(self, data: Dict, filename: str, data_type: str = "processed"):
        """
        保存数据为JSON文件
        
        Args:
            data: 字典数据
            filename: 文件名
            data_type: 数据类型 ('processed')
        """
        if data_type == "processed":
            filepath = self.processed_data_dir / filename
        else:
            raise ValueError("data_type must be 'processed'")
        
        # 确保目录存在
        filepath.parent.mkdir(parents=True, exist_ok=True)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"数据已保存到: {filepath}")
    
    def load_excel(self, filename: str, sheet_name: Optional[str] = None, data_type: str = "raw") -> Union[pd.DataFrame, Dict]:
        """
        加载Excel文件
        
        Args:
            filename: 文件名
            sheet_name: 工作表名称，None表示加载所有工作表
            data_type: 数据类型 ('raw', 'processed')
        
        Returns:
            pandas DataFrame 或 字典（多个工作表）
        """
        if data_type == "raw":
            filepath = self.raw_data_dir / filename
        elif data_type == "processed":
            filepath = self.processed_data_dir / filename
        else:
            raise ValueError("data_type must be 'raw' or 'processed'")
        
        if not filepath.exists():
            raise FileNotFoundError(f"文件不存在: {filepath}")
        
        return pd.read_excel(filepath, sheet_name=sheet_name)
    
    def get_file_list(self, data_type: str = "processed", extension: str = None) -> List[str]:
        """
        获取指定目录下的文件列表
        
        Args:
            data_type: 数据类型 ('raw', 'processed', 'exports')
            extension: 文件扩展名过滤，如 '.csv', '.json'
        
        Returns:
            文件名列表
        """
        if data_type == "raw":
            directory = self.raw_data_dir
        elif data_type == "processed":
            directory = self.processed_data_dir
        elif data_type == "exports":
            directory = self.exports_dir
        else:
            raise ValueError("data_type must be 'raw', 'processed', or 'exports'")
        
        if not directory.exists():
            return []
        
        files = []
        for file_path in directory.iterdir():
            if file_path.is_file():
                if extension is None or file_path.suffix == extension:
                    files.append(file_path.name)
        
        return sorted(files)

# 创建全局数据加载器实例
data_loader = DataLoader()

if __name__ == "__main__":
    # 测试数据加载器
    print("数据加载器测试:")
    print(f"Raw data files: {data_loader.get_file_list('raw')}")
    print(f"Processed data files: {data_loader.get_file_list('processed')}")
    print(f"Export files: {data_loader.get_file_list('exports')}") 