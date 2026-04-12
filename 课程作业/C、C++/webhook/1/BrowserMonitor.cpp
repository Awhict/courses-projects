#include <windows.h>
#include <iostream>
#include <string>

const wchar_t* g_logFileName = L"browser_activity.log";

// 窗口过程
LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message) {
    case WM_COPYDATA: {
        COPYDATASTRUCT* pcds = (COPYDATASTRUCT*)lParam;
        if (pcds->dwData == 0 && pcds->lpData) {
            std::wstring text((wchar_t*)pcds->lpData);
            HANDLE hFile = CreateFile(g_logFileName, FILE_APPEND_DATA, FILE_SHARE_READ, NULL, OPEN_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
            if (hFile != INVALID_HANDLE_VALUE) {
                DWORD bytesWritten;
                WriteFile(hFile, text.c_str(), text.size() * sizeof(wchar_t), &bytesWritten, NULL);
                WriteFile(hFile, L"\r\n", 2 * sizeof(wchar_t), &bytesWritten, NULL);
                CloseHandle(hFile);
            }
        }
        break;
    }
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProc(hWnd, message, wParam, lParam);
    }
    return 0;
}

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE, PWSTR pCmdLine, int nCmdShow) {
    // 注册窗口类
    WNDCLASSW wc = {0};
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = L"BrowserMonitorClass";
    RegisterClassW(&wc);

    // 创建隐藏窗口
    HWND hWnd = CreateWindowW(wc.lpszClassName, L"", 0, 0, 0, 0, 0, HWND_MESSAGE, NULL, hInstance, NULL);
    if (!hWnd) return 0;

    // 加载DLL
    HMODULE hDll = LoadLibrary(L"BrowserHook.dll");
    if (!hDll) {
        MessageBoxW(NULL, L"Failed to load DLL", L"Error", MB_OK);
        return 0;
    }

    // 获取并安装钩子
    typedef BOOL (*InstallHookFunc)(HWND);
    InstallHookFunc installHook = (InstallHookFunc)GetProcAddress(hDll, "InstallHook");
    if (installHook && installHook(hWnd)) {
        MSG msg;
        while (GetMessage(&msg, NULL, 0, 0)) {
            TranslateMessage(&msg);
            DispatchMessage(&msg);
        }

        // 卸载钩子
        typedef void (*UninstallHookFunc)();
        UninstallHookFunc uninstallHook = (UninstallHookFunc)GetProcAddress(hDll, "UninstallHook");
        if (uninstallHook) uninstallHook();
    }

    FreeLibrary(hDll);
    return 0;
}