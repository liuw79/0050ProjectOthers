#include <windows.h>
#include <wininet.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <wchar.h>

// 强制使用Unicode版本
#ifndef UNICODE
#define UNICODE
#endif
#ifndef _UNICODE
#define _UNICODE
#endif

#pragma comment(lib, "wininet.lib")
#pragma comment(lib, "user32.lib")
#pragma comment(lib, "gdi32.lib")
#pragma comment(lib, "kernel32.lib")

#define ID_URL_EDIT 1001
#define ID_GO_BUTTON 1002
#define ID_CONTENT_EDIT 1003
#define ID_BACK_BUTTON 1004
#define ID_FORWARD_BUTTON 1005
#define ID_REFRESH_BUTTON 1006

HWND hUrlEdit, hContentEdit, hGoButton, hBackButton, hForwardButton, hRefreshButton;
wchar_t currentUrl[1024] = L"";
wchar_t history[10][1024];
int historyIndex = -1;
int historyCount = 0;

// 简单的HTML标签移除函数
void removeHtmlTags(const char* html, wchar_t* text) {
    int i = 0, j = 0;
    int inTag = 0;
    int len = strlen(html);
    
    // 将UTF-8转换为Unicode
    wchar_t* whtml = (wchar_t*)malloc((len + 1) * sizeof(wchar_t));
    MultiByteToWideChar(CP_UTF8, 0, html, -1, whtml, len + 1);
    
    int wlen = wcslen(whtml);
    while (i < wlen) {
        if (whtml[i] == L'<') {
            inTag = 1;
        } else if (whtml[i] == L'>') {
            inTag = 0;
        } else if (!inTag) {
            if (whtml[i] == L'&') {
                // 简单的HTML实体解码
                if (wcsncmp(&whtml[i], L"&amp;", 5) == 0) {
                    text[j++] = L'&';
                    i += 4;
                } else if (wcsncmp(&whtml[i], L"&lt;", 4) == 0) {
                    text[j++] = L'<';
                    i += 3;
                } else if (wcsncmp(&whtml[i], L"&gt;", 4) == 0) {
                    text[j++] = L'>';
                    i += 3;
                } else if (wcsncmp(&whtml[i], L"&quot;", 6) == 0) {
                    text[j++] = L'"';
                    i += 5;
                } else if (wcsncmp(&whtml[i], L"&nbsp;", 6) == 0) {
                    text[j++] = L' ';
                    i += 5;
                } else {
                    text[j++] = whtml[i];
                }
            } else {
                text[j++] = whtml[i];
            }
        }
        i++;
    }
    text[j] = L'\0';
    free(whtml);
}

// 下载网页内容
char* downloadPage(const wchar_t* url) {
    // 将Unicode URL转换为ANSI用于WinINet
    char* ansiUrl = (char*)malloc(2048);
    WideCharToMultiByte(CP_ACP, 0, url, -1, ansiUrl, 2048, NULL, NULL);
    HINTERNET hInternet, hConnect;
    char* buffer = NULL;
    DWORD bytesRead;
    DWORD totalSize = 0;
    DWORD bufferSize = 4096;
    
    hInternet = InternetOpenA("SimpleBrowser/1.0", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
    if (!hInternet) {
        free(ansiUrl);
        return NULL;
    }
    
    hConnect = InternetOpenUrlA(hInternet, ansiUrl, NULL, 0, INTERNET_FLAG_RELOAD, 0);
    if (!hConnect) {
        InternetCloseHandle(hInternet);
        free(ansiUrl);
        return NULL;
    }
    free(ansiUrl);
    
    buffer = (char*)malloc(bufferSize);
    if (!buffer) {
        InternetCloseHandle(hConnect);
        InternetCloseHandle(hInternet);
        return NULL;
    }
    
    char tempBuffer[1024];
    while (InternetReadFile(hConnect, tempBuffer, sizeof(tempBuffer) - 1, &bytesRead) && bytesRead > 0) {
        if (totalSize + bytesRead >= bufferSize) {
            bufferSize *= 2;
            buffer = (char*)realloc(buffer, bufferSize);
            if (!buffer) {
                InternetCloseHandle(hConnect);
                InternetCloseHandle(hInternet);
                return NULL;
            }
        }
        memcpy(buffer + totalSize, tempBuffer, bytesRead);
        totalSize += bytesRead;
    }
    
    buffer[totalSize] = '\0';
    
    InternetCloseHandle(hConnect);
    InternetCloseHandle(hInternet);
    
    return buffer;
}

// 添加到历史记录
void addToHistory(const wchar_t* url) {
    if (historyIndex < 9) {
        historyIndex++;
        historyCount = historyIndex + 1;
    } else {
        // 移动历史记录
        for (int i = 0; i < 9; i++) {
            wcscpy(history[i], history[i + 1]);
        }
    }
    wcscpy(history[historyIndex], url);
}

// 导航到URL
void navigateToUrl(const wchar_t* url) {
    wchar_t fullUrl[1024];
    
    // 自动添加协议
    if (wcsstr(url, L"://") == NULL) {
        if (wcsncmp(url, L"www.", 4) == 0 || wcschr(url, L'.') != NULL) {
            swprintf(fullUrl, 1024, L"http://%s", url);
        } else {
            swprintf(fullUrl, 1024, L"http://www.google.com/search?q=%s", url);
        }
    } else {
        wcscpy(fullUrl, url);
    }
    
    SetWindowTextW(hUrlEdit, fullUrl);
    wcscpy(currentUrl, fullUrl);
    addToHistory(fullUrl);
    
    SetWindowTextW(hContentEdit, L"正在加载...");
    
    char* htmlContent = downloadPage(fullUrl);
    if (htmlContent) {
        wchar_t* textContent = (wchar_t*)malloc(strlen(htmlContent) * 2 * sizeof(wchar_t));
        if (textContent) {
            removeHtmlTags(htmlContent, textContent);
            SetWindowTextW(hContentEdit, textContent);
            free(textContent);
        }
        free(htmlContent);
    } else {
        SetWindowTextW(hContentEdit, L"无法加载页面。请检查URL是否正确。");
    }
}

// 窗口过程
LRESULT CALLBACK WindowProc(HWND hwnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_CREATE: {
            HINSTANCE hInstance = GetModuleHandle(NULL);
            
            // 创建地址栏
            CreateWindowW(L"STATIC", L"地址:", WS_VISIBLE | WS_CHILD,
                        10, 10, 50, 25, hwnd, NULL, hInstance, NULL);
            
            hUrlEdit = CreateWindowW(L"EDIT", L"", WS_VISIBLE | WS_CHILD | WS_BORDER | ES_AUTOHSCROLL,
                                   70, 10, 400, 25, hwnd, (HMENU)ID_URL_EDIT, hInstance, NULL);
            
            hGoButton = CreateWindowW(L"BUTTON", L"转到", WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                                    480, 10, 60, 25, hwnd, (HMENU)ID_GO_BUTTON, hInstance, NULL);
            
            // 创建导航按钮
            hBackButton = CreateWindowW(L"BUTTON", L"后退", WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                                      10, 45, 60, 25, hwnd, (HMENU)ID_BACK_BUTTON, hInstance, NULL);
            
            hForwardButton = CreateWindowW(L"BUTTON", L"前进", WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                                         80, 45, 60, 25, hwnd, (HMENU)ID_FORWARD_BUTTON, hInstance, NULL);
            
            hRefreshButton = CreateWindowW(L"BUTTON", L"刷新", WS_VISIBLE | WS_CHILD | BS_PUSHBUTTON,
                                         150, 45, 60, 25, hwnd, (HMENU)ID_REFRESH_BUTTON, hInstance, NULL);
            
            // 创建内容显示区域
            hContentEdit = CreateWindowW(L"EDIT", L"欢迎使用简单浏览器！\r\n\r\n请在地址栏输入网址，例如：\r\nwww.example.com\r\nbaidu.com\r\n\r\n注意：此浏览器只能显示纯文本内容，不支持CSS、JavaScript等现代网页技术。",
                                       WS_VISIBLE | WS_CHILD | WS_BORDER | WS_VSCROLL | ES_MULTILINE | ES_READONLY,
                                       10, 80, 760, 400, hwnd, (HMENU)ID_CONTENT_EDIT, hInstance, NULL);
            
            // 设置默认字体
            HFONT hFont = CreateFontW(14, 0, 0, 0, FW_NORMAL, FALSE, FALSE, FALSE,
                                   DEFAULT_CHARSET, OUT_DEFAULT_PRECIS, CLIP_DEFAULT_PRECIS,
                                   DEFAULT_QUALITY, DEFAULT_PITCH | FF_DONTCARE, L"微软雅黑");
            
            SendMessage(hUrlEdit, WM_SETFONT, (WPARAM)hFont, TRUE);
            SendMessage(hContentEdit, WM_SETFONT, (WPARAM)hFont, TRUE);
            SendMessage(hGoButton, WM_SETFONT, (WPARAM)hFont, TRUE);
            SendMessage(hBackButton, WM_SETFONT, (WPARAM)hFont, TRUE);
            SendMessage(hForwardButton, WM_SETFONT, (WPARAM)hFont, TRUE);
            SendMessage(hRefreshButton, WM_SETFONT, (WPARAM)hFont, TRUE);
            
            break;
        }
        
        case WM_COMMAND: {
            switch (LOWORD(wParam)) {
                case ID_GO_BUTTON: {
                    wchar_t url[1024];
                    GetWindowTextW(hUrlEdit, url, sizeof(url)/sizeof(wchar_t));
                    if (wcslen(url) > 0) {
                        navigateToUrl(url);
                    }
                    break;
                }
                
                case ID_BACK_BUTTON: {
                    if (historyIndex > 0) {
                        historyIndex--;
                        navigateToUrl(history[historyIndex]);
                        historyIndex--; // 因为navigateToUrl会增加索引
                    }
                    break;
                }
                
                case ID_FORWARD_BUTTON: {
                    if (historyIndex < historyCount - 1) {
                        historyIndex++;
                        navigateToUrl(history[historyIndex]);
                        historyIndex--; // 因为navigateToUrl会增加索引
                    }
                    break;
                }
                
                case ID_REFRESH_BUTTON: {
                    if (wcslen(currentUrl) > 0) {
                        navigateToUrl(currentUrl);
                        historyIndex--; // 因为navigateToUrl会增加索引
                    }
                    break;
                }
                
                case ID_URL_EDIT: {
                    if (HIWORD(wParam) == EN_SETFOCUS) {
                        SendMessage(hUrlEdit, EM_SETSEL, 0, -1);
                    }
                    break;
                }
            }
            
            // 处理回车键
            if (HIWORD(wParam) == EN_CHANGE && LOWORD(wParam) == ID_URL_EDIT) {
                if (GetAsyncKeyState(VK_RETURN) & 0x8000) {
                    wchar_t url[1024];
                    GetWindowTextW(hUrlEdit, url, sizeof(url)/sizeof(wchar_t));
                    if (wcslen(url) > 0) {
                        navigateToUrl(url);
                    }
                }
            }
            break;
        }
        
        case WM_SIZE: {
            int width = LOWORD(lParam);
            int height = HIWORD(lParam);
            
            // 调整控件大小
            SetWindowPos(hUrlEdit, NULL, 70, 10, width - 150, 25, SWP_NOZORDER);
            SetWindowPos(hGoButton, NULL, width - 70, 10, 60, 25, SWP_NOZORDER);
            SetWindowPos(hContentEdit, NULL, 10, 80, width - 20, height - 90, SWP_NOZORDER);
            break;
        }
        
        case WM_DESTROY:
            PostQuitMessage(0);
            break;
            
        default:
            return DefWindowProc(hwnd, uMsg, wParam, lParam);
    }
    return 0;
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow) {
    const wchar_t* className = L"SimpleBrowserWindow";
    
    // 注册窗口类
    WNDCLASSW wc = {0};
    wc.lpfnWndProc = WindowProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = className;
    wc.hbrBackground = (HBRUSH)(COLOR_WINDOW + 1);
    wc.hCursor = LoadCursor(NULL, IDC_ARROW);
    wc.hIcon = LoadIcon(NULL, IDI_APPLICATION);
    
    if (!RegisterClassW(&wc)) {
        MessageBoxW(NULL, L"窗口类注册失败！", L"错误", MB_OK | MB_ICONERROR);
        return 1;
    }
    
    // 创建窗口
    HWND hwnd = CreateWindowW(className, L"简单浏览器 - 纯文本版",
                            WS_OVERLAPPEDWINDOW,
                            CW_USEDEFAULT, CW_USEDEFAULT, 800, 600,
                            NULL, NULL, hInstance, NULL);
    
    if (!hwnd) {
        MessageBoxW(NULL, L"窗口创建失败！", L"错误", MB_OK | MB_ICONERROR);
        return 1;
    }
    
    ShowWindow(hwnd, nCmdShow);
    UpdateWindow(hwnd);
    
    // 消息循环
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }
    
    return msg.wParam;
}