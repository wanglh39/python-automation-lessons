"""安全机制 —— FAILSAFE / PAUSE / 弹框交互

演示 pyautogui 的安全机制和用户交互：FAILSAFE 紧急退出、PAUSE 操作暂停、
confirm/alert/prompt/password 弹框。FAILSAFE 只用 print 说明不真触发
（真触发脚本就停了）。弹框可以真实演示（安全，只是弹个对话框）。
最后总结写 pyautogui 脚本的最佳实践。

运行: uv run python lessons/10_GUI桌面自动化/04_安全机制.py
"""
import pyautogui


# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


print("=" * 55)
print("1. FAILSAFE：紧急退出机制")
print("=" * 55)
print(f"  pyautogui.FAILSAFE = {pyautogui.FAILSAFE}")
print("  -> FAILSAFE=True 时，鼠标移到屏幕左上角 (0,0) 会抛 FailSafeException")
print("  -> 这是救命稻草：脚本失控时把鼠标甩到左上角就能立刻中断")
print("  -> 实现原理：每个会移动鼠标的调用开头检查 position()，在 (0,0) 就抛异常")
print("  -> 注意：只在'调用 pyautogui 时'检查，卡在 time.sleep 里不触发")
print("  本脚本不真实触发 FAILSAFE（触发了就停了），只说明用法：")
print("    import pyautogui")
print("    pyautogui.FAILSAFE = True   # 务必放最前面")
print("    try:")
print("        pyautogui.moveTo(100, 100, duration=1)")
print("    except pyautogui.FailSafeException:")
print("        print('用户触发了紧急退出，脚本停止')")

print("\n" + "=" * 55)
print("2. PAUSE：每个操作后暂停")
print("=" * 55)
print(f"  pyautogui.PAUSE = {pyautogui.PAUSE}  (秒)")
print("  -> 每个 pyautogui 调用后会 time.sleep(PAUSE)，让你看清/反应")
print("  -> 默认 0.1 秒；调试时建议设 0.5~1，正式跑可设 0 或小一点")
print("  演示把 PAUSE 临时调大，看效果：")
old_pause = pyautogui.PAUSE
pyautogui.PAUSE = 0.3
print(f"  已把 PAUSE 设为 {pyautogui.PAUSE}，接下来 position() 后会暂停 0.3 秒")
import time
t0 = time.time()
pyautogui.position()  # 这个调用后会暂停 PAUSE 秒
elapsed = time.time() - t0
print(f"  position() 调用耗时约 {elapsed:.3f} 秒（含 PAUSE={pyautogui.PAUSE}）")
pyautogui.PAUSE = old_pause
print(f"  已恢复 PAUSE = {pyautogui.PAUSE}")
print("  -> PAUSE 太大脚本慢，太小来不及反应；0.1~0.3 是常用区间")

print("\n" + "=" * 55)
print("3. confirm：确认框（真实演示，安全）")
print("=" * 55)
print("  即将弹出一个确认框，点'OK'或'Cancel'继续")
print("  -> pyautogui.confirm(text, title) 返回 'OK' 或 'Cancel'")
result = pyautogui.confirm(
    text="这是教学脚本的确认框演示\n点 OK 或 Cancel 都可以，脚本都会继续",
    title="GUI 自动化教学",
)
print(f"  你点了: {result!r}")
print("  -> confirm 是跟用户确认'要不要继续'的好办法，写自动化脚本强烈推荐")
print("  -> 真实用法：if pyautogui.confirm('即将点击 (100,100)，继续？') != 'OK': sys.exit()")

print("\n" + "=" * 55)
print("4. alert：警告框（真实演示，安全）")
print("=" * 55)
print("  即将弹出一个警告框，点'OK'继续")
pyautogui.alert(text="这是 alert 警告框演示\n只有 OK 按钮，用于通知用户", title="提示")
print("  -> alert(text, title) 只有一个 OK 按钮，用于纯通知，不返回值")
print("  -> 适合'出错了告诉你一声'、'完成了告诉你一声'")

print("\n" + "=" * 55)
print("5. prompt：输入框（真实演示，安全）")
print("=" * 55)
print("  即将弹出一个输入框，可以输入文字或直接取消")
user_input = pyautogui.prompt(
    text="请随便输入点什么（或直接点 Cancel）",
    title="输入框演示",
    default="默认值",
)
print(f"  返回值: {user_input!r}")
print("  -> prompt(text, title, default) 返回输入的字符串，点 Cancel 返回 None")
print("  -> 适合让用户输入文件名、循环次数等参数")

print("\n" + "=" * 55)
print("6. password：密码框（真实演示，安全）")
print("=" * 55)
print("  即将弹出一个密码框，输入显示为 * 号")
pwd = pyautogui.password(
    text="演示密码框，输入会显示为 *\n（别真输密码，这只是演示）",
    title="密码框演示",
)
print(f"  返回值长度: {len(pwd) if pwd is not None else None}  (不打印内容)")
print("  -> password(text, title) 跟 prompt 一样返回字符串/None，但输入显示为 *")
print("  -> 适合需要密码的自动化脚本（不过更推荐用环境变量/keyring 存密码）")

print("\n" + "=" * 55)
print("7. 最佳实践：写 pyautogui 脚本的安全清单")
print("=" * 55)
print("  [1] 永远先设 FAILSAFE=True 和 PAUSE，放脚本最前面")
print("  [2] 真实操作前用 confirm 让用户确认，给取消的机会")
print("  [3] 每个 click/moveTo 前 print 提示即将做什么、坐标多少")
print("  [4] 坐标尽量用找图（locateCenterOnScreen）获取，别硬编码")
print("      硬编码坐标换机器/换分辨率就错位了")
print("  [5] 限制操作范围：onScreen(x,y) 检查坐标在屏内，别点到屏外")
print("  [6] 操作完 print 结果，让用户知道脚本干了什么")
print("  [7] 用 try/except 包住关键操作，出错时 alert 通知用户")
print("  [8] 别在循环里高频 click 不变的位置，找到后记住坐标复用")
print("  [9] 调试时 PAUSE 设大（0.5~1），正式跑再调小")
print("  [10] 脚本失控时：鼠标甩到屏幕左上角触发 FAILSAFE 退出")

print("\n" + "=" * 55)
print("8. 安全脚本模板")
print("=" * 55)
print("  import pyautogui, sys")
print("  pyautogui.FAILSAFE = True")
print("  pyautogui.PAUSE = 0.3")
print("  if pyautogui.confirm('即将开始自动化操作，继续？') != 'OK':")
print("      sys.exit('用户取消')")
print("  try:")
print("      btn = pyautogui.locateCenterOnScreen('btn.png', confidence=0.9)")
print("      if btn is None:")
print("          pyautogui.alert('没找到按钮，可能界面变了'); sys.exit(1)")
print("      print(f'即将点击 {btn}')")
print("      pyautogui.click(*btn)")
print("      pyautogui.alert('操作完成')")
print("  except pyautogui.FailSafeException:")
print("      print('用户触发紧急退出')")
print("  except Exception as e:")
print("      pyautogui.alert(f'出错: {e}', '错误')")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. FAILSAFE=True：鼠标甩到左上角紧急退出，务必设；PAUSE 控制操作节奏")
print("  2. confirm/alert/prompt/password 是跟用户交互的弹框，安全可真实演示")
print("  3. 写脚本铁律：先设安全、操作前确认、print 提示、坐标用找图、try/except")
print("  4. 硬编码坐标换机器就错位，优先 locateCenterOnScreen 动态找")
print("  5. 失控时鼠标甩左上角触发 FAILSAFE；调试时 PAUSE 设大一点")