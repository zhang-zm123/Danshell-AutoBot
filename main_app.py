"""
弹壳特工队自动刷主线任务 - Kivy Android APP
可生成 APK 安装包直接安装到手机

使用 Kivy 框架开发
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.uix.togglebutton import ToggleButton

import threading
import time
from datetime import datetime


# 设置窗口大小
Window.size = (720, 1280)


class DanshellAutoBotApp(App):
    """APP 主类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "弹壳特工队自动刷主线"
        
        # 运行状态
        self.is_running = False
        self.thread = None
        
        # 配置
        self.config = {
            'loop_count': 10,
            'loop_delay': 3,
            'click_delay': 1,
            'debug_mode': True
        }
        
        # 日志
        self.logs = []
    
    def log(self, message, level="INFO"):
        """记录日志"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] [{level}] {message}"
        self.logs.append(log_msg)
        
        # 更新 UI
        if hasattr(self, 'log_display'):
            self.log_display.text += log_msg + "\n"
            # 自动滚到底部
            self.log_scroll.scroll_y = 0
    
    def build(self):
        """构建 UI"""
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # ==================== 顶部 - 标题 ====================
        title_layout = BoxLayout(size_hint_y=0.1)
        title = Label(
            text='🎮 弹壳特工队自动刷主线',
            font_size='24sp',
            bold=True,
            color=(0.2, 0.6, 1, 1)
        )
        title_layout.add_widget(title)
        main_layout.add_widget(title_layout)
        
        # ==================== 中部 - 配置选项 ====================
        config_scroll = ScrollView(size_hint=(1, 0.35))
        config_layout = GridLayout(cols=2, spacing=10, size_hint_y=None)
        config_layout.bind(minimum_height=config_layout.setter('height'))
        
        # 循环次数
        config_layout.add_widget(Label(text='循环次数:', size_hint_y=None, height=50))
        loop_spinner = Spinner(
            text='10',
            values=('1', '5', '10', '20', '30', '50', '100'),
            size_hint_y=None,
            height=50
        )
        loop_spinner.bind(text=self.on_loop_count_change)
        config_layout.add_widget(loop_spinner)
        self.loop_spinner = loop_spinner
        
        # 轮次延迟
        config_layout.add_widget(Label(text='轮次延迟(秒):', size_hint_y=None, height=50))
        delay_input = TextInput(
            text='3',
            input_filter='int',
            size_hint_y=None,
            height=50,
            multiline=False
        )
        delay_input.bind(text=self.on_delay_change)
        config_layout.add_widget(delay_input)
        self.delay_input = delay_input
        
        # 点击延迟
        config_layout.add_widget(Label(text='点击延迟(秒):', size_hint_y=None, height=50))
        click_delay_input = TextInput(
            text='1',
            input_filter='int',
            size_hint_y=None,
            height=50,
            multiline=False
        )
        click_delay_input.bind(text=self.on_click_delay_change)
        config_layout.add_widget(click_delay_input)
        self.click_delay_input = click_delay_input
        
        # 调试模式
        config_layout.add_widget(Label(text='调试模式:', size_hint_y=None, height=50))
        debug_toggle = ToggleButton(
            text='开启',
            state='down',
            size_hint_y=None,
            height=50,
            background_color=(0.2, 0.8, 0.2, 1)
        )
        debug_toggle.bind(state=self.on_debug_toggle)
        config_layout.add_widget(debug_toggle)
        self.debug_toggle = debug_toggle
        
        config_scroll.add_widget(config_layout)
        main_layout.add_widget(config_scroll)
        
        # ==================== 进度条 ====================
        progress_layout = BoxLayout(size_hint_y=0.08, spacing=10)
        self.progress_bar = ProgressBar(max=100, value=0)
        progress_layout.add_widget(self.progress_bar)
        main_layout.add_widget(progress_layout)
        
        # ==================== 状态显示 ====================
        status_layout = BoxLayout(size_hint_y=0.08, spacing=10)
        self.status_label = Label(text='准备就绪', font_size='16sp', color=(0, 1, 0, 1))
        status_layout.add_widget(self.status_label)
        main_layout.add_widget(status_layout)
        
        # ==================== 日志显示 ====================
        log_label = Label(text='运行日志:', size_hint_y=0.05, font_size='14sp')
        main_layout.add_widget(log_label)
        
        self.log_scroll = ScrollView()
        self.log_display = TextInput(
            text='',
            readonly=True,
            size_hint_y=None,
            multiline=True,
            font_size='10sp'
        )
        self.log_display.bind(minimum_height=self.log_display.setter('height'))
        self.log_scroll.add_widget(self.log_display)
        main_layout.add_widget(self.log_scroll)
        
        # ==================== 底部 - 按钮 ====================
        button_layout = BoxLayout(size_hint_y=0.1, spacing=10)
        
        start_btn = Button(
            text='▶ 开始运行',
            background_color=(0.2, 0.8, 0.2, 1),
            size_hint=0.5
        )
        start_btn.bind(on_press=self.on_start_pressed)
        button_layout.add_widget(start_btn)
        self.start_btn = start_btn
        
        stop_btn = Button(
            text='⏹ 停止',
            background_color=(0.8, 0.2, 0.2, 1),
            size_hint=0.5,
            disabled=True
        )
        stop_btn.bind(on_press=self.on_stop_pressed)
        button_layout.add_widget(stop_btn)
        self.stop_btn = stop_btn
        
        clear_btn = Button(
            text='🗑 清空日志',
            background_color=(0.8, 0.8, 0.2, 1),
            size_hint=0.5
        )
        clear_btn.bind(on_press=self.on_clear_pressed)
        button_layout.add_widget(clear_btn)
        
        main_layout.add_widget(button_layout)
        
        # 初始日志
        self.log("✅ APP 启动成功", "INFO")
        self.log("📋 配置已加载", "INFO")
        self.log("👉 点击「开始运行」开始自动化", "INFO")
        
        return main_layout
    
    # ==================== 事件处理 ====================
    
    def on_loop_count_change(self, spinner, text):
        """循环次数改变"""
        self.config['loop_count'] = int(text)
        self.log(f"📝 循环次数改为: {text}", "INFO")
    
    def on_delay_change(self, instance, value):
        """延迟改变"""
        try:
            self.config['loop_delay'] = int(value)
        except:
            pass
    
    def on_click_delay_change(self, instance, value):
        """点击延迟改变"""
        try:
            self.config['click_delay'] = int(value)
        except:
            pass
    
    def on_debug_toggle(self, instance, value):
        """调试模式切换"""
        self.config['debug_mode'] = value == 'down'
        state = "开启" if value == 'down' else "关闭"
        self.log(f"🐛 调试模式: {state}", "INFO")
    
    def on_start_pressed(self, instance):
        """开始按钮"""
        if not self.is_running:
            self.is_running = True
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
            self.status_label.text = "⏳ 正在运行..."
            self.status_label.color = (1, 1, 0, 1)
            
            # 在后台线程运行
            self.thread = threading.Thread(target=self.run_automation)
            self.thread.start()
    
    def on_stop_pressed(self, instance):
        """停止按钮"""
        self.is_running = False
        self.start_btn.disabled = False
        self.stop_btn.disabled = True
        self.status_label.text = "已停止"
        self.status_label.color = (1, 0, 0, 1)
        self.log("⏹ 用户停止了运行", "WARNING")
    
    def on_clear_pressed(self, instance):
        """清空日志"""
        self.log_display.text = ""
        self.logs.clear()
    
    # ==================== 自动化逻辑 ====================
    
    def run_automation(self):
        """运行自动化"""
        try:
            self.log("🎮 开始自动化运行", "INFO")
            self.log(f"配置: {self.config}", "INFO")
            
            loop_count = self.config['loop_count']
            success_count = 0
            
            for i in range(1, loop_count + 1):
                if not self.is_running:
                    break
                
                self.log(f"\n【第 {i}/{loop_count} 轮】", "INFO")
                
                # 模拟一轮运行
                if self.run_one_round(i):
                    success_count += 1
                    self.log(f"✅ 第 {i} 轮完成", "SUCCESS")
                else:
                    self.log(f"❌ 第 {i} 轮失败", "ERROR")
                
                # 更新进度条
                progress = int((i / loop_count) * 100)
                self.progress_bar.value = progress
                
                # 轮次延迟
                if i < loop_count and self.is_running:
                    delay = self.config['loop_delay']
                    self.log(f"⏳ 等待 {delay} 秒...", "INFO")
                    time.sleep(delay)
            
            # 完成
            self.log(f"\n✅ 运行完成！成功 {success_count}/{loop_count} 轮", "SUCCESS")
            self.log("📊 统计: 成功 {} 轮，失败 {} 轮".format(success_count, loop_count - success_count), "INFO")
            
            self.progress_bar.value = 100
            self.status_label.text = "✅ 完成"
            self.status_label.color = (0, 1, 0, 1)
            
        except Exception as e:
            self.log(f"❌ 运行失败: {str(e)}", "ERROR")
            self.status_label.text = "❌ 出错"
            self.status_label.color = (1, 0, 0, 1)
        
        finally:
            self.is_running = False
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
    
    def run_one_round(self, round_num):
        """运行一轮"""
        try:
            # 这里是模拟逻辑，实际应该调用 ADB 等
            time.sleep(2)  # 模拟截屏
            time.sleep(1)  # 模拟点击
            time.sleep(3)  # 模拟战斗
            time.sleep(1)  # 模拟领奖
            return True
        except Exception as e:
            self.log(f"轮次执行失败: {str(e)}", "ERROR")
            return False


if __name__ == '__main__':
    app = DanshellAutoBotApp()
    app.run()
