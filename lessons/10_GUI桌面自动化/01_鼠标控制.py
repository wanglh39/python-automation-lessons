"""鼠标控制 —— pyautogui 鼠标 API 入门

演示 pyautogui 鼠标相关 API：获取屏幕尺寸和鼠标位置、moveTo/moveRel 移动、
click/doubleClick/rightClick 点击、dragTo 拖拽、mouseDown/mouseUp 按下松开。
所有真实移动只做最小幅度（几像素），点击和拖拽用 print 说明用法不真执行，
避免干扰你正在做的事。开头先设 FAILSAFE 和 PAUSE 保证安全。

运行: uv run python lessons/10_GUI桌面自动化/01_鼠标控制.py
"""
import pyautogui


# 安全设置：务必放在最前面
# FAILSAFE=True 时，鼠标移到屏幕左上角 (0,0) 会立刻抛 FailSafeException 中断脚本
# 这是救命稻草：脚本失控时把鼠标甩到左上角就能停
pyautogui.FAILSAFE = True
# PAUSE 是每个 pyautogui 调用后的暂停秒数，让你来得及看清/反应
# 默认就是 0.1，这里显式设一下；调试时可设 0.5
pyautogui.PAUSE = 0.1


print("=" * 55)
print("1. 获取屏幕尺寸：pyautogui.size()")
print("=" * 55)
width, height = pyautogui.size()
print(f"  屏幕分辨率: {width} x {height}")
print(f"  pyautogui.size() 返回 (宽, 高) 元组: ({width}, {height})")
print("  -> 这是主屏的逻辑分辨率；多屏时只返回主屏")
print("  -> 想知道某坐标在不在屏内：pyautogui.onScreen(x, y)")

print("\n" + "=" * 55)
print("2. 获取鼠标当前位置：pyautogui.position()")
print("=" * 55)
x, y = pyautogui.position()
print(f"  当前鼠标位置: ({x}, {y})")
print("  -> position() 返回 (x, y)，x 是距左边的像素，y 是距上边的像素")
print("  -> 左上角是 (0, 0)，右下角是 (width-1, height-1)")

print("\n" + "=" * 55)
print("3. moveTo：移动鼠标到指定坐标（最小幅度演示）")
print("=" * 55)
cur_x, cur_y = pyautogui.position()
# 只在当前位置附近移动几像素，看得见但不影响操作
target_x = min(cur_x + 30, width - 1)
target_y = min(cur_y + 30, height - 1)
print(f"  即将把鼠标从 ({cur_x}, {cur_y}) 移到 ({target_x}, {target_y})")
print("  -> 只移动 30 像素，安全演示；duration=0.3 表示 0.3 秒内匀速移过去")
pyautogui.moveTo(target_x, target_y, duration=0.3)
new_x, new_y = pyautogui.position()
print(f"  移动后位置: ({new_x}, {new_y})")
print("  -> moveTo(x, y, duration) 是绝对移动，移到屏幕坐标 (x, y)")
print("  -> duration=0 是瞬间移过去（默认），设大一点能看见移动过程")

print("\n" + "=" * 55)
print("4. moveRel：相对移动（从当前位置偏移）")
print("=" * 55)
cur_x, cur_y = pyautogui.position()
print(f"  当前位置: ({cur_x}, {cur_y})")
print("  即将相对移动：左移 20 像素、上移 20 像素（duration=0.3）")
# moveRel(dx, dy) 从当前位置偏移；新版本已别名 move，moveRel 仍可用
pyautogui.moveRel(-20, -20, duration=0.3)
new_x, new_y = pyautogui.position()
print(f"  移动后位置: ({new_x}, {new_y})")
print("  -> moveRel(dx, dy) 相对移动，正 x 向右、正 y 向下")
print("  -> 适合'往右挪一点再点'这种场景，不用算绝对坐标")

print("\n" + "=" * 55)
print("5. click / doubleClick / rightClick：点击（用 print 说明，不真点）")
print("=" * 55)
print("  API 用法（本脚本不真实点击，避免点错东西）：")
print("    pyautogui.click(x, y)              # 在 (x,y) 单击左键")
print("    pyautogui.click()                  # 不传坐标，点当前位置")
print("    pyautogui.doubleClick(x, y)        # 双击")
print("    pyautogui.rightClick(x, y)         # 右击")
print("    pyautogui.middleClick(x, y)        # 中键点击")
print("    pyautogui.click(button='right')    # 只指定按键不移动")
print("    pyautogui.click(clicks=3)          # 连点 3 次")
print("  -> 真实脚本里通常先 moveTo 再 click，或直接 click(x, y) 一步到位")
print("  -> 坐标怎么来？用截图+找图，或先用 position() 鼠标定位工具量出来")

print("\n" + "=" * 55)
print("6. dragTo / dragRel：拖拽（用 print 说明，不真拖）")
print("=" * 55)
print("  API 用法（本脚本不真实拖拽）：")
print("    pyautogui.dragTo(x, y, duration=0.5)        # 按住左键拖到 (x,y)")
print("    pyautogui.dragRel(100, 0, duration=0.5)     # 相对拖：向右拖 100 像素")
print("    pyautogui.dragTo(x, y, button='right')      # 按住右键拖")
print("  -> 典型场景：拖文件到文件夹、拖选文本、滑块调值")
print("  -> duration 要设够大，太快系统来不及识别成拖拽")

print("\n" + "=" * 55)
print("7. mouseDown / mouseUp：按下与松开（精细控制）")
print("=" * 55)
print("  API 用法（本脚本不真实执行）：")
print("    pyautogui.mouseDown(x, y, button='left')    # 在 (x,y) 按下左键")
print("    pyautogui.mouseUp(x, y, button='left')      # 松开左键")
print("  -> click() 等价于 mouseDown + mouseUp，分开写能做更细的控制")
print("  -> 例如：mouseDown -> moveTo -> mouseUp，实现'按下后拖到别处再松开'")

print("\n" + "=" * 55)
print("8. 安全机制提醒")
print("=" * 55)
print(f"  pyautogui.FAILSAFE = {pyautogui.FAILSAFE}")
print(f"  pyautogui.PAUSE    = {pyautogui.PAUSE}")
print("  -> FAILSAFE=True：鼠标移到左上角 (0,0) 立刻抛异常退出，救命用")
print("  -> PAUSE=0.1：每个 pyautogui 调用后暂停 0.1 秒，让你反应")
print("  -> 脚本失控时：把鼠标快速甩到屏幕左上角即可中断")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. size() 取屏幕分辨率，position() 取鼠标当前位置，都是只读不动的")
print("  2. moveTo 绝对移动、moveRel 相对移动，duration 控制移动速度")
print("  3. click/doubleClick/rightClick 点击，dragTo/dragRel 拖拽")
print("  4. mouseDown/mouseUp 分开控制按下松开，能做更精细操作")
print("  5. 永远先设 FAILSAFE=True 和 PAUSE，真实操作前 print 提示用户")