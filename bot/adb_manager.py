#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ADB 管理器模块"""

import subprocess
import os
import platform
from pathlib import Path
from .logger import setup_logger

logger = setup_logger(__name__)


class ADBManager:
    """ADB 管理器类"""
    
    def __init__(self, config):
        """
        初始化 ADB 管理器
        
        Args:
            config: 配置字典
        """
        self.config = config
        self.device_id = config.get("device_id", "emulator-5554")
        self.adb_path = self.find_adb()
    
    def find_adb(self):
        """查找 ADB 路径"""
        # 检查环境变量中的 adb
        adb_path = None
        
        if platform.system() == "Windows":
            # Windows 上检查常见位置
            common_paths = [
                "adb.exe",
                "C:\\android-sdk\\platform-tools\\adb.exe",
                "C:\\Program Files\\Android\\Android Studio\\platform-tools\\adb.exe",
                os.path.expanduser("~\\AppData\\Local\\Android\\Sdk\\platform-tools\\adb.exe"),
            ]
            for path in common_paths:
                if os.path.exists(path):
                    adb_path = path
                    break
        else:
            # Unix-like 系统
            result = subprocess.run(["which", "adb"], capture_output=True, text=True)
            if result.returncode == 0:
                adb_path = result.stdout.strip()
        
        # 尝试直接调用 adb
        if not adb_path:
            adb_path = "adb"
        
        return adb_path
    
    def check_adb(self):
        """检查 ADB 是否可用"""
        try:
            result = subprocess.run(
                [self.adb_path, "version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"❌ ADB 检查失败: {str(e)}")
            return False
    
    def get_devices(self):
        """获取已连接的设备列表"""
        try:
            result = subprocess.run(
                [self.adb_path, "devices"],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            devices = []
            for line in result.stdout.split('\n')[1:]:
                line = line.strip()
                if line and not line.startswith('*'):
                    device_id, status = line.split()
                    if status == "device":
                        devices.append(device_id)
            
            return devices
        except Exception as e:
            logger.error(f"❌ 获取设备列表失败: {str(e)}")
            return []
    
    def is_device_connected(self):
        """检查设备是否已连接"""
        devices = self.get_devices()
        return self.device_id in devices or len(devices) > 0
    
    def execute_shell(self, command):
        """
        执行 shell 命令
        
        Args:
            command: shell 命令
        
        Returns:
            输出结果
        """
        try:
            cmd = [self.adb_path, "-s", self.device_id, "shell"] + command.split()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.stdout, result.returncode
        except Exception as e:
            logger.error(f"❌ 执行 shell 命令失败: {str(e)}")
            return "", 1
    
    def take_screenshot(self, output_path="screen.png"):
        """
        截屏
        
        Args:
            output_path: 输出文件路径
        
        Returns:
            是否成功
        """
        try:
            # 截屏到设备
            self.execute_shell(f"screencap -p /sdcard/{output_path}")
            
            # 从设备拉取文件
            cmd = [
                self.adb_path,
                "-s",
                self.device_id,
                "pull",
                f"/sdcard/{output_path}",
                output_path
            ]
            result = subprocess.run(cmd, capture_output=True, timeout=10)
            return result.returncode == 0
        except Exception as e:
            logger.error(f"❌ 截屏失败: {str(e)}")
            return False
    
    def tap(self, x, y):
        """
        点击屏幕
        
        Args:
            x: x 坐标
            y: y 坐标
        
        Returns:
            是否成功
        """
        try:
            output, code = self.execute_shell(f"input tap {int(x)} {int(y)}")
            return code == 0
        except Exception as e:
            logger.error(f"❌ 点击失败: {str(e)}")
            return False
    
    def swipe(self, x1, y1, x2, y2, duration=500):
        """
        滑动屏幕
        
        Args:
            x1, y1: 起始坐标
            x2, y2: 结束坐标
            duration: 持续时间（毫秒）
        
        Returns:
            是否成功
        """
        try:
            output, code = self.execute_shell(
                f"input swipe {int(x1)} {int(y1)} {int(x2)} {int(y2)} {int(duration)}"
            )
            return code == 0
        except Exception as e:
            logger.error(f"❌ 滑动失败: {str(e)}")
            return False
    
    def start_app(self, package_name, activity_name=None):
        """
        启动应用
        
        Args:
            package_name: 包名
            activity_name: 活动名（可选）
        
        Returns:
            是否成功
        """
        try:
            if activity_name:
                intent = f"{package_name}/{activity_name}"
            else:
                intent = package_name
            
            output, code = self.execute_shell(f"am start -n {intent}")
            return code == 0
        except Exception as e:
            logger.error(f"❌ 启动应用失败: {str(e)}")
            return False
    
    def kill_app(self, package_name):
        """
        杀死应用进程
        
        Args:
            package_name: 包名
        
        Returns:
            是否成功
        """
        try:
            output, code = self.execute_shell(f"am force-stop {package_name}")
            return code == 0
        except Exception as e:
            logger.error(f"❌ 杀死应用失败: {str(e)}")
            return False
    
    def get_screen_resolution(self):
        """
        获取屏幕分辨率
        
        Returns:
            (width, height) 元组
        """
        try:
            output, code = self.execute_shell("wm size")
            if code == 0:
                # 解析输出格式: "Physical size: 1080x2340"
                parts = output.split(":")[-1].strip().split("x")
                return (int(parts[0]), int(parts[1]))
        except Exception as e:
            logger.error(f"❌ 获取屏幕分辨率失败: {str(e)}")
        
        # 返回默认值
        return (1080, 2340)
