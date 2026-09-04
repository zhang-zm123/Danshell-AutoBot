#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""坐标查找工具 - 用于查找屏幕上点击位置的坐标"""

import sys
import os
import json
import cv2

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.adb_manager import ADBManager
from bot.image_utils import ImageUtils
from bot.logger import setup_logger

logger = setup_logger(__name__)


class CoordinateFinder:
    """坐标查找器"""
    
    def __init__(self, config_path="config.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = json.load(f)
        
        self.adb = ADBManager(self.config)
        self.img_util = ImageUtils()
        self.selected_points = []
    
    def on_mouse(self, event, x, y, flags, param):
        """鼠标事件回调"""
        if event == cv2.EVENT_LBUTTONDOWN:
            self.selected_points.append((x, y))
            logger.info(f"✅ 选中点: ({x}, {y})")
    
    def find_coordinates(self):
        """找坐标"""
        logger.info("🎯 坐标查找工具启动")
        logger.info("📸 正在截屏...")
        
        # 截屏
        screenshot_path = "temp_screenshot.png"
        if not self.adb.take_screenshot(screenshot_path):
            logger.error("❌ 截屏失败")
            return
        
        # 加载图像
        img = self.img_util.load_image(screenshot_path)
        if img is None:
            logger.error("❌ 无法加载图像")
            return
        
        logger.info(f"✅ 截屏成功: {screenshot_path}")
        logger.info(f"📐 分辨率: {img.shape[1]}x{img.shape[0]}")
        logger.info("\n🖱️  使用说明:")
        logger.info("   - 在图像上左键点击选择坐标")
        logger.info("   - 按 ESC 键退出")
        
        # 显示图像
        cv2.namedWindow("Coordinate Finder", cv2.WINDOW_NORMAL)
        cv2.setMouseCallback("Coordinate Finder", self.on_mouse)
        cv2.imshow("Coordinate Finder", img)
        
        while True:
            key = cv2.waitKey(1) & 0xFF
            if key == 27:  # ESC 键
                break
        
        cv2.destroyAllWindows()
        
        # 输出结果
        if self.selected_points:
            logger.info(f"\n📍 选中的坐标:")
            for i, (x, y) in enumerate(self.selected_points):
                logger.info(f"   点 {i+1}: ({x}, {y})")
            
            # 保存到文件
            output = {
                "coordinates": self.selected_points,
                "resolution": (img.shape[1], img.shape[0])
            }
            
            with open("coordinates.json", "w") as f:
                json.dump(output, f, indent=2)
            
            logger.info(f"✅ 坐标已保存到 coordinates.json")
        else:
            logger.info("⚠️  未选中任何坐标")
        
        # 清理临时文件
        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)


if __name__ == "__main__":
    finder = CoordinateFinder()
    finder.find_coordinates()
