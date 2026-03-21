const Database = require('better-sqlite3');
const path = require('path');

class DatabaseWrapper {
  constructor() {
    this.dbPath = path.join(__dirname, '..', 'data', 'restrict_url.db');
    this.db = null;
    
    const fs = require('fs');
    const dataDir = path.dirname(this.dbPath);
    if (!fs.existsSync(dataDir)) {
      fs.mkdirSync(dataDir, { recursive: true });
    }
  }
  
  connect() {
    return new Promise((resolve, reject) => {
      try {
        this.db = new Database(this.dbPath);
        console.log('已连接到SQLite数据库');
        this.initTables();
        resolve();
      } catch (err) {
        console.error('数据库连接错误:', err.message);
        reject(err);
      }
    });
  }
  
  initTables() {
    const createRestrictedUrlsTable = `
      CREATE TABLE IF NOT EXISTS restricted_urls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )
    `;
    
    const createAccessLogTable = `
      CREATE TABLE IF NOT EXISTS access_log (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hostname TEXT NOT NULL,
        full_url TEXT NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        restricted BOOLEAN DEFAULT 0
      )
    `;
    
    this.db.exec(createRestrictedUrlsTable);
    this.db.exec(createAccessLogTable);
    console.log('数据库表初始化完成');
  }
  
  addRestrictedUrl(url) {
    return new Promise((resolve, reject) => {
      try {
        const stmt = this.db.prepare('INSERT OR IGNORE INTO restricted_urls (url) VALUES (?)');
        const result = stmt.run(url);
        console.log(`已添加限制URL: ${url}, ID: ${result.lastInsertRowid}`);
        resolve({ id: result.lastInsertRowid, url });
      } catch (err) {
        console.error('添加限制URL失败:', err.message);
        reject(err);
      }
    });
  }
  
  removeRestrictedUrl(url) {
    return new Promise((resolve, reject) => {
      try {
        const stmt = this.db.prepare('DELETE FROM restricted_urls WHERE url = ?');
        const result = stmt.run(url);
        console.log(`已移除限制URL: ${url}, 影响行数: ${result.changes}`);
        resolve({ changes: result.changes, url });
      } catch (err) {
        console.error('移除限制URL失败:', err.message);
        reject(err);
      }
    });
  }
  
  getRestrictedUrls() {
    return new Promise((resolve, reject) => {
      try {
        const stmt = this.db.prepare('SELECT * FROM restricted_urls ORDER BY created_at DESC');
        const rows = stmt.all();
        resolve(rows);
      } catch (err) {
        console.error('获取限制URL列表失败:', err.message);
        reject(err);
      }
    });
  }
  
  logAccess(hostname, fullUrl, restricted = false) {
    return new Promise((resolve, reject) => {
      try {
        const stmt = this.db.prepare('INSERT INTO access_log (hostname, full_url, restricted) VALUES (?, ?, ?)');
        const result = stmt.run(hostname, fullUrl, restricted ? 1 : 0);
        resolve({ id: result.lastInsertRowid });
      } catch (err) {
        console.error('记录访问日志失败:', err.message);
        reject(err);
      }
    });
  }
  
  getAccessLog(limit = 100, offset = 0) {
    return new Promise((resolve, reject) => {
      try {
        const stmt = this.db.prepare(`
          SELECT * FROM access_log 
          ORDER BY timestamp DESC 
          LIMIT ? OFFSET ?
        `);
        const rows = stmt.all(limit, offset);
        resolve(rows);
      } catch (err) {
        console.error('获取访问日志失败:', err.message);
        reject(err);
      }
    });
  }
  
  cleanOldAccessLog(daysToKeep = 30) {
    return new Promise((resolve, reject) => {
      try {
        const stmt = this.db.prepare(`
          DELETE FROM access_log 
          WHERE timestamp < datetime('now', '-' || ? || ' days')
        `);
        const result = stmt.run(daysToKeep);
        console.log(`已清理 ${result.changes} 条旧访问日志`);
        resolve({ changes: result.changes });
      } catch (err) {
        console.error('清理旧访问日志失败:', err.message);
        reject(err);
      }
    });
  }
  
  close() {
    return new Promise((resolve, reject) => {
      if (this.db) {
        try {
          this.db.close();
          console.log('数据库连接已关闭');
          resolve();
        } catch (err) {
          console.error('关闭数据库连接失败:', err.message);
          reject(err);
        }
      } else {
        resolve();
      }
    });
  }
}

module.exports = DatabaseWrapper;
