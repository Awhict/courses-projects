# monitor_browser.py
import ctypes
import time
import os

# 加载钩子DLL
hook_dll = ctypes.WinDLL(os.path.abspath("hook_dll.dll"))

# 安装钩子
hook_dll.InstallHook()

print("Monitoring browser operations... (Press Ctrl+C to stop)")
try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    pass

# 卸载钩子
hook_dll.UninstallHook()
print("Monitoring stopped. Check browser_ops.log")