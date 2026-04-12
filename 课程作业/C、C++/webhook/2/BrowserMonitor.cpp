// BrowserMonitor.cpp
#include <windows.h>
#include <iostream>
#include <string>
#include <shlobj.h>
#include <shlwapi.h>

#pragma comment(lib, "shlwapi.lib")
#pragma comment(lib, "shfolder.lib")

std::wstring g_logFilePath;

LRESULT CALLBACK WndProc(HWND hWnd, UINT message, WPARAM wParam, LPARAM lParam) {
    switch (message) {
    case WM_COPYDATA: {
        COPYDATASTRUCT* pcds = (COPYDATASTRUCT*)lParam;
        if (pcds->dwData == 0 && pcds->lpData) {
            std::wstring text((wchar_t*)pcds->lpData);

            // 确保目录存在
            size_t pos = g_logFilePath.find_last_of(L"\\/");
            if (pos != std::wstring::npos) {
                std::wstring dir = g_logFilePath.substr(0, pos);
                if (!dir.empty()) {
                    int result = SHCreateDirectoryExW(NULL, dir.c_str(), NULL);
                    if (result != ERROR_SUCCESS && result != ERROR_ALREADY_EXISTS) {
                        MessageBoxW(hWnd, L"无法创建日志目录", L"错误", MB_OK);
                        break;
                    }
                }
            }

            // 写入文件
            HANDLE hFile = CreateFileW(
                g_logFilePath.c_str(),
                FILE_APPEND_DATA,
                FILE_SHARE_READ,
                NULL,
                OPEN_ALWAYS,
                FILE_ATTRIBUTE_NORMAL,
                NULL
            );

            if (hFile != INVALID_HANDLE_VALUE) {
                DWORD bytesWritten;
                text += L"\r\n";
                WriteFile(
                    hFile,
                    text.c_str(),
                    static_cast<DWORD>(text.size() * sizeof(wchar_t)),
                    &bytesWritten,
                    NULL
                );
                CloseHandle(hFile);
            } else {
                DWORD error = GetLastError();
                std::wstring errorMsg = L"文件写入失败 (代码: " + std::to_wstring(error) + L")";
                MessageBoxW(hWnd, errorMsg.c_str(), L"错误", MB_OK);
            }
        }
        break;
    }
    case WM_DESTROY:
        PostQuitMessage(0);
        break;
    default:
        return DefWindowProcW(hWnd, message, wParam, lParam);
    }
    return 0;
}

int WINAPI wWinMain(HINSTANCE hInstance, HINSTANCE, PWSTR pCmdLine, int nCmdShow) {
    // 获取桌面路径
    wchar_t desktopPath[MAX_PATH];
    if (SUCCEEDED(SHGetFolderPathW(NULL, CSIDL_DESKTOPDIRECTORY, NULL, SHGFP_TYPE_CURRENT, desktopPath))) {
        g_logFilePath = std::wstring(desktopPath) + L"\\browser_activity.log";
    } else {
        g_logFilePath = L"C:\\browser_activity.log";
        MessageBoxW(NULL, L"使用默认日志路径", L"提示", MB_OK);
    }

    // 注册窗口类
    WNDCLASSW wc = { 0 };
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = L"BrowserMonitorClass";
    if (!RegisterClassW(&wc)) {
        MessageBoxW(NULL, L"窗口类注册失败", L"错误", MB_OK);
        return 1;
    }

    // 创建消息窗口
    HWND hWnd = CreateWindowW(wc.lpszClassName, L"", 0, 0, 0, 0, 0, HWND_MESSAGE, NULL, hInstance, NULL);
    if (!hWnd) {
        MessageBoxW(NULL, L"窗口创建失败", L"错误", MB_OK);
        return 1;
    }

    // 加载DLL
    HMODULE hDll = LoadLibraryW(L"BrowserHook.dll");
    if (!hDll) {
        MessageBoxW(NULL, L"无法加载DLL文件", L"错误", MB_OK);
        return 1;
    }

    // 安装钩子
    typedef BOOL(*InstallHookFunc)(HWND);
    InstallHookFunc installHook = (InstallHookFunc)GetProcAddress(hDll, "InstallHook");
    if (!installHook || !installHook(hWnd)) {
        MessageBoxW(NULL, L"钩子安装失败", L"错误", MB_OK);
        FreeLibrary(hDll);
        return 1;
    }

    // 消息循环
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // 卸载钩子
    typedef void(*UninstallHookFunc)();
    UninstallHookFunc uninstallHook = (UninstallHookFunc)GetProcAddress(hDll, "UninstallHook");
    if (uninstallHook) uninstallHook();

    FreeLibrary(hDll);
    return 0;
}