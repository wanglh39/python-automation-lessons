"""键盘控制 —— pyautogui 键盘 API + pyperclip 剪贴板

演示 pyautogui 键盘相关 API：typewrite 打字、press 按键、hotkey 组合键、
keyDown/keyUp 按住松开。打字和按键只用 print 说明用法不真执行（避免把字符
打进你正在编辑的文件）。pyperclip 剪贴板可以真实演示，安全。最后演示
"用剪贴板复制粘贴一段文字"的完整流程（剪贴板真实操作，粘贴用 print 说明）。

运行: uv run python lessons/10_GUI桌面自动化/02_键盘控制.py
"""
import pyautogui
import pyperclip


# 安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


print("=" * 55)
print("1. typewrite：模拟打字（用 print 说明，不真打）")
print("=" * 55)
print("  API 用法（本脚本不真实打字，避免干扰你正在编辑的内容）：")
print("    pyautogui.typewrite('Hello world')              # 逐字符打出")
print("    pyautogui.typewrite('Hello', interval=0.1)      # 每个字符间隔 0.1 秒")
print("    pyautogui.typewrite(['H','i','enter'])          # 传列表可含按键名")
print("  -> typewrite 是'逐个字符敲'，能看见打字过程；interval 控制速度")
print("  -> 注意：typewrite 默认只支持 ASCII，中文要靠剪贴板粘贴（见第 5 节）")
print("  -> 真实场景：先 click 点到输入框，再 typewrite 打字")

print("\n" + "=" * 55)
print("2. press：按单个键（用 print 说明，不真按）")
print("=" * 55)
print("  API 用法（本脚本不真实按键）：")
print("    pyautogui.press('enter')        # 回车")
print("    pyautogui.press('esc')          # Esc")
print("    pyautogui.press('tab')          # Tab")
print("    pyautogui.press('backspace')    # 退格")
print("    pyautogui.press('delete')       # Delete")
print("    pyautogui.press('space')        # 空格")
print("    pyautogui.press('f5')           # F5")
print("    pyautogui.press('left')         # 方向键左")
print("  -> press 适合按'单个有名字的键'，如回车、Esc、方向键、功能键")
print("  -> 完整按键名列表见 pyautogui.KEYBOARD_KEYS")

print("\n" + "=" * 55)
print("3. hotkey：组合键（用 print 说明，不真按）")
print("=" * 55)
print("  API 用法（本脚本不真实按键）：")
print("    pyautogui.hotkey('ctrl', 'c')      # Ctrl+C 复制")
print("    pyautogui.hotkey('ctrl', 'v')      # Ctrl+V 粘贴")
print("    pyautogui.hotkey('ctrl', 's')      # Ctrl+S 保存")
print("    pyautogui.hotkey('ctrl', 'a')      # Ctrl+A 全选")
print("    pyautogui.hotkey('alt', 'f4')      # Alt+F4 关窗口")
print("    pyautogui.hotkey('ctrl', 'shift', 'esc')  # 打开任务管理器")
print("  -> hotkey 自动处理'按下顺序'：依次按下，再逆序松开")
print("  -> 等价于 keyDown('ctrl') + keyDown('c') + keyUp('c') + keyUp('ctrl')")

print("\n" + "=" * 55)
print("4. keyDown / keyUp：按住与松开（用 print 说明）")
print("=" * 55)
print("  API 用法（本脚本不真实按键）：")
print("    pyautogui.keyDown('shift')       # 按住 shift")
print("    pyautogui.press('left')          # 按方向键（shift 按住时是选区）")
print("    pyautogui.press('left')")
print("    pyautogui.keyUp('shift')         # 松开 shift")
print("  -> 适合'按住某键同时做别的事'，比如按住 shift 多选、按住 ctrl 多选")

print("\n" + "=" * 55)
print("5. pyperclip：剪贴板读写（真实演示，安全）")
print("=" * 55)
print("  pyperclip.copy(text) 写入剪贴板，pyperclip.paste() 读取剪贴板")
print("  -> 这是真实操作，但只动剪贴板不动键鼠，安全")
# 先备份当前剪贴板内容，演示完恢复
try:
    original = pyperclip.paste()
except Exception as e:
    original = ""
    print(f"  [读取原剪贴板失败，置空] {e}")

demo_text = "Python 自动化：从剪贴板复制粘贴"
print(f"  即将写入剪贴板: {demo_text!r}")
pyperclip.copy(demo_text)
read_back = pyperclip.paste()
print(f"  读回剪贴板内容: {read_back!r}")
print(f"  写入和读回一致: {read_back == demo_text}")
print("  -> pyperclip 跨平台：Windows/macOS/Linux 都能用同一套 API")

# 恢复原来的剪贴板内容，不破坏用户剪贴板
pyperclip.copy(original)
print(f"  已恢复你原来的剪贴板内容（长度 {len(original)} 字符）")

print("\n" + "=" * 55)
print("6. 实战套路：剪贴板 + 粘贴输入中文")
print("=" * 55)
print("  pyautogui.typewrite 不支持中文，输入中文的标准套路是：")
print("    import pyperclip, pyautogui")
print("    pyperclip.copy('你好世界')            # 中文先放剪贴板")
print("    pyautogui.hotkey('ctrl', 'v')         # 再粘贴进去")
print("  -> 本脚本不真实执行粘贴（不碰你的输入框），只演示剪贴板这一半：")
chinese_text = "你好，GUI 自动化"
pyperclip.copy(chinese_text)
print(f"  已把 {chinese_text!r} 放进剪贴板")
print(f"  现在你在任何输入框按 Ctrl+V 都能粘出这段文字（可手动试一下）")
print("  -> 真实脚本里接下来会 pyautogui.click(输入框坐标) 然后 hotkey('ctrl','v')")
# 恢复剪贴板
pyperclip.copy(original)
print(f"  （演示完，已恢复你原来的剪贴板内容）")

print("\n" + "=" * 55)
print("7. 完整按键名速查（pyautogui.KEYBOARD_KEYS 节选）")
print("=" * 55)
keys = pyautogui.KEYBOARD_KEYS
print(f"  pyautogui.KEYBOARD_KEYS 共 {len(keys)} 个按键名")
print(f"  前 20 个: {keys[:20]}")
print("  -> 常用：enter esc tab space backspace delete")
print("  -> 方向：left right up down")
print("  -> 修饰：ctrl shift alt winleft winright")
print("  -> 功能：f1 f2 ... f12")
print("  -> 字母数字直接传 'a' 'b' '1' '2' 即可")

print("\n" + "=" * 55)
print("完成!")
print("=" * 55)
print("要点:")
print("  1. typewrite 逐字符打字（只支持 ASCII），press 按单个键，hotkey 组合键")
print("  2. keyDown/keyUp 分开控制按住松开，能做'按住 shift 多选'这类操作")
print("  3. 中文输入靠剪贴板：pyperclip.copy(中文) + hotkey('ctrl','v')")
print("  4. pyperclip.copy/paste 操作剪贴板，跨平台，安全，可真实演示")
print("  5. 真实打字前先 click 到输入框；教学脚本不真打字，避免干扰用户")