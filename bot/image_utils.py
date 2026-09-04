#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""图像识别工具模块"""

import cv2
import numpy as np
from pathlib import Path
from .logger import setup_logger

logger = setup_logger(__name__)


class ImageUtils:
    """图像处理和识别工具类"""
    
    @staticmethod
    def load_image(image_path, gray=False):
        """
        加载图像
        
        Args:
            image_path: 图像文件路径
            gray: 是否转为灰度图
        
        Returns:
            图像数组，如果加载失败返回 None
        """
        try:
            img = cv2.imread(image_path)
            if img is None:
                logger.error(f"❌ 图像加载失败: {image_path}")
                return None
            
            if gray:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            return img
        except Exception as e:
            logger.error(f"❌ 加载图像异常: {str(e)}")
            return None
    
    @staticmethod
    def save_image(image, output_path):
        """
        保存图像
        
        Args:
            image: 图像数组
            output_path: 输出文件路径
        
        Returns:
            是否成功
        """
        try:
            # 创建目录
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(output_path, image)
            logger.debug(f"✅ 图像已保存: {output_path}")
            return True
        except Exception as e:
            logger.error(f"❌ 保存图像失败: {str(e)}")
            return False
    
    @staticmethod
    def match_template(screen, template, confidence=0.8):
        """
        模板匹配
        
        Args:
            screen: 屏幕截图（彩色）
            template: 模板图像（彩色）
            confidence: 置信度阈值 (0-1)
        
        Returns:
            匹配结果列表 [(x, y, confidence), ...]
        """
        try:
            # 转为灰度图进行匹配
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            
            # 模板匹配
            result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # 计算置信度 (0-1)
            conf = max_val / (template_gray.shape[0] * template_gray.shape[1])
            
            if conf >= confidence:
                h, w = template_gray.shape
                # 返回矩形中心点
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                return [(center_x, center_y, conf)]
            
            return []
        except Exception as e:
            logger.error(f"❌ 模板匹配失败: {str(e)}")
            return []
    
    @staticmethod
    def find_all_templates(screen, template, confidence=0.8):
        """
        找到屏幕上所有匹配的模板位置
        
        Args:
            screen: 屏幕截图（彩色）
            template: 模板图像（彩色）
            confidence: 置信度阈值
        
        Returns:
            匹配位置列表
        """
        try:
            screen_gray = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            
            result = cv2.matchTemplate(screen_gray, template_gray, cv2.TM_CCOEFF)
            
            # 获取所有超过阈值的位置
            threshold = confidence * (template_gray.shape[0] * template_gray.shape[1])
            locations = np.where(result >= threshold)
            
            h, w = template_gray.shape
            matches = []
            for pt in zip(*locations[::-1]):
                center_x = pt[0] + w // 2
                center_y = pt[1] + h // 2
                matches.append((center_x, center_y))
            
            return matches
        except Exception as e:
            logger.error(f"❌ 查找所有模板失败: {str(e)}")
            return []
    
    @staticmethod
    def detect_color(screen, lower_hsv, upper_hsv):
        """
        检测特定颜色的区域
        
        Args:
            screen: 屏幕截图
            lower_hsv: 下界 HSV 值
            upper_hsv: 上界 HSV 值
        
        Returns:
            掩码图像
        """
        try:
            # 转为 HSV 颜色空间
            hsv = cv2.cvtColor(screen, cv2.COLOR_BGR2HSV)
            
            # 根据颜色范围创建掩码
            mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
            
            return mask
        except Exception as e:
            logger.error(f"❌ 颜色检测失败: {str(e)}")
            return None
    
    @staticmethod
    def find_contours(mask, min_area=100):
        """
        查找轮廓
        
        Args:
            mask: 二值掩码
            min_area: 最小面积阈值
        
        Returns:
            轮廓列表
        """
        try:
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
            valid_contours = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area >= min_area:
                    x, y, w, h = cv2.boundingRect(cnt)
                    valid_contours.append({
                        'contour': cnt,
                        'area': area,
                        'x': x,
                        'y': y,
                        'w': w,
                        'h': h,
                        'center_x': x + w // 2,
                        'center_y': y + h // 2
                    })
            
            return valid_contours
        except Exception as e:
            logger.error(f"❌ 查找轮廓失败: {str(e)}")
            return []
    
    @staticmethod
    def draw_rect(image, x, y, w, h, color=(0, 255, 0), thickness=2):
        """
        绘制矩形框
        
        Args:
            image: 图像
            x, y: 左上角坐标
            w, h: 宽和高
            color: 颜色 (B, G, R)
            thickness: 线条厚度
        
        Returns:
            修改后的图像
        """
        return cv2.rectangle(image, (x, y), (x + w, y + h), color, thickness)
    
    @staticmethod
    def draw_circle(image, x, y, radius=5, color=(0, 255, 0), thickness=2):
        """
        绘制圆形
        
        Args:
            image: 图像
            x, y: 圆心坐标
            radius: 半径
            color: 颜色
            thickness: 线条厚度
        
        Returns:
            修改后的图像
        """
        return cv2.circle(image, (int(x), int(y)), radius, color, thickness)
    
    @staticmethod
    def draw_text(image, text, x, y, font_scale=1, color=(255, 255, 255), thickness=2):
        """
        绘制文本
        
        Args:
            image: 图像
            text: 文本内容
            x, y: 文本位置
            font_scale: 字体大小
            color: 颜色
            thickness: 厚度
        
        Returns:
            修改后的图像
        """
        font = cv2.FONT_HERSHEY_SIMPLEX
        return cv2.putText(image, text, (int(x), int(y)), font, font_scale, color, thickness)
    
    @staticmethod
    def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
        """
        调整图像大小
        
        Args:
            image: 图像
            width: 目标宽度
            height: 目标高度
            inter: 插值方法
        
        Returns:
            调整后的图像
        """
        h, w = image.shape[:2]
        
        if width is None and height is None:
            return image
        
        if width is None:
            ratio = height / float(h)
            width = int(w * ratio)
        elif height is None:
            ratio = width / float(w)
            height = int(h * ratio)
        
        return cv2.resize(image, (width, height), interpolation=inter)
    
    @staticmethod
    def crop(image, x, y, w, h):
        """
        裁剪图像
        
        Args:
            image: 图像
            x, y: 起始坐标
            w, h: 宽和高
        
        Returns:
            裁剪后的图像
        """
        return image[int(y):int(y+h), int(x):int(x+w)]
