#include <Windows.h>
#include <iostream>
#include <fstream>

HHOOK hHook = NULL;
KBDLLHOOKSTRUCT kbdStruct;

// 将虚拟键码转换为键名
std::string GetKeyName(int code) {
    char name[128];
    UINT scanCode = MapVirtualKey(code, MAPVK_VK_TO_VSC);
    HKL layout = GetKeyboardLayout(0);
    
    long lParamValue = (scanCode << 16) | (1 << 24);
    GetKeyNameTextA(lParamValue, name, 128);
    
    return std::string(name);
}

// 键盘钩子回调函数
LRESULT CALLBACK LowLevelKeyboardProc(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode == HC_ACTION) {
        kbdStruct = *((KBDLLHOOKSTRUCT*)lParam);
        
        // 过滤系统快捷键（可选）
        if (kbdStruct.vkCode == VK_LWIN || kbdStruct.vkCode == VK_RWIN) 
            return 1;
        
        // 打印按键信息
        if (wParam == WM_KEYDOWN || wParam == WM_SYSKEYDOWN) {
            std::string keyName = GetKeyName(kbdStruct.vkCode);
            std::cout << "Key pressed: " << keyName 
                      << " [0x" << std::hex << kbdStruct.vkCode << "]\n";
        }
    }
    return CallNextHookEx(hHook, nCode, wParam, lParam);
}

int main() {
    // 设置控制台编码
    SetConsoleOutputCP(CP_UTF8);
    
    // 安装键盘钩子
    hHook = SetWindowsHookEx(WH_KEYBOARD_LL, LowLevelKeyboardProc, 
                            GetModuleHandle(NULL), 0);
    if (!hHook) {
        std::cerr << "Hook failed! Error: " << GetLastError() << "\n";
        return 1;
    }
    std::cout << "Hook installed. Monitoring keyboard input...\n";

    // 消息循环
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    UnhookWindowsHookEx(hHook);
    return 0;
}