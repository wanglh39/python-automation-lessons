# 模块 10：GUI 桌面自动化

> 前面那些自动化都是在"后台"干活——发请求、解析 HTML、读写文件，看不见摸不着。但很多软件只有图形界面（GUI）：老版的 ERP、桌面绘图工具、安装向导、游戏辅助，没有命令行接口、没有 API，只能像人一样去点鼠标、敲键盘。pyautogui 就是干这个的：让 Python 真的控制鼠标移动、点击、拖拽，模拟键盘打字、按快捷键，还能截屏、在屏幕上找图。配合 pyperclip 操作剪贴板，可以做出"自动填表单、自动点按钮、自动登录"这类脚本。本模块演示鼠标、键盘、截图找图、安全机制四块，**所有真实操作都做最小幅度并提前提示，绝不乱动你的鼠标键盘**。

## 核心库一览

| 库 | 来源 | 用途 | 推荐度 |
|---|:---:|---|:---:|
| `pyautogui` | 第三方 | 控制鼠标移动/点击/拖拽、键盘打字/按键、截屏、屏幕找图 | ★★★★★ |
| `pyperclip` | 第三方 | 跨平台剪贴板：copy() 写入、paste() 读取 | ★★★★ |
| `Pillow` | 第三方 | pyautogui 截图底层依赖，截图返回 Image 对象 | ★★★★ |
| `opencv` | 第三方（可选） | 让 locateOnScreen 支持 confidence 模糊匹配 | ★★★ |

> pyautogui 装好后 Pillow 会自动跟着装（截图依赖）。opencv 是可选的：不装也能截图、找图，只是 `locateOnScreen` 不能传 `confidence` 参数（模糊匹配），只能精确像素匹配。需要模糊匹配时 `uv add opencv-python`。

## pyautogui 能做什么 / 注意事项

**能做什么**：
- **鼠标**：获取位置、移动到指定坐标、相对移动、单击/双击/右击、拖拽、按下/松开
- **键盘**：打字（typewrite）、按单个键（press）、组合键（hotkey）、按下/松开
- **截屏**：全屏截图、区域截图，保存成 PNG 或返回 Image 对象
- **找图**：在屏幕上找一张小图的位置（自动化点击按钮的常用套路）
- **弹框**：confirm / alert / prompt，跟用户交互确认
- **安全**：FAILSAFE（鼠标移到左上角触发异常退出）、PAUSE（每个操作后暂停）

**重要警告——pyautogui 会真的操作你的鼠标键盘！**

这跟 selenium 不一样：selenium 控制的是它自己开的浏览器，pyautogui 控制的是**你正在用的这套键鼠**。脚本跑起来时，你的鼠标真的会动、真的会点、键盘真的会打字。如果脚本有 bug 或者坐标写错，可能：
- 鼠标乱跳，点错东西（误删文件、发错消息）
- 键盘乱打，把一堆字符打进你正在编辑的文件
- 卡在死循环里停不下来

**所以写 pyautogui 脚本必须遵守三条铁律**：
1. **永远先设 `pyautogui.FAILSAFE = True`**：紧急时把鼠标甩到屏幕左上角 (0,0)，会立刻抛 FailSafeException 中断脚本。这是救命稻草。
2. **设 `pyautogui.PAUSE`**：每个 PyAutoGUI 操作后暂停一下（默认 0.1 秒），让你来得及反应。调试时设大一点（0.5~1 秒）。
3. **真实操作前 print 提示**：告诉用户"接下来要点 (x,y)"、"接下来要打字 xxx"，给人取消的机会（关终端窗口即可）。

> 本模块所有教学脚本都遵守这三条。涉及真实鼠标移动的只移动几像素（看得见但不影响操作），键盘打字只用 print 说明用法不真打，截图和弹框这类安全操作才真实执行。

## 核心 API 速查

```python
import pyautogui

# --- 安全设置（务必放在最前面）---
pyautogui.FAILSAFE = True   # 鼠标移到左上角(0,0)触发 FailSafeException，救命用
pyautogui.PAUSE = 0.1       # 每个 pyautogui 调用后暂停 0.1 秒（默认就是 0.1）

# --- 屏幕与鼠标位置 ---
width, height = pyautogui.size()        # 屏幕分辨率，返回 (宽, 高)
x, y = pyautogui.position()             # 鼠标当前位置
pyautogui.onScreen(x, y)                # 坐标是否在屏幕范围内

# --- 鼠标移动 ---
pyautogui.moveTo(x, y, duration=0.3)    # 移到 (x,y)，duration 秒内匀速移
pyautogui.moveRel(50, 0, duration=0.2)  # 相对移动：右移 50 像素（moveRel 已别名 move）

# --- 鼠标点击 ---
pyautogui.click(x, y)                   # 在 (x,y) 单击左键（不传坐标则点当前位置）
pyautogui.doubleClick(x, y)             # 双击
pyautogui.rightClick(x, y)              # 右击
pyautogui.middleClick(x, y)             # 中键点击
pyautogui.click(button='right')         # 只指定按键，不移动

# --- 拖拽 ---
pyautogui.dragTo(x, y, duration=0.5)             # 拖到 (x,y)
pyautogui.dragRel(100, 0, duration=0.5)          # 相对拖动：向右拖 100 像素

# --- 鼠标按下/松开（精细控制）---
pyautogui.mouseDown(x, y, button='left')   # 按下左键
pyautogui.mouseUp(x, y, button='left')     # 松开左键

# --- 键盘 ---
pyautogui.typewrite('Hello', interval=0.1) # 打字（每个字符间隔 0.1 秒）
pyautogui.press('enter')                   # 按单个键
pyautogui.hotkey('ctrl', 'c')              # 组合键：Ctrl+C
pyautogui.keyDown('shift')                 # 按住 shift
pyautogui.keyUp('shift')                   # 松开 shift

# --- 截屏 ---
img = pyautogui.screenshot()               # 全屏截图，返回 PIL.Image
img.save('screen.png')                     # 保存到文件
img = pyautogui.screenshot(region=(0,0,300,300))  # 区域截图 (左,上,宽,高)

# --- 找图 ---
pos = pyautogui.locateOnScreen('button.png')           # 找图，返回 Box(left,top,width,height)
center = pyautogui.locateCenterOnScreen('button.png') # 返回中心点 (x,y)
for pos in pyautogui.locateAllOnScreen('button.png'): # 找所有匹配位置
    print(pos)
# confidence 模糊匹配（需要 opencv-python）
pos = pyautogui.locateOnScreen('button.png', confidence=0.9)

# --- 弹框（跟用户交互）---
pyautogui.alert('出错了', '错误')                 # 警告框，只有确定
ok = pyautogui.confirm('要继续吗？')              # 确认框，返回 'OK' 或 'Cancel'
text = pyautogui.prompt('请输入文件名')           # 输入框，返回字符串或 None
pwd = pyautogui.password('请输入密码')            # 密码框，输入显示为 *
```

```python
# --- 剪贴板（pyperclip，跨平台）---
import pyperclip
pyperclip.copy('要复制的内容')     # 写入剪贴板
text = pyperclip.paste()           # 读取剪贴板
# pyautogui 没有直接读写剪贴板的函数，靠 pyperclip 补这个缺口
# 常见套路：pyperclip.copy(text) + pyautogui.hotkey('ctrl','v') 粘贴
```

## 本模块示例

| 脚本 | 演示 |
|---|---|
| [01_鼠标控制.py](01_鼠标控制.py) | 屏幕尺寸、鼠标位置、moveTo/moveRel 移动（最小幅度）、click/drag 用法说明、FAILSAFE |
| [02_键盘控制.py](02_键盘控制.py) | typewrite/press/hotkey 用法说明、pyperclip 剪贴板真实演示、复制粘贴流程 |
| [03_截图与找图.py](03_截图与找图.py) | 全屏截图、区域截图、locateOnScreen 找图完整流程、confidence 说明 |
| [04_安全机制.py](04_安全机制.py) | FAILSAFE/PAUSE 作用、confirm/alert/prompt 弹框真实演示、最佳实践 |

运行方式：
```bash
uv run python lessons/10_GUI桌面自动化/01_鼠标控制.py
uv run python lessons/10_GUI桌面自动化/02_键盘控制.py
uv run python lessons/10_GUI桌面自动化/03_截图与找图.py
uv run python lessons/10_GUI桌面自动化/04_安全机制.py
```

> 脚本安全：鼠标只移动几像素、键盘不真打字、截图和弹框才真实执行。跑的时候别同时操作鼠标，看完脚本输出就行。要中途停掉，把鼠标甩到屏幕左上角即可触发 FAILSAFE 退出。

## 底层原理（简单了解）

1. **pyautogui 底层调系统 API**：在 Windows 上调 `ctypes` + Win32 API（`SetCursorPos`、`mouse_event`、`keybd_event`），在 macOS 上调 Quartz（`CGEventCreateMouseEvent`），在 Linux 上调 Xlib。所以同一套 Python 代码能跨平台控制键鼠——但具体行为有细微差异（比如 macOS 上某些按键需要"辅助功能"权限）。pyautogui 把这些差异封掉了，你只管写 `click(x, y)`。
2. **截图用 Pillow（PIL.ImageGrab）**：`pyautogui.screenshot()` 内部调 `PIL.ImageGrab.grab()`，Windows 上走 Win32 的 `BitBlt`、macOS 上走 `CGWindowListCreateImage`、Linux 上走 Xlib。返回的是 `PIL.Image.Image` 对象，可以直接 `.save()` 存文件、`.crop()` 裁剪、`.getpixel()` 取像素。所以"截图"本身不依赖 pyautogui，直接用 Pillow 也能做，pyautogui 只是包了一层方便配合找图。
3. **找图是像素逐点匹配**：`locateOnScreen('btn.png')` 的原理是——先截一张全屏图，把目标小图（btn.png）的像素跟全屏图逐位置比对，找像素完全一致的位置。这是**精确匹配**，差一个像素的颜色（抗锯齿、主题变化）就找不到。所以实际用要装 opencv 开 `confidence=0.9` 做**模糊匹配**：用模板匹配算法（cv2.matchTemplate）算相似度，≥ 0.9 就算匹配上。这也是为什么找图很慢——精确匹配要遍历每个位置，模糊匹配还要算相似度矩阵。
4. **FAILSAFE 的实现**：pyautogui 在每个会移动鼠标的调用开头检查 `position()`，如果鼠标在 (0,0) 就抛 `FailSafeException`。所以"鼠标甩到左上角"能中断——脚本下一次调 pyautogui 时就会检查到并退出。但注意：如果脚本正卡在 `time.sleep(10)` 里没调 pyautogui，FAILSAFE 不会触发，得等 sleep 完。所以 PAUSE 别设太大，否则反应慢。
5. **PAUSE 的实现**：每个 pyautogui 公开函数装饰了 `_pyautogui_win._pause`，调用完会 `time.sleep(PAUSE)`。默认 0.1 秒，让你来得及看清鼠标在干什么。设成 0 能跑快点但更危险，调试时建议设 0.5~1 秒。