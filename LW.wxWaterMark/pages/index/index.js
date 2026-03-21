/*
【开发协作备忘】
1. 功能完成/满意/告一段落时，主动建议 Git 提交。
2. 始终使用中文沟通。
3. 日志优先按钮复制，否则手动管理（删除旧日志，读取新日志）。
4. 反复出错的问题添加注释说明。
5. 复杂代码问题，提醒用户提供示例代码供学习。
6. 疑难或反复修改无效问题，提醒用户寻求外部帮助并同步结果。
*/

// pages/index/index.js - 真机优化版本

const PLACEHOLDER_USAGE = '____';
const WATERMARK_PREFIX = '仅供';
const WATERMARK_SUFFIX = '使用不得用于其他用途，有效期至';

// 格式化日期为YY/MM/DD
function formatDate(date) {
  const year = date.getFullYear().toString().slice(-2);
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${year}/${month}/${day}`;
}

Page({
  /**
   * 页面的初始数据
   */
  data: {
    tempFilePath: null,          // 选择的图片路径
    fullWatermarkText: '',       // 当前水印文字
    imageMaxHeightPx: 300,        // 图片预览最大高度（像素）
    canvasWidth: 400,
    canvasHeight: 300,
    savedImages: []              // 历史保存的图片列表
  },

  /**
   * 生命周期函数--监听页面加载
   */
  onLoad: function() {
    console.log('页面加载 - 真机优化版本');
    
    // 获取系统信息
    wx.getSystemInfo({
      success: (res) => {
        console.log('系统信息:', res);
        this.setData({
          imageMaxHeightPx: res.windowHeight * 0.4
        });
      }
    });

    // 生成默认水印文本
    const today = new Date();
    const expiry = new Date(today.getTime() + 30 * 24 * 60 * 60 * 1000); // 30天后
    const expiryDateString = formatDate(expiry);
    const usage = wx.getStorageSync('lastUsage') || PLACEHOLDER_USAGE;
    const defaultText = `${WATERMARK_PREFIX}${usage}${WATERMARK_SUFFIX}${expiryDateString}`;

    // 加载历史图片
    this.loadSavedImages();

    this.setData({
      fullWatermarkText: defaultText
    });
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {
    // 保存用户输入的用途
    const currentText = this.data.fullWatermarkText;
    if (currentText.includes(WATERMARK_PREFIX) && currentText.includes(WATERMARK_SUFFIX)) {
      const startIndex = WATERMARK_PREFIX.length;
      const endIndex = currentText.indexOf(WATERMARK_SUFFIX);
      if (startIndex < endIndex) {
        const extractedUsage = currentText.substring(startIndex, endIndex);
        if (extractedUsage !== PLACEHOLDER_USAGE) {
          wx.setStorageSync('lastUsage', extractedUsage);
        }
      }
    }
  },

  /**
   * 加载历史图片
   */
  loadSavedImages: function() {
    const savedImages = wx.getStorageSync('savedImages') || [];
    console.log('加载历史图片:', savedImages.length);
    this.setData({
      savedImages: savedImages
    });
  },

  /**
   * 保存图片到历史
   */
  saveImageToHistory: function(filePath) {
    if (!filePath) return;
    
    let savedImages = wx.getStorageSync('savedImages') || [];
    
    // 检查是否已存在
    const exists = savedImages.some(img => img.path === filePath);
    if (exists) {
      console.log('图片已在历史中');
      return;
    }
    
    // 添加到历史（最多保存10张）
    savedImages.unshift({
      path: filePath,
      timestamp: Date.now()
    });
    
    if (savedImages.length > 10) {
      savedImages = savedImages.slice(0, 10);
    }
    
    wx.setStorageSync('savedImages', savedImages);
    this.loadSavedImages();
    console.log('图片已保存到历史');
  },

  /**
   * 选择图片
   */
  chooseImage: function() {
    console.log('开始选择图片');
    wx.chooseImage({
      count: 1,
      sourceType: ['album', 'camera'],
      success: (res) => {
        console.log('图片选择成功:', res.tempFilePaths[0]);
        const filePath = res.tempFilePaths[0];
        this.setData({
          tempFilePath: filePath
        });
        // 保存到历史
        this.saveImageToHistory(filePath);
      },
      fail: (err) => {
        console.error('图片选择失败:', err);
        if (err.errMsg !== "chooseImage:fail cancel") {
          wx.showToast({ title: '图片选择失败', icon: 'none' });
        }
      }
    });
  },

  /**
   * 选择历史图片
   */
  selectSavedImage: function(e) {
    const index = e.currentTarget.dataset.index;
    const imagePath = this.data.savedImages[index].path;
    console.log('选择历史图片:', imagePath);
    
    // 检查文件是否仍然存在
    wx.getFileInfo({
      filePath: imagePath,
      success: () => {
        this.setData({
          tempFilePath: imagePath
        });
        wx.showToast({ title: '已选择', icon: 'success', duration: 1000 });
      },
      fail: () => {
        wx.showToast({ title: '图片已失效，请重新选择', icon: 'none' });
        // 从历史中移除
        this.deleteSavedImage(index);
      }
    });
  },

  /**
   * 删除历史图片
   */
  deleteSavedImage: function(index) {
    const savedImages = this.data.savedImages;
    savedImages.splice(index, 1);
    wx.setStorageSync('savedImages', savedImages);
    this.loadSavedImages();
  },

  /**
   * 长按删除历史图片
   */
  onLongPressSavedImage: function(e) {
    const index = e.currentTarget.dataset.index;
    wx.showModal({
      title: '删除图片',
      content: '确定要从历史中删除这张图片吗？',
      success: (res) => {
        if (res.confirm) {
          this.deleteSavedImage(index);
          wx.showToast({ title: '已删除', icon: 'success', duration: 1000 });
        }
      }
    });
  },

  /**
   * 水印文字变化处理
   */
  onWatermarkTextChange: function(e) {
    this.setData({
      fullWatermarkText: e.detail.value
    });
  },

  /**
   * 生成水印图片
   */
  generateWatermarkedImage: function() {
    console.log('开始生成水印图片');
    
    if (!this.data.tempFilePath) {
      wx.showToast({ title: '请先选择图片', icon: 'none' });
      return;
    }

    if (this.data.fullWatermarkText.includes(PLACEHOLDER_USAGE)) {
      wx.showToast({ title: '请填写水印用途', icon: 'none' });
      return;
    }

    if (!this.data.fullWatermarkText.trim()) {
      wx.showToast({ title: '水印文字不能为空', icon: 'none' });
      return;
    }

    wx.showLoading({ title: '生成中...' });

    // 获取图片信息
    wx.getImageInfo({
      src: this.data.tempFilePath,
      success: (res) => {
        console.log('图片信息:', res);
        this.drawWatermark(res.width, res.height);
      },
      fail: (err) => {
        console.error('获取图片信息失败:', err);
        wx.hideLoading();
        wx.showToast({ title: '图片处理失败', icon: 'none' });
      }
    });
  },

  // 绘制水印 - 45度斜向水印
  drawWatermark: function(imgWidth, imgHeight) {
    console.log('开始绘制水印, 图片尺寸:', imgWidth, 'x', imgHeight);
    
    // 设置Canvas尺寸与图片相同
    this.setData({
      canvasWidth: imgWidth,
      canvasHeight: imgHeight
    });
    
    // 延迟一下确保Canvas尺寸更新
    setTimeout(() => {
      const ctx = wx.createCanvasContext('watermarkCanvas', this);
      
      // 先清空画布
      ctx.clearRect(0, 0, imgWidth, imgHeight);
      
      // 绘制原图 - 填满整个Canvas
      console.log('绘制原图:', this.data.tempFilePath);
      ctx.drawImage(this.data.tempFilePath, 0, 0, imgWidth, imgHeight);
      
      // 设置水印样式
      const fontSize = Math.max(16, Math.min(imgWidth, imgHeight) / 25);
      const watermarkText = this.data.fullWatermarkText;
      
      console.log('水印文字:', watermarkText, '字体大小:', fontSize);
      
      ctx.setFontSize(fontSize);
      ctx.setFillStyle('rgba(0, 0, 0, 0.3)'); // 稍微降低透明度避免遮挡
      ctx.setTextAlign('center');
      ctx.setTextBaseline('middle');
      
      // 绘制多行斜向水印覆盖整个图片
      const spacing = fontSize * 5; // 水印行间距
      const diagonal = Math.sqrt(imgWidth * imgWidth + imgHeight * imgHeight); // 对角线长度
      const centerX = imgWidth / 2;
      const centerY = imgHeight / 2;
      
      console.log('绘制斜向水印，间距:', spacing);
      
      // 保存当前状态
      ctx.save();
      
      // 移动到中心点
      ctx.translate(centerX, centerY);
      
      // 旋转-45度（从左下到右上）
      ctx.rotate(-Math.PI / 4);
      
      // 绘制多行水印，覆盖整个图片区域
      const rowCount = Math.ceil(diagonal / spacing) + 2;
      const startY = -diagonal / 2;
      
      for (let i = 0; i < rowCount; i++) {
        const y = startY + i * spacing;
        ctx.fillText(watermarkText, 0, y);
      }
      
      // 恢复状态
      ctx.restore();
      
      console.log('开始执行draw');
      
      // 执行绘制
      ctx.draw(false, () => {
        console.log('Canvas绘制完成，开始导出');
        
        // 等待绘制完成后导出
        setTimeout(() => {
          wx.canvasToTempFilePath({
            canvasId: 'watermarkCanvas',
            x: 0,
            y: 0,
            width: imgWidth,
            height: imgHeight,
            destWidth: imgWidth,  // 保持原始尺寸
            destHeight: imgHeight, // 保持原始尺寸
            quality: 0.9,
            fileType: 'jpg',
            success: (tempRes) => {
              console.log('图片导出成功:', tempRes.tempFilePath);
              console.log('导出尺寸参数 - 原图:', imgWidth + 'x' + imgHeight);
              this.saveToAlbum(tempRes.tempFilePath);
            },
            fail: (err) => {
              console.error('图片导出失败:', err);
              wx.hideLoading();
              wx.showToast({ 
                title: '生成失败: ' + (err.errMsg || '未知错误'), 
                icon: 'none',
                duration: 3000
              });
            }
          }, this);
        }, 1000); // 减少等待时间
      });
    }, 200); // 等待Canvas尺寸更新
  },

  // 保存到相册
  saveToAlbum: function(filePath) {
    console.log('保存图片到相册:', filePath);
    
    wx.saveImageToPhotosAlbum({
      filePath: filePath,
      success: () => {
        wx.hideLoading();
        wx.showToast({ title: '已保存到相册', icon: 'success' });
        console.log('保存成功');
      },
      fail: (err) => {
        console.error('保存失败:', err);
        wx.hideLoading();
        
        if (err.errMsg && err.errMsg.includes('auth')) {
          wx.showModal({
            title: '需要权限',
            content: '请允许访问相册以保存图片',
            confirmText: '去设置',
            success: (modalRes) => {
              if (modalRes.confirm) {
                wx.openSetting();
              }
            }
          });
        } else {
          wx.showToast({ 
            title: '保存失败: ' + (err.errMsg || '未知错误'), 
            icon: 'none',
            duration: 3000
          });
        }
      }
    });
  }
})