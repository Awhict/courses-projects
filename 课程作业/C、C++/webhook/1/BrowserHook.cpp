#include <windows.h>
#include <psapi.h>
#include <tchar.h>

#pragma comment(lib, "psapi.lib")

HHOOK g_hook = NULL;
HWND g_hostWnd = NULL;

// 钩子过程，处理WH_CALLWNDPROCRET消息
LRESULT CALLBACK CallWndProcRet(int nCode, WPARAM wParam, LPARAM lParam) {
    if (nCode >= 0) {
        CWPRETSTRUCT* pMsg = (CWPRETSTRUCT*)lParam;
        if (pMsg->message == WM_SETTEXT) {
            HWND hWnd = pMsg->hwnd;
            DWORD processId;
            GetWindowThreadProcessId(hWnd, &processId);

            HANDLE hProcess = OpenProcess(PROCESS_QUERY_INFORMATION | PROCESS_VM_READ, FALSE, processId);
            if (hProcess) {
                TCHAR exePath[MAX_PATH];
                if (GetModuleFileNameEx(hProcess, NULL, exePath, MAX_PATH)) {
                    TCHAR* exeName = _tcsrchr(exePath, _T('\\'));
                    exeName = exeName ? exeName + 1 : exePath;

                    if (_tcsicmp(exeName, _T("chrome.exe")) == 0 ||
                        _tcsicmp(exeName, _T("msedge.exe")) == 0 ||
                        _tcsicmp(exeName, _T("firefox.exe")) == 0 ||
                        _tcsicmp(exeName, _T("iexplore.exe")) == 0) {

                        WCHAR textBuffer[2048];
                        if (SendMessageW(hWnd, WM_GETTEXT, 2048, (LPARAM)textBuffer)) {
                            if (g_hostWnd) {
                                COPYDATASTRUCT cds;
                                cds.dwData = 0;
                                cds.cbData = (wcslen(textBuffer) + 1) * sizeof(WCHAR);
                                cds.lpData = textBuffer;
                                SendMessage(g_hostWnd, WM_COPYDATA, (WPARAM)hWnd, (LPARAM)&cds);
                            }
                        }
                    }
                }
                CloseHandle(hProcess);
            }
        }
    }
    return CallNextHookEx(g_hook, nCode, wParam, lParam);
}

// 导出函数：安装钩子
extern "C" __declspec(dllexport) BOOL InstallHook(HWND hHostWnd) {
    g_hostWnd = hHostWnd;
    g_hook = SetWindowsHookEx(WH_CALLWNDPROCRET, CallWndProcRet, GetModuleHandle(_T("BrowserHook.dll")), 0);
    return g_hook != NULL;
}

// 导出函数：卸载钩子
extern "C" __declspec(dllexport) void UninstallHook() {
    if (g_hook) {
        UnhookWindowsHookEx(g_hook);
        g_hook = NULL;
    }
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    return TRUE;
}