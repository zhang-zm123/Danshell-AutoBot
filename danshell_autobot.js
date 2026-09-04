// ============================================================
// 弹壳特工队自动刷主线任务 - Auto.js 脚本
// 在手机上运行，无需 PC 连接
// ============================================================

// 等待 Auto.js 服务启动
auto.waitFor();

// ============================================================
// 配置参数
// ============================================================

const CONFIG = {
  // 游戏包名
  GAME_PACKAGE: "com.danshell.game",
  
  // 运行次数
  LOOP_COUNT: 10,
  
  // 延迟时间（毫秒）
  LOOP_DELAY: 3000,        // 轮次间隔
  CLICK_DELAY: 1000,       // 点击延迟
  WAIT_TIMEOUT: 60000,     // 战斗超时
  
  // 调试模式
  DEBUG: true,
  
  // 截屏保存路径
  SCREENSHOT_DIR: "/sdcard/DCIM/DanshellAutoBot"
};

// ============================================================
// 日志和调试工具
// ============================================================

function log(msg, level = "INFO") {
  const time = new Date().toLocaleTimeString();
  const prefix = {
    "INFO": "ℹ️",
    "SUCCESS": "✅",
    "WARNING": "⚠️",
    "ERROR": "❌"
  }[level] || "📌";
  
  const logMsg = `[${time}] ${prefix} ${msg}`;
  console.log(logMsg);
  
  // 显示 Toast（手机右下角提示）
  if (level === "ERROR") {
    toast(msg);
  }
}

function saveScreenshot(name) {
  if (!CONFIG.DEBUG) return;
  
  try {
    // 创建目录
    if (!files.exists(CONFIG.SCREENSHOT_DIR)) {
      files.createPath(CONFIG.SCREENSHOT_DIR);
    }
    
    const path = CONFIG.SCREENSHOT_DIR + "/" + name + ".png";
    captureScreen(path);
    log(`截图已保存: ${name}`, "INFO");
  } catch (e) {
    log(`保存截图失败: ${e}`, "WARNING");
  }
}

// ============================================================
// 游戏控制函数
// ============================================================

/**
 * 启动游戏
 */
function startGame() {
  log("📱 启动游戏...", "INFO");
  
  // 点击应用图标启动游戏
  let launchResult = app.launch(CONFIG.GAME_PACKAGE);
  
  if (!launchResult) {
    log("游��启动失败，尝试手动打开", "WARNING");
    app.startActivity({
      action: "android.intent.action.MAIN",
      package: CONFIG.GAME_PACKAGE
    });
  }
  
  sleep(5000);  // 等待游戏加载
  log("✅ 游戏已启动", "SUCCESS");
}

/**
 * 查找文本并点击
 */
function findAndClickText(textName, timeout = 5000) {
  log(`👀 寻找文本: ${textName}`, "INFO");
  
  let startTime = Date.now();
  while (Date.now() - startTime < timeout) {
    let target = text(textName).findOnce();
    
    if (target && target.clickable()) {
      target.click();
      log(`👆 点击文本: ${textName}`, "SUCCESS");
      sleep(CONFIG.CLICK_DELAY);
      return true;
    }
    
    sleep(500);
  }
  
  log(`未找到文本: ${textName}`, "WARNING");
  return false;
}

/**
 * 等待文本出现
 */
function waitForText(textName, timeout = 10000) {
  log(`⏳ 等待文本: ${textName}`, "INFO");
  
  let startTime = Date.now();
  while (Date.now() - startTime < timeout) {
    if (text(textName).exists()) {
      log(`✅ 找到文本: ${textName}`, "SUCCESS");
      return true;
    }
    sleep(500);
  }
  
  log(`等待超时: ${textName}`, "WARNING");
  return false;
}

/**
 * 点击按钮（用 description 或 text）
 */
function clickButton(buttonName) {
  log(`👆 点击按钮: ${buttonName}`, "INFO");
  
  // 方法1：通过文本点击
  if (text(buttonName).exists()) {
    text(buttonName).findOnce().click();
    sleep(CONFIG.CLICK_DELAY);
    return true;
  }
  
  // 方法2：通过 description 点击
  if (desc(buttonName).exists()) {
    desc(buttonName).findOnce().click();
    sleep(CONFIG.CLICK_DELAY);
    return true;
  }
  
  log(`找不到按钮: ${buttonName}`, "WARNING");
  return false;
}

/**
 * 检测游戏是否在前台
 */
function isGameInForeground() {
  let currentPackage = currentPackage();
  return currentPackage === CONFIG.GAME_PACKAGE;
}

/**
 * 等待游戏回到前台
 */
function waitForGameForeground(timeout = 5000) {
  let startTime = Date.now();
  while (Date.now() - startTime < timeout) {
    if (isGameInForeground()) {
      return true;
    }
    sleep(500);
  }
  return false;
}

// ============================================================
// 主要自动化逻辑
// ============================================================

/**
 * 运行一轮自动化
 */
function runOneRound(roundNum) {
  log(`\n【第 ${roundNum} 轮】`, "INFO");
  
  try {
    // 1. 检查游戏是否在前台
    if (!isGameInForeground()) {
      log("游戏不在前台，尝试恢复", "WARNING");
      app.launchPackage(CONFIG.GAME_PACKAGE);
      sleep(2000);
    }
    
    saveScreenshot(`round_${roundNum}_start`);
    
    // 2. 进入主线任务
    log("📌 进入主线任务...", "INFO");
    if (!findAndClickText("主线", 3000)) {
      log("无法进入主线任务", "WARNING");
      return false;
    }
    sleep(2000);
    
    // 3. 选择任务
    log("📌 选择任务...", "INFO");
    
    // 这里需要根据实际游戏界面自定义
    // 例如：点击第一个可用的任务
    if (!findAndClickText("开始", 3000)) {
      log("无法选择任务，尝试找其他按钮", "WARNING");
      
      // 备选方案：点击任意地方尝试进入
      click(device.width / 2, device.height / 2);
      sleep(2000);
    }
    
    // 4. 开始战斗
    log("📌 开始战斗...", "INFO");
    if (!findAndClickText("开始", 3000)) {
      findAndClickText("自动", 2000);  // 如果有自动按钮也可以点
    }
    sleep(3000);
    
    // 5. 等待战斗完成
    log("⏳ 等待战斗完成...", "INFO");
    
    // 等待看到结算界面或奖励提示
    let battleComplete = false;
    let waitStart = Date.now();
    
    while (Date.now() - waitStart < CONFIG.WAIT_TIMEOUT) {
      if (text("领取").exists() || text("完成").exists() || text("胜利").exists()) {
        battleComplete = true;
        break;
      }
      sleep(1000);
    }
    
    if (!battleComplete) {
      log("战斗超时，继续尝试", "WARNING");
    }
    
    sleep(2000);
    saveScreenshot(`round_${roundNum}_result`);
    
    // 6. 领取奖励
    log("📌 领取奖励...", "INFO");
    if (!findAndClickText("领取", 2000)) {
      log("无法领取奖励", "WARNING");
    }
    sleep(2000);
    
    // 7. 返回主界面
    log("📌 返回主界面...", "INFO");
    
    // 尝试点击返回
    if (!findAndClickText("返回", 2000)) {
      // 备选方案：点击左上角返回按钮
      click(50, 50);
      sleep(2000);
    }
    
    log(`✅ 第 ${roundNum} 轮完成`, "SUCCESS");
    return true;
    
  } catch (e) {
    log(`❌ 第 ${roundNum} 轮执行失败: ${e}`, "ERROR");
    return false;
  }
}

// ============================================================
// 主程序入口
// ============================================================

function main() {
  log("=".repeat(50), "INFO");
  log("🎮 弹壳特工队自动刷主线任务启动", "INFO");
  log("=".repeat(50), "INFO");
  
  log(`📋 配置:`, "INFO");
  log(`   - 循环次数: ${CONFIG.LOOP_COUNT}`, "INFO");
  log(`   - 轮次延迟: ${CONFIG.LOOP_DELAY}ms`, "INFO");
  log(`   - 点击延迟: ${CONFIG.CLICK_DELAY}ms`, "INFO");
  log(`   - 调试模式: ${CONFIG.DEBUG ? "开启" : "关闭"}`, "INFO");
  
  // 启动游戏
  startGame();
  
  // 统计
  let successCount = 0;
  let failCount = 0;
  
  // 运行循环
  log(`\n🎯 开始自动化运行...`, "INFO");
  
  for (let i = 1; i <= CONFIG.LOOP_COUNT; i++) {
    try {
      if (runOneRound(i)) {
        successCount++;
      } else {
        failCount++;
      }
      
      // 轮次间隔
      if (i < CONFIG.LOOP_COUNT) {
        log(`⏳ 等待 ${CONFIG.LOOP_DELAY / 1000} 秒后开始下一轮...`, "INFO");
        sleep(CONFIG.LOOP_DELAY);
      }
      
    } catch (e) {
      log(`第 ${i} 轮异常: ${e}`, "ERROR");
      failCount++;
    }
  }
  
  // 显示统计
  log("\n" + "=".repeat(50), "INFO");
  log("📊 执行统计:", "INFO");
  log(`   - 总轮数: ${CONFIG.LOOP_COUNT}`, "INFO");
  log(`   - 成功: ${successCount}`, "SUCCESS");
  log(`   - 失败: ${failCount}`, "INFO");
  log("=".repeat(50), "INFO");
  
  log("\n✅ 自动化运行完成！", "SUCCESS");
  toast("运行完成！成功 " + successCount + " 轮，失败 " + failCount + " 轮");
  
  // 显示截图保存位置
  if (CONFIG.DEBUG) {
    log(`📸 截图保存在: ${CONFIG.SCREENSHOT_DIR}`, "INFO");
  }
}

// ============================================================
// 错误处理和主启动
// ============================================================

try {
  // 检查权限
  if (!auto.waitFor()) {
    log("❌ 需要启用无障碍服务", "ERROR");
    toastLog("请在设置中启用本应用的无障碍服务");
    exit();
  }
  
  // 运行主程序
  main();
  
} catch (e) {
  log(`程序崩溃: ${e}`, "ERROR");
  console.error(e);
  toastLog("程序出错: " + e);
}

// ============================================================
// 脚本结束
// ============================================================
