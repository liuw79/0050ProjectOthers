const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');
const http = require('http');
const url = require('url');
const path = require('path');

class ProxyServer {
  constructor(database = null) {
    this.app = express();
    this.server = null;
    this.port = 8080; // 代理服务器端口
    this.isRunningFlag = false;
    this.restrictedUrls = new Set(); // 存储限制的URL
    this.accessLog = []; // 存储访问日志
    this.database = database; // 数据库实例
    
    // 初始化一些常见的短视频网站域名
    this.initDefaultRestrictedUrls();
    
    // 设置中间件
    this.setupMiddleware();
  }
  
  // 初始化默认限制的URL
  initDefaultRestrictedUrls() {
    // 添加一些常见的短视频网站域名
    const defaultUrls = [
      'douyin.com',
      'kuaishou.com',
      'bilibili.com',
      'ixigua.com',
      'toutiao.com',
      'weibo.com',
      'zhihu.com'
    ];
    
    defaultUrls.forEach(url => {
      this.restrictedUrls.add(url);
    });
  }
  
  // 设置中间件
  setupMiddleware() {
    // 记录所有请求的中间件
    this.app.use(async (req, res, next) => {
      const hostname = req.hostname;
      const fullUrl = req.protocol + '://' + req.get('host') + req.originalUrl;
      
      // 记录访问日志
      await this.logAccess(hostname, fullUrl);
      
      // 检查是否为限制的URL
      if (this.isUrlRestricted(hostname)) {
        console.log(`阻止访问: ${hostname}`);
        return res.status(403).send(`
          <html>
            <head><title>访问被限制</title></head>
            <body style="font-family: Arial, sans-serif; text-align: center; padding-top: 50px;">
              <h1>访问被限制</h1>
              <p>此网站已被限制访问</p>
              <p>网址: ${hostname}</p>
            </body>
          </html>
        `);
      }
      
      next();
    });
    
    // 代理中间件
    this.app.use('/', createProxyMiddleware({
      target: 'http://localhost', // 目标服务器，实际使用时会根据请求动态确定
      changeOrigin: true,
      secure: false, // 允许无效证书
      router: (req) => {
        // 动态确定目标服务器
        const protocol = req.protocol;
        const hostname = req.hostname;
        return `${protocol}://${hostname}`;
      },
      onError: (err, req, res) => {
        console.error('代理错误:', err.message);
        res.status(500).send('代理服务器错误');
      },
      onProxyReq: (proxyReq, req, res) => {
        // 可以在这里修改请求头等
        console.log(`代理请求: ${req.method} ${req.url}`);
      }
    }));
  }
  
  // 记录访问日志
  async logAccess(hostname, fullUrl) {
    const timestamp = new Date().toISOString();
    const isRestricted = this.isUrlRestricted(hostname);
    const logEntry = {
      timestamp,
      hostname,
      fullUrl,
      restricted: isRestricted
    };
    
    // 添加到内存日志数组
    this.accessLog.unshift(logEntry);
    
    // 限制日志数组大小，避免内存占用过多
    if (this.accessLog.length > 1000) {
      this.accessLog = this.accessLog.slice(0, 1000);
    }
    
    // 如果有数据库实例，也记录到数据库
    if (this.database) {
      try {
        await this.database.logAccess(hostname, fullUrl, isRestricted);
      } catch (error) {
        console.error('记录访问日志到数据库失败:', error);
      }
    }
    
    console.log(`访问记录: ${hostname} - ${timestamp} - ${isRestricted ? '已阻止' : '已允许'}`);
  }
  
  // 检查URL是否被限制
  isUrlRestricted(hostname) {
    // 检查完整域名或部分匹配
    for (const restrictedUrl of this.restrictedUrls) {
      if (hostname === restrictedUrl || hostname.includes('.' + restrictedUrl) || hostname.endsWith(restrictedUrl)) {
        return true;
      }
    }
    return false;
  }
  
  // 启动代理服务器
  start() {
    return new Promise((resolve, reject) => {
      if (this.isRunningFlag) {
        return reject(new Error('代理服务器已在运行'));
      }
      
      this.server = http.createServer(this.app);
      
      this.server.listen(this.port, () => {
        this.isRunningFlag = true;
        console.log(`代理服务器已启动，端口: ${this.port}`);
        console.log('请将系统代理设置为: 127.0.0.1:' + this.port);
        resolve();
      });
      
      this.server.on('error', (err) => {
        console.error('代理服务器错误:', err);
        reject(err);
      });
    });
  }
  
  // 停止代理服务器
  stop() {
    return new Promise((resolve, reject) => {
      if (!this.isRunningFlag || !this.server) {
        return reject(new Error('代理服务器未运行'));
      }
      
      this.server.close((err) => {
        if (err) {
          console.error('停止代理服务器时出错:', err);
          return reject(err);
        }
        
        this.isRunningFlag = false;
        this.server = null;
        console.log('代理服务器已停止');
        resolve();
      });
    });
  }
  
  // 检查服务器是否运行中
  isRunning() {
    return this.isRunningFlag;
  }
  
  // 添加限制的URL
  addRestrictedUrl(url) {
    this.restrictedUrls.add(url);
    console.log(`已添加限制URL: ${url}`);
  }
  
  // 移除限制的URL
  removeRestrictedUrl(url) {
    this.restrictedUrls.delete(url);
    console.log(`已移除限制URL: ${url}`);
  }
  
  // 获取所有限制的URL
  getRestrictedUrls() {
    return Array.from(this.restrictedUrls);
  }
  
  // 获取访问日志
  getAccessLog(limit = 100) {
    return this.accessLog.slice(0, limit);
  }
}

module.exports = ProxyServer;