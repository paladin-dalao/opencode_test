#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python 常用库功能集成工具文件
集成模块：os、sys、json、time、datetime、requests、csv、re、shutil、logging
前置依赖：需要安装第三方库 requests（pip install requests）
"""

import os
import sys
import json
import time
import datetime
import requests
import csv
import re
import shutil
import logging

# ======================== 1. 日志配置（logging） ========================
def setup_logger(name: str, log_file: str, level=logging.INFO) -> logging.Logger:
    """
    配置日志记录器，输出到文件和控制台
    :param name: 日志器名称
    :param log_file: 日志文件路径
    :param level: 日志级别（默认 INFO）
    :return: 配置好的 Logger 对象
    """
    # 避免重复添加处理器
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    
    logger.setLevel(level)
    
    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_formatter)
    
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger

# 初始化默认日志器
logger = setup_logger("python_toolkit", "toolkit.log")

# ======================== 2. 文件/目录操作（os、shutil） ========================
def create_dir(dir_path: str) -> bool:
    """
    创建目录（支持多级目录），已存在则不报错
    :param dir_path: 目录路径
    :return: 创建成功返回 True，失败返回 False
    """
    try:
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"目录创建成功/已存在：{dir_path}")
        return True
    except Exception as e:
        logger.error(f"创建目录失败：{e}")
        return False

def copy_file(src_path: str, dst_path: str) -> bool:
    """
    复制文件
    :param src_path: 源文件路径
    :param dst_path: 目标文件路径
    :return: 复制成功返回 True，失败返回 False
    """
    try:
        shutil.copy2(src_path, dst_path)
        logger.info(f"文件复制成功：{src_path} -> {dst_path}")
        return True
    except Exception as e:
        logger.error(f"复制文件失败：{e}")
        return False

def list_files(dir_path: str, ext: str = None) -> list:
    """
    列出指定目录下的文件（可选过滤扩展名）
    :param dir_path: 目录路径
    :param ext: 扩展名过滤（如 .txt）
    :return: 文件路径列表
    """
    file_list = []
    try:
        for file in os.listdir(dir_path):
            file_path = os.path.join(dir_path, file)
            if os.path.isfile(file_path):
                if ext and not file_path.endswith(ext):
                    continue
                file_list.append(file_path)
        logger.info(f"列出目录文件成功：{dir_path}（扩展名过滤：{ext}）")
    except Exception as e:
        logger.error(f"列出目录文件失败：{e}")
    return file_list

# ======================== 3. 时间/日期处理（time、datetime） ========================
def get_current_time(format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    获取当前时间字符串
    :param format: 时间格式（默认 %Y-%m-%d %H:%M:%S）
    :return: 格式化的时间字符串
    """
    try:
        current_time = datetime.datetime.now().strftime(format)
        return current_time
    except Exception as e:
        logger.error(f"获取当前时间失败：{e}")
        return ""

def timestamp_to_datetime(timestamp: float, format: str = "%Y-%m-%d %H:%M:%S") -> str:
    """
    时间戳转换为日期时间字符串
    :param timestamp: 时间戳（秒级）
    :param format: 时间格式
    :return: 格式化的时间字符串
    """
    try:
        dt = datetime.datetime.fromtimestamp(timestamp)
        return dt.strftime(format)
    except Exception as e:
        logger.error(f"时间戳转换失败：{e}")
        return ""

# ======================== 4. 网络请求（requests） ========================
def http_get(url: str, params: dict = None, headers: dict = None) -> dict:
    """
    发送 HTTP GET 请求
    :param url: 请求 URL
    :param params: 请求参数
    :param headers: 请求头
    :return: 响应结果（字典，包含 status_code 和 data）
    """
    result = {"status_code": 0, "data": None, "error": ""}
    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        result["status_code"] = response.status_code
        # 尝试解析 JSON，失败则返回文本
        try:
            result["data"] = response.json()
        except:
            result["data"] = response.text
        logger.info(f"GET 请求成功：{url}（状态码：{response.status_code}）")
    except Exception as e:
        result["error"] = str(e)
        logger.error(f"GET 请求失败：{e}")
    return result

def http_post(url: str, data: dict = None, json_data: dict = None, headers: dict = None) -> dict:
    """
    发送 HTTP POST 请求
    :param url: 请求 URL
    :param data: form 表单数据
    :param json_data: JSON 数据
    :param headers: 请求头
    :return: 响应结果（字典，包含 status_code 和 data）
    """
    result = {"status_code": 0, "data": None, "error": ""}
    try:
        response = requests.post(
            url, data=data, json=json_data, headers=headers, timeout=10
        )
        result["status_code"] = response.status_code
        # 尝试解析 JSON，失败则返回文本
        try:
            result["data"] = response.json()
        except:
            result["data"] = response.text
        logger.info(f"POST 请求成功：{url}（状态码：{response.status_code}）")
    except Exception as e:
        result["error"] = str(e)
        logger.error(f"POST 请求失败：{e}")
    return result

# ======================== 5. 数据解析（json、csv、re） ========================
def read_json(file_path: str) -> dict:
    """
    读取 JSON 文件
    :param file_path: 文件路径
    :return: JSON 数据字典（失败返回空字典）
    """
    data = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        logger.info(f"读取 JSON 文件成功：{file_path}")
    except Exception as e:
        logger.error(f"读取 JSON 文件失败：{e}")
    return data

def write_json(file_path: str, data: dict, indent: int = 4) -> bool:
    """
    写入 JSON 文件
    :param file_path: 文件路径
    :param data: 要写入的字典数据
    :param indent: 缩进空格数
    :return: 写入成功返回 True，失败返回 False
    """
    try:
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=indent)
        logger.info(f"写入 JSON 文件成功：{file_path}")
        return True
    except Exception as e:
        logger.error(f"写入 JSON 文件失败：{e}")
        return False

def read_csv(file_path: str, delimiter: str = ",") -> list:
    """
    读取 CSV 文件
    :param file_path: 文件路径
    :param delimiter: 分隔符（默认逗号）
    :return: 数据列表（每行是一个字典）
    """
    data = []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f, delimiter=delimiter)
            for row in reader:
                data.append(dict(row))
        logger.info(f"读取 CSV 文件成功：{file_path}")
    except Exception as e:
        logger.error(f"读取 CSV 文件失败：{e}")
    return data

def regex_match(pattern: str, text: str) -> list:
    """
    正则表达式匹配
    :param pattern: 正则表达式
    :param text: 要匹配的文本
    :return: 匹配结果列表
    """
    try:
        matches = re.findall(pattern, text)
        logger.info(f"正则匹配成功：匹配到 {len(matches)} 个结果")
        return matches
    except Exception as e:
        logger.error(f"正则匹配失败：{e}")
        return []

# ======================== 6. 系统信息（sys、os） ========================
def get_system_info() -> dict:
    """
    获取系统基础信息
    :return: 系统信息字典
    """
    info = {
        "python_version": sys.version,
        "platform": sys.platform,
        "current_dir": os.getcwd(),
        "cpu_count": os.cpu_count(),
        "env_path": os.environ.get("PATH", "")
    }
    logger.info("获取系统信息成功")
    return info

# 测试代码（仅在直接运行该文件时执行）
if __name__ == "__main__":
    # 示例：调用各功能
    print("=== 测试工具文件功能 ===")
    
    # 1. 日志测试
    logger.info("开始测试工具文件")
    
    # 2. 时间测试
    print("当前时间：", get_current_time())
    
    # 3. 文件操作测试
    create_dir("test_dir")
    
    # 4. 系统信息测试
    sys_info = get_system_info()
    print("Python 版本：", sys_info["python_version"])
    
    # 5. 网络请求测试（示例：请求百度）
    response = http_get("https://www.baidu.com")
    print("百度请求状态码：", response["status_code"])
    
    logger.info("工具文件测试完成")
