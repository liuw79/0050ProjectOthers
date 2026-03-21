/*
 * 在线编译器版本 - 简化的浏览器模拟器
 * 适用于 https://www.onlinegdb.com/online_c_compiler
 * 或其他在线C编译器
 * 
 * 注意：此版本移除了Windows特定的API，仅用于演示核心逻辑
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// 模拟的浏览器结构
typedef struct {
    char url[1024];
    char content[4096];
    char history[10][1024];
    int historyIndex;
    int historyCount;
} SimpleBrowser;

// 简单的HTML标签移除函数
void removeHtmlTags(const char* html, char* text) {
    int i = 0, j = 0;
    int inTag = 0;
    int len = strlen(html);
    
    while (i < len) {
        if (html[i] == '<') {
            inTag = 1;
        } else if (html[i] == '>') {
            inTag = 0;
        } else if (!inTag) {
            if (html[i] == '&') {
                // 简单的HTML实体解码
                if (strncmp(&html[i], "&amp;", 5) == 0) {
                    text[j++] = '&';
                    i += 4;
                } else if (strncmp(&html[i], "&lt;", 4) == 0) {
                    text[j++] = '<';
                    i += 3;
                } else if (strncmp(&html[i], "&gt;", 4) == 0) {
                    text[j++] = '>';
                    i += 3;
                } else if (strncmp(&html[i], "&quot;", 6) == 0) {
                    text[j++] = '"';
                    i += 5;
                } else if (strncmp(&html[i], "&nbsp;", 6) == 0) {
                    text[j++] = ' ';
                    i += 5;
                } else {
                    text[j++] = html[i];
                }
            } else {
                text[j++] = html[i];
            }
        }
        i++;
    }
    text[j] = '\0';
}

// 模拟网页内容
const char* getSimulatedContent(const char* url) {
    if (strstr(url, "baidu.com") || strstr(url, "百度")) {
        return "<html><head><title>百度一下</title></head><body><h1>百度搜索</h1><p>这是一个模拟的百度页面。</p><p>搜索框：[___________] [百度一下]</p><p>热门搜索：新闻、图片、视频、地图</p></body></html>";
    } else if (strstr(url, "google.com") || strstr(url, "谷歌")) {
        return "<html><head><title>Google</title></head><body><h1>Google Search</h1><p>This is a simulated Google page.</p><p>Search: [___________] [Google Search]</p><p>Popular: News, Images, Videos, Maps</p></body></html>";
    } else if (strstr(url, "example.com")) {
        return "<html><head><title>Example Domain</title></head><body><h1>Example Domain</h1><p>This domain is for use in illustrative examples in documents.</p><p>You may use this domain in literature without prior coordination or asking for permission.</p></body></html>";
    } else if (strstr(url, "github.com")) {
        return "<html><head><title>GitHub</title></head><body><h1>GitHub</h1><p>Where the world builds software</p><p>Repositories: [Search repositories...]</p><p>Features: Code hosting, Version control, Collaboration</p></body></html>";
    } else {
        return "<html><head><title>简单浏览器</title></head><body><h1>页面未找到</h1><p>抱歉，无法加载该页面。</p><p>这是一个模拟的浏览器，只能显示预设的几个网站：</p><ul><li>baidu.com - 百度搜索</li><li>google.com - 谷歌搜索</li><li>example.com - 示例网站</li><li>github.com - GitHub</li></ul></body></html>";
    }
}

// 添加到历史记录
void addToHistory(SimpleBrowser* browser, const char* url) {
    if (browser->historyIndex < 9) {
        browser->historyIndex++;
        browser->historyCount = browser->historyIndex + 1;
    } else {
        // 移动历史记录
        for (int i = 0; i < 9; i++) {
            strcpy(browser->history[i], browser->history[i + 1]);
        }
    }
    strcpy(browser->history[browser->historyIndex], url);
}

// 导航到URL
void navigateToUrl(SimpleBrowser* browser, const char* url) {
    char fullUrl[1024];
    
    // 自动添加协议
    if (strstr(url, "://") == NULL) {
        if (strncmp(url, "www.", 4) == 0 || strchr(url, '.') != NULL) {
            sprintf(fullUrl, "http://%s", url);
        } else {
            sprintf(fullUrl, "http://www.google.com/search?q=%s", url);
        }
    } else {
        strcpy(fullUrl, url);
    }
    
    strcpy(browser->url, fullUrl);
    addToHistory(browser, fullUrl);
    
    // 获取模拟的网页内容
    const char* htmlContent = getSimulatedContent(fullUrl);
    removeHtmlTags(htmlContent, browser->content);
    
    printf("\n=== 已导航到: %s ===\n", fullUrl);
    printf("%s\n", browser->content);
}

// 显示帮助信息
void showHelp() {
    printf("\n=== 简单浏览器命令 ===\n");
    printf("go <url>     - 访问网址\n");
    printf("back         - 后退\n");
    printf("forward      - 前进\n");
    printf("refresh      - 刷新\n");
    printf("history      - 显示历史记录\n");
    printf("help         - 显示帮助\n");
    printf("quit         - 退出程序\n");
    printf("\n推荐测试网址:\n");
    printf("- baidu.com\n");
    printf("- google.com\n");
    printf("- example.com\n");
    printf("- github.com\n");
    printf("========================\n\n");
}

// 显示历史记录
void showHistory(SimpleBrowser* browser) {
    printf("\n=== 浏览历史 ===\n");
    if (browser->historyCount == 0) {
        printf("暂无浏览历史\n");
    } else {
        for (int i = 0; i < browser->historyCount; i++) {
            if (i == browser->historyIndex) {
                printf("-> %s (当前)\n", browser->history[i]);
            } else {
                printf("   %s\n", browser->history[i]);
            }
        }
    }
    printf("================\n\n");
}

int main() {
    SimpleBrowser browser = {0};
    browser.historyIndex = -1;
    browser.historyCount = 0;
    
    printf("=================================\n");
    printf("    欢迎使用简单浏览器模拟器\n");
    printf("=================================\n");
    printf("这是一个在线编译器版本的浏览器模拟器\n");
    printf("可以模拟基本的网页浏览功能\n\n");
    
    showHelp();
    
    char command[1024];
    char url[1024];
    
    while (1) {
        printf("浏览器> ");
        if (!fgets(command, sizeof(command), stdin)) {
            break;
        }
        
        // 移除换行符
        command[strcspn(command, "\n")] = 0;
        
        if (strncmp(command, "go ", 3) == 0) {
            strcpy(url, command + 3);
            navigateToUrl(&browser, url);
        } else if (strcmp(command, "back") == 0) {
            if (browser.historyIndex > 0) {
                browser.historyIndex--;
                navigateToUrl(&browser, browser.history[browser.historyIndex]);
                browser.historyIndex--; // 因为navigateToUrl会增加索引
            } else {
                printf("无法后退，已在历史记录的开始位置\n");
            }
        } else if (strcmp(command, "forward") == 0) {
            if (browser.historyIndex < browser.historyCount - 1) {
                browser.historyIndex++;
                navigateToUrl(&browser, browser.history[browser.historyIndex]);
                browser.historyIndex--; // 因为navigateToUrl会增加索引
            } else {
                printf("无法前进，已在历史记录的末尾位置\n");
            }
        } else if (strcmp(command, "refresh") == 0) {
            if (strlen(browser.url) > 0) {
                navigateToUrl(&browser, browser.url);
                browser.historyIndex--; // 因为navigateToUrl会增加索引
            } else {
                printf("当前没有页面可以刷新\n");
            }
        } else if (strcmp(command, "history") == 0) {
            showHistory(&browser);
        } else if (strcmp(command, "help") == 0) {
            showHelp();
        } else if (strcmp(command, "quit") == 0 || strcmp(command, "exit") == 0) {
            printf("感谢使用简单浏览器！再见！\n");
            break;
        } else if (strlen(command) == 0) {
            // 空命令，继续
            continue;
        } else {
            printf("未知命令: %s\n", command);
            printf("输入 'help' 查看可用命令\n\n");
        }
    }
    
    return 0;
}