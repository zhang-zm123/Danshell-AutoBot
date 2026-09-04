#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""调试工具 - 实时显示屏幕和识别结果"""

import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from bot.adb_manager import ADBManager
from bot.image_utils import ImageUtils
from bot.logger import setup_logger

logger = setup_logger(__name__)


def debug_mode():
    """调试模式"""
    # 加载配置
    with open("config.json", "r", encoding="utf-8") as f:
        config = json.load(f)
    
    adb = ADBManager(config)
    img_util = ImageUtils()
    
    logger.info("🔍 进入调试模式")
    logger.info(f"📱 设备 ID: {adb.device_id}")
    logger.info("⏳ 每 3 秒截一次屏...")
    logger.info("按 Ctrl+C 退出")
    
    try:
        count = 0
        while True:
            count += 1
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            output_path = f"screenshots/debug_{timestamp}_{count}.png"
            
            logger.info(f"\n🎬 第 {count} 次截屏: {output_path}")
            
            if adb.take_screenshot(output_path):
                logger.info(f"✅ 截屏成功")
                
                # 显示图像大小
                img = img_util.load_image(output_path)
                if img is not None:
                    h, w = img.shape[:2]
                    logger.info(f"   分辨率: {w}x{h}")
            else:
                logger.error(f"❌ 截屏失败")
            
            logger.info("⏳ 3 秒后继续...")
            time.sleep(3)
    
    except KeyboardInterrupt:
        logger.info("\n✅ 调试模式结束")


if __name__ == "__main__":
    debug_mode()
