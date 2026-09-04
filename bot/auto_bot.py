#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""自动化机器人核心模块"""

import time
import os
from pathlib import Path
from .logger import setup_logger
from .image_utils import ImageUtils

logger = setup_logger(__name__)


class AutoBot:
    """自动化机器人类"""
    
    def __init__(self, config, adb_manager):
        """
        初始化自动化机器人
        
        Args:
            config: 配置字典
            adb_manager: ADB 管理器实例
        """
        self.config = config
        self.adb = adb_manager
        self.image_utils = ImageUtils()
        
        # 从配置获取参数
        self.game_package = config.get("game_package", "com.danshell.game")
        self.screenshot_path = config.get("screenshot_path", "./screenshots")
        self.template_path = config.get("template_path", "./templates")
        self.confidence = config.get("confidence", 0.8)
        self.debug_mode = config.get("debug_mode", False)
        self.click_delay = config.get("click_delay", 1)
        
        # 创建必要的目录
        Path(self.screenshot_path).mkdir(parents=True, exist_ok=True)
        Path(self.template_path).mkdir(parents=True, exist_ok=True)
        
        self.round_count = 0
    
    def take_screenshot(self, name="screen"):
        """
        截屏
        
        Args:
            name: 截图名称
        
        Returns:
            图像数组，失败返回 None
        """
        try:
            output_path = os.path.join(self.screenshot_path, f"{name}_{self.round_count}.png")
            if self.adb.take_screenshot(output_path):
                logger.debug(f"✅ 截图成功: {output_path}")
                return self.image_utils.load_image(output_path)
            else:
                logger.error(f"❌ 截图失败")
                return None
        except Exception as e:
            logger.error(f"❌ 截屏异常: {str(e)}")
            return None
    
    def find_button(self, template_name, screenshot=None):
        """
        查找按钮
        
        Args:
            template_name: 模板文件名（不含路径）
            screenshot: 屏幕截图（可选，如果不提供则会自动截屏）
        
        Returns:
            (x, y) 坐标，未找到返回 None
        """
        try:
            if screenshot is None:
                screenshot = self.take_screenshot()
            
            if screenshot is None:
                logger.error(f"❌ 无法获取屏幕截图")
                return None
            
            # 加载模板
            template_path = os.path.join(self.template_path, template_name)
            if not os.path.exists(template_path):
                logger.warning(f"⚠️  模板文件不存在: {template_path}")
                return None
            
            template = self.image_utils.load_image(template_path)
            if template is None:
                return None
            
            # 查找模板
            matches = self.image_utils.match_template(
                screenshot,
                template,
                confidence=self.confidence
            )
            
            if matches:
                x, y, conf = matches[0]
                logger.debug(f"✅ 找到按钮 {template_name}: ({x}, {y}), 置信度: {conf:.2f}")
                
                if self.debug_mode:
                    # 调试模式下保存标注图像
                    debug_img = screenshot.copy()
                    debug_img = self.image_utils.draw_circle(debug_img, x, y, radius=20, color=(0, 255, 0))
                    debug_path = os.path.join(
                        self.screenshot_path,
                        f"debug_{template_name}_{self.round_count}.png"
                    )
                    self.image_utils.save_image(debug_img, debug_path)
                
                return (x, y)
            else:
                logger.warning(f"⚠️  未找到按钮: {template_name}")
                return None
        
        except Exception as e:
            logger.error(f"❌ 查找按钮异常: {str(e)}")
            return None
    
    def click(self, x, y, delay=None):
        """
        点击屏幕
        
        Args:
            x, y: 坐标
            delay: 延迟时间（可选）
        
        Returns:
            是否成功
        """
        try:
            logger.info(f"👆 点击: ({x}, {y})")
            if self.adb.tap(x, y):
                if delay is None:
                    delay = self.click_delay
                time.sleep(delay)
                return True
            else:
                logger.error(f"❌ 点击失败")
                return False
        except Exception as e:
            logger.error(f"❌ 点击异常: {str(e)}")
            return False
    
    def click_button(self, template_name, delay=None):
        """
        查找并点击按钮
        
        Args:
            template_name: 模板文件名
            delay: 延迟时间（可选）
        
        Returns:
            是否成功
        """
        try:
            pos = self.find_button(template_name)
            if pos:
                return self.click(pos[0], pos[1], delay)
            else:
                logger.warning(f"⚠️  无法找到按钮: {template_name}")
                return False
        except Exception as e:
            logger.error(f"❌ 点击按钮异常: {str(e)}")
            return False
    
    def wait_for_button(self, template_name, timeout=30):
        """
        等待按钮出现
        
        Args:
            template_name: 模板文件名
            timeout: 超时时间（秒）
        
        Returns:
            是否找到
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            pos = self.find_button(template_name)
            if pos:
                logger.info(f"✅ 找到按钮: {template_name}")
                return True
            
            time.sleep(1)
        
        logger.warning(f"⚠️  等待按钮超时: {template_name}")
        return False
    
    def start_game(self):
        """
        启动游戏
        
        Returns:
            是否成功
        """
        try:
            logger.info(f"📱 启动游戏: {self.game_package}")
            
            # 先杀死游戏进程
            self.adb.kill_app(self.game_package)
            time.sleep(1)
            
            # 启动游戏
            if self.adb.start_app(self.game_package):
                logger.info("✅ 游戏启动命令已发送")
                time.sleep(5)  # 等待游戏完全加载
                return True
            else:
                logger.error("❌ 游戏启动失败")
                return False
        except Exception as e:
            logger.error(f"❌ 启动游戏异常: {str(e)}")
            return False
    
    def restart_game(self):
        """重启游戏"""
        logger.info("🔄 重启游戏...")
        self.adb.kill_app(self.game_package)
        time.sleep(2)
        return self.start_game()
    
    def run_one_round(self):
        """
        运行一轮自动化
        
        Returns:
            是否成功
        """
        try:
            self.round_count += 1
            logger.info(f"🎮 开始第 {self.round_count} 轮自动化")
            
            # ==================== 你需要根据游戏界面自定义这部分 ====================
            
            # 1. 截屏并检查当前界面
            screenshot = self.take_screenshot(f"round_{self.round_count}")
            if screenshot is None:
                logger.error("❌ 无法获取截图")
                return False
            
            # 2. 进入主线任务
            logger.info("📌 进入主线任务...")
            if not self.click_button("main_line_button.png", delay=2):
                logger.warning("⚠️  无法进入主线任务，尝试重试")
                time.sleep(2)
            
            # 3. 选择任务关卡
            logger.info("📌 选择任务关卡...")
            if not self.click_button("select_task.png", delay=1):
                logger.warning("⚠️  无法选择任务")
                return False
            
            # 4. 点击开始战斗
            logger.info("📌 开始战斗...")
            if not self.click_button("start_battle.png", delay=3):
                logger.warning("⚠️  无法开始战斗")
                return False
            
            # 5. 等待战斗完成
            logger.info("⏳ 等待战斗完成...")
            if not self.wait_for_button("battle_result.png", timeout=60):
                logger.warning("⚠️  战斗超时")
                return False
            
            time.sleep(2)
            
            # 6. 领取奖励
            logger.info("📌 领取奖励...")
            if not self.click_button("claim_reward.png", delay=2):
                logger.warning("⚠️  无法领取奖励")
            
            # 7. 返回主界面
            logger.info("📌 返回主界面...")
            if not self.click_button("back_button.png", delay=2):
                logger.warning("⚠️  无法返回主界面")
            
            # ==================== 自定义部分结束 ====================
            
            logger.info(f"✅ 第 {self.round_count} 轮完成")
            return True
        
        except Exception as e:
            logger.error(f"❌ 运行一轮异常: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return False
    
    def cleanup(self):
        """清理资源"""
        try:
            logger.info("🧹 清理资源...")
            # 这里可以添加清理代码
            logger.info("✅ 资源清理完成")
        except Exception as e:
            logger.error(f"❌ 清理资源失败: {str(e)}")
