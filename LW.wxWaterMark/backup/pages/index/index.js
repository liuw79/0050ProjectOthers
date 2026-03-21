/*
【开发协作备忘】
1. 功能完成/满意/告一段落时，主动建议 Git 提交。
2. 始终使用中文沟通。
3. 日志优先按钮复制，否则手动管理（删除旧日志，读取新日志）。
4. 反复出错的问题添加注释说明。
5. 复杂代码问题，提醒用户提供示例代码供学习。
6. 疑难或反复修改无效问题，提醒用户寻求外部帮助并同步结果。
*/

// pages/index/index.js

const PLACEHOLDER_USAGE = '____';
const WATERMARK_PREFIX = '仅供';
const WATERMARK_SUFFIX = '使用不得用于其他用途，有效期至';

// Helper function to format date as YY/MM/DD
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
    initialWatermarkText: '',    // 初始水印文字（用于比较）
    fullWatermarkText: '',       // 当前水印文字
    imageMaxHeightPx: 300        // 图片预览最大高度（像素）
  },

  /**
   * 选择图片
   */
  chooseImage: function() {
    // 优先使用wx.chooseMedia，降级到wx.chooseImage提高兼容性
    if (wx.chooseMedia) {
      wx.chooseMedia({
        count: 1,
        mediaType: ['image'],
        sourceType: ['album', 'camera'],
        success: (res) => {
          this.setData({
            tempFilePath: res.tempFiles[0].tempFilePath
          });
        },
        fail: (err) => {
          if (err.errMsg !== "chooseMedia:fail cancel") {
            // 降级使用旧API
            this.chooseImageFallback();
          }
        }
      });
    } else {
      // 直接使用旧API
      this.chooseImageFallback();
    }
  },

  // 兼容性降级方案
  chooseImageFallback: function() {
    wx.chooseImage({
      count: 1,
      sourceType: ['album', 'camera'],
      success: (res) => {
        this.setData({
          tempFilePath: res.tempFilePaths[0]
        });
      },
      fail: (err) => {
        if (err.errMsg !== "chooseImage:fail cancel") {
          wx.showToast({ title: '图片选择失败', icon: 'none' });
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
   * 生命周期函数--监听页面加载
   */
  onLoad: function() {
    // 计算图片预览区域的最大高度
    let imageMaxHeight = 300; // 默认值
    try {
        // 使用wx.getSystemInfo替代wx.getWindowInfo提高兼容性
        wx.getSystemInfo({
          success: (res) => {
            if (res.windowHeight) {
              imageMaxHeight = res.windowHeight * 0.4;
              this.setData({
                imageMaxHeightPx: imageMaxHeight
              });
            }
          },
          fail: (err) => {
            console.error("获取系统信息失败:", err);
            // 使用默认值
          }
        });
    } catch (e) {
        console.error("获取窗口信息失败:", e);
        // Fallback is handled by the default value
    }

    // 生成默认水印文本
    const today = new Date();
    const expiry = new Date(new Date().setMonth(today.getMonth() + 1));
    const expiryDateString = formatDate(expiry);
    const usage = wx.getStorageSync('lastUsage') || PLACEHOLDER_USAGE;
    const defaultText = `${WATERMARK_PREFIX}${usage}${WATERMARK_SUFFIX}${expiryDateString}`;

    this.setData({
      imageMaxHeightPx: imageMaxHeight,
      initialWatermarkText: defaultText, // Keep initial text for comparison
      fullWatermarkText: defaultText
    });
  },

  /**
   * 生命周期函数--监听页面卸载
   */
  onUnload: function() {
      // 保存用户输入的用途
      const currentText = this.data.fullWatermarkText;
      
      if (currentText.startsWith(WATERMARK_PREFIX) && currentText.includes(WATERMARK_SUFFIX)) {
          const startIndex = WATERMARK_PREFIX.length;
          const endIndex = currentText.indexOf(WATERMARK_SUFFIX);
          
          if (startIndex < endIndex) {
              const extractedUsage = currentText.substring(startIndex, endIndex);
              if (extractedUsage !== PLACEHOLDER_USAGE) {
                  wx.setStorageSync('lastUsage', extractedUsage);
              } else {
                  wx.removeStorageSync('lastUsage');
              }
          } else {
              wx.removeStorageSync('lastUsage');
          }
      } else {
          wx.removeStorageSync('lastUsage');
      }
  },

  /**
   * 生成水印图片
   */
  generateWatermarkedImage: function() {
    // 检查是否上传了图片
    if (!this.data.tempFilePath) {
      wx.showToast({ title: '请先上传图片', icon: 'none' });
      return;
    }

    // 检查水印文字是否包含占位符
    if (this.data.fullWatermarkText.includes(PLACEHOLDER_USAGE)) {
      wx.showToast({ title: '请填写____处的水印用途', icon: 'none' });
      return;
    }
    
    // 检查水印文字是否为空
    if (!this.data.fullWatermarkText.trim()) {
      wx.showToast({ title: '水印文字不能为空', icon: 'none' });
      return;
    }

    // 调试信息
    console.log('开始生成水印图片');
    console.log('图片路径:', this.data.tempFilePath);
    console.log('水印文字:', this.data.fullWatermarkText);
    console.log('系统信息:', wx.getSystemInfoSync());

    // 权限预检查
    this.checkPermissions(() => {
      wx.showLoading({ title: '生成中...' });
      this.processImage();
    });
  },

  // 权限检查
  checkPermissions: function(callback) {
    wx.getSetting({
      success: (res) => {
        if (res.authSetting['scope.writePhotosAlbum'] === false) {
          // 用户曾经拒绝过权限
          wx.showModal({
            title: '权限提示',
            content: '需要获取相册写入权限才能保存图片，请在设置中开启',
            confirmText: '去设置',
            success: (modalRes) => {
              if (modalRes.confirm) {
                wx.openSetting({
                  success: (settingRes) => {
                    if (settingRes.authSetting['scope.writePhotosAlbum']) {
                      callback();
                    } else {
                      wx.showToast({ title: '未获得权限，无法保存', icon: 'none' });
                    }
                  }
                });
              }
            }
          });
        } else {
          // 权限未定义或已授权
          callback();
        }
      },
      fail: () => {
        // 获取设置失败，直接继续
        callback();
      }
    });
  },

  // 处理图片
  processImage: function() {

    // 获取图片信息
    wx.getImageInfo({
      src: this.data.tempFilePath,
      success: (res) => {
        const imgWidth = res.width;
        const imgHeight = res.height;

        // 真机环境直接使用旧版Canvas，避免兼容性问题
        console.log('真机优化：直接使用旧版Canvas');
        this.tryCanvasLegacy(imgWidth, imgHeight);
      },
      fail: (err) => {
        wx.hideLoading();
        wx.showToast({ title: '获取图片信息失败', icon: 'none' });
        console.error('获取图片信息失败:', err);
      }
    });
  },

  // 尝试使用Canvas 2D
  tryCanvas2D: function(imgWidth, imgHeight, callback) {
    try {
      // 延迟执行，确保Canvas完全渲染
      setTimeout(() => {
        const query = wx.createSelectorQuery().in(this);
        query.select('#watermarkCanvas')
          .fields({ node: true, size: true })
          .exec((execRes) => {
            if (!execRes || !execRes[0] || !execRes[0].node) {
              console.log('Canvas 2D不可用，降级到旧版Canvas');
              callback(false);
              return;
            }

            const canvas = execRes[0].node;
            const ctx = canvas.getContext('2d');

            if (!ctx) {
              console.log('Canvas 2D上下文获取失败，降级到旧版Canvas');
              callback(false);
              return;
            }

            // 设置canvas尺寸
            canvas.width = imgWidth;
            canvas.height = imgHeight;

            // 直接调用绘制水印方法
            this.drawWatermark(ctx, imgWidth, imgHeight, () => {
              // 延迟一下确保绘制完成
              setTimeout(() => {
                wx.canvasToTempFilePath({
                  canvas: canvas,
                  quality: 0.9,
                  fileType: 'jpg',
                  success: (tempRes) => {
                    this.saveToAlbum(tempRes.tempFilePath);
                  },
                  fail: (err) => {
                    wx.hideLoading();
                    wx.showToast({ title: '生成图片失败', icon: 'none' });
                    console.error('Canvas 2D生成图片失败:', err);
                    callback(false);
                  }
                });
              }, 100);
            });
          });
      }, 100);
    } catch (e) {
      console.error('Canvas 2D异常:', e);
      callback(false);
    }
  },

  // 使用旧版Canvas（真机优化版）
  tryCanvasLegacy: function(imgWidth, imgHeight) {
    try {
      console.log('使用旧版Canvas处理图片, 尺寸:', imgWidth, 'x', imgHeight);
      const ctx = wx.createCanvasContext('watermarkCanvas', this);
      
      if (!ctx) {
        wx.hideLoading();
        wx.showToast({ title: 'Canvas初始化失败', icon: 'none' });
        return;
      }
      
      // 绘制图片
      ctx.drawImage(this.data.tempFilePath, 0, 0, imgWidth, imgHeight);
      
      // 简化版水印绘制，避免复杂操作
      const fontSize = Math.max(16, Math.min(imgWidth, imgHeight) / 15);
      const watermarkText = this.data.fullWatermarkText;
      
      console.log('设置水印文字:', watermarkText, '字体大小:', fontSize);
      
      ctx.setFontSize(fontSize);
      ctx.setFillStyle('rgba(0, 0, 0, 0.3)');
      ctx.setTextAlign('center');
      
      // 简单居中水印，不旋转
      const centerX = imgWidth / 2;
      const centerY = imgHeight / 2;
      
      ctx.fillText(watermarkText, centerX, centerY - fontSize);
      ctx.fillText(watermarkText, centerX, centerY);
      ctx.fillText(watermarkText, centerX, centerY + fontSize);
      
      console.log('开始绘制Canvas');
      ctx.draw(false, () => {
        console.log('Canvas绘制完成，开始导出');
        // 延迟确保draw完成
        setTimeout(() => {
          wx.canvasToTempFilePath({
            canvasId: 'watermarkCanvas',
            quality: 0.8,
            fileType: 'png',
            success: (tempRes) => {
              console.log('Canvas导出成功:', tempRes.tempFilePath);
              this.saveToAlbum(tempRes.tempFilePath);
            },
            fail: (err) => {
              console.error('Canvas导出失败:', err);
              wx.hideLoading();
              wx.showToast({ title: '生成图片失败: ' + (err.errMsg || '未知错误'), icon: 'none' });
            }
          }, this);
        }, 500);
      });
    } catch (e) {
      wx.hideLoading();
      wx.showToast({ title: 'Canvas处理异常', icon: 'none' });
      console.error('旧版Canvas异常:', e);
    }
  },

  // 旧版Canvas重试
  retryLegacyCanvas: function(imgWidth, imgHeight) {
    console.log('尝试重新使用旧版Canvas');
    try {
      const ctx = wx.createCanvasContext('watermarkCanvas', this);
      
      // 简化绘制，只绘制基本水印
      ctx.drawImage(this.data.tempFilePath, 0, 0, imgWidth, imgHeight);
      
      // 简化水印绘制
      const fontSize = Math.max(16, Math.min(imgWidth, imgHeight) / 15);
      ctx.setFontSize(fontSize);
      ctx.setFillStyle('rgba(0, 0, 0, 0.3)');
      ctx.setTextAlign('center');
      
      const watermarkText = this.data.fullWatermarkText;
      const centerX = imgWidth / 2;
      const centerY = imgHeight / 2;
      
      ctx.fillText(watermarkText, centerX, centerY);
      
      ctx.draw(false, () => {
        setTimeout(() => {
          wx.canvasToTempFilePath({
            canvasId: 'watermarkCanvas',
            success: (tempRes) => {
              console.log('重试成功');
              this.saveToAlbum(tempRes.tempFilePath);
            },
            fail: (err) => {
              wx.hideLoading();
              wx.showToast({ title: '图片处理失败，请重试', icon: 'none' });
              console.error('重试也失败:', err);
            }
          }, this);
        }, 300);
      });
    } catch (e) {
      wx.hideLoading();
      wx.showToast({ title: '处理失败', icon: 'none' });
      console.error('重试异常:', e);
    }
  },

  // Canvas 2D绘制水印
  drawWatermark: function(ctx, imgWidth, imgHeight, callback) {
    // 注意：Canvas 2D中需要使用image对象，不能直接使用路径
    try {
      const image = ctx.canvas.createImage();
      
      // 设置超时机制
      const timeoutId = setTimeout(() => {
        console.error('Canvas 2D图片加载超时');
        callback();
      }, 5000);
      
      image.onload = () => {
        clearTimeout(timeoutId);
        try {
          ctx.clearRect(0, 0, imgWidth, imgHeight);
          ctx.drawImage(image, 0, 0, imgWidth, imgHeight);

          const fontSize = Math.max(14, Math.min(imgWidth, imgHeight) / 20);
          ctx.font = `${fontSize}px sans-serif`;
          ctx.fillStyle = 'rgba(0, 0, 0, 0.2)';
          ctx.textAlign = 'center';
          ctx.textBaseline = 'middle';

          ctx.save();
          ctx.translate(imgWidth / 2, imgHeight / 2);
          ctx.rotate(-30 * Math.PI / 180);

          const watermarkText = this.data.fullWatermarkText;
          const offset = Math.sqrt(imgWidth*imgWidth + imgHeight*imgHeight) * 0.25;

          ctx.fillText(watermarkText, 0, 0);
          ctx.fillText(watermarkText, -offset, -offset);
          ctx.fillText(watermarkText, offset, offset);

          ctx.restore();
          callback();
        } catch (drawError) {
          clearTimeout(timeoutId);
          console.error('Canvas 2D绘制失败:', drawError);
          callback();
        }
      };

      image.onerror = (err) => {
        clearTimeout(timeoutId);
        console.error('Canvas 2D图片加载失败:', err);
        callback();
      };

      image.src = this.data.tempFilePath;
    } catch (e) {
      console.error('Canvas 2D drawWatermark异常:', e);
      callback();
    }
  },

  // 旧版Canvas绘制水印
  drawWatermarkLegacy: function(ctx, imgWidth, imgHeight, callback) {
    const fontSize = Math.max(14, Math.min(imgWidth, imgHeight) / 20);
    ctx.setFontSize(fontSize);
    ctx.setFillStyle('rgba(0, 0, 0, 0.2)');
    ctx.setTextAlign('center');
    ctx.setTextBaseline('middle');

    ctx.save();
    ctx.translate(imgWidth / 2, imgHeight / 2);
    ctx.rotate(-30 * Math.PI / 180);

    const watermarkText = this.data.fullWatermarkText;
    const offset = Math.sqrt(imgWidth*imgWidth + imgHeight*imgHeight) * 0.25;

    ctx.fillText(watermarkText, 0, 0);
    ctx.fillText(watermarkText, -offset, -offset);
    ctx.fillText(watermarkText, offset, offset);

    ctx.restore();
    callback();
  },

  // 保存到相册
  saveToAlbum: function(filePath) {
    wx.saveImageToPhotosAlbum({
      filePath: filePath,
      success: () => {
        wx.hideLoading();
        wx.showToast({ title: '已保存到相册', icon: 'success' });
      },
      fail: (err) => {
        wx.hideLoading();
        if (err.errMsg && (err.errMsg.includes('auth deny') || err.errMsg.includes('auth denied'))) {
          wx.showModal({
            title: '授权提示',
            content: '需要您授权保存图片到相册',
            showCancel: false,
            success: (modalRes) => {
              if (modalRes.confirm) {
                wx.openSetting({
                  success(settingRes) {
                    if (settingRes.authSetting['scope.writePhotosAlbum']) {
                      wx.showToast({ title: '授权成功，请重试', icon: 'none' });
                    } else {
                      wx.showToast({ title: '授权失败', icon: 'none' });
                    }
                  }
                });
              }
            }
          });
        } else {
          wx.showToast({ title: '保存失败', icon: 'none' });
          console.error('保存失败:', err);
        }
      }
    });
  }
})