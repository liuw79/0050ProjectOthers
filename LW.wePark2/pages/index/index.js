const app = getApp();
// 获取实时日志管理器实例
const logger = wx.getRealtimeLogManager ? wx.getRealtimeLogManager() : null;

Page({
  data: {
    selectedFloor: null,
    parkingTime: '',
    dayText: '',
    floors: [
      { name: '1楼', value: '1F', type: 'large' },
      { name: '-1楼', value: '-1F', type: 'large' },
      { name: '-2楼', value: '-2F', type: 'large' },
      { name: '-3楼', value: '-3F', type: 'small' },
      { name: '-4楼', value: '-4F', type: 'small' },
      { name: '-5楼', value: '-5F', type: 'small' }
    ],
    // --- Camera Related State ---
    cameraEnabled: false, // User's preference via switch, persisted
    cameraAuthorized: false, // OS permission status
    cameraActive: false, // Should the <camera> component be rendered and trying to run?
    cameraErrorOccurred: false, // Did the <camera> binderror fire?
    cameraContext: null,
    photoSrc: '' 
  },
  
  // 添加分享功能
  onShareAppMessage: function() {
    let title = '停哪了停车助手'; // 恢复默认标题
    if (this.data.selectedFloor) { // 恢复动态标题逻辑
      title = '我停在了' + this.data.selectedFloor.name + '，' + this.data.parkingTime;
    }
    return {
      title: title, // 使用恢复后的 title 变量
      path: '/pages/index/index'
      // imageUrl: '/images/share.png' // Use online image URL or remove for default screenshot
    }
  },

  onLoad: function () {
    logger?.info('Index Page onLoad Start');
    const selectedFloor = app.globalData.selectedFloor;
    if (selectedFloor) {
      logger?.info('Loaded selectedFloor from globalData:', selectedFloor);
      this.setData({
        selectedFloor: selectedFloor,
        photoSrc: selectedFloor.photoInfo ? selectedFloor.photoInfo.path : ''
      });
      this.updateTimeInfo(selectedFloor.timestamp);
    }

    try {
      const cameraEnabledStored = wx.getStorageSync('cameraEnabled');
      const enabled = cameraEnabledStored === true;
      logger?.info('Loaded cameraEnabled from storage:', enabled);
      this.setData({ cameraEnabled: enabled }); 
      if (enabled) {
        this.checkCameraPermission(false);
      }
    } catch (e) {
      logger?.error('读取摄像头设置失败', e); // 恢复之前的日志和处理
      this.setData({ cameraEnabled: false });
    }

    // 恢复显式开启分享菜单的调用
    wx.showShareMenu({
      withShareTicket: true, 
      menus: ['shareAppMessage'] // 保持只开启分享给朋友
    });

    logger?.info('Index Page onLoad End');
  },
  
  onShow: function() {
      if (this.data.cameraEnabled && !this.data.cameraAuthorized) {
          logger?.info('Page onShow: Re-checking camera permission.');
          this.checkCameraPermission(false); 
      }
  },

  // 切换摄像头开关
  toggleCamera: function(e) {
    const desiredState = e.detail.value;
    logger?.info(`切换相机开关: ${desiredState}`);
    wx.setStorageSync('cameraEnabled', desiredState);

    if (desiredState) {
      this.setData({ cameraEnabled: true });
      this.checkCameraPermission(true); 
    } else {
      logger?.info('禁用相机组件');
      this.setData({ 
          cameraEnabled: false, 
          cameraActive: false, 
          cameraErrorOccurred: false, 
          cameraContext: null 
      });
    }
  },
  
  // 检查相机权限
  checkCameraPermission: function(requestIfNeeded = false) {
      logger?.info(`检查相机权限 (请求: ${requestIfNeeded})...`);
      wx.getSetting({
          success: (res) => {
              if (res.authSetting['scope.camera']) {
                  logger?.info('相机权限：已授权');
                  if (!this.data.cameraAuthorized) {
                    this.setData({ cameraAuthorized: true });
                  }
                  if (this.data.cameraEnabled) {
                      this.activateCameraComponent();
                  }
              } else {
                  logger?.warn('相机权限：未授权');
                  this.setData({ cameraAuthorized: false, cameraActive: false, cameraContext: null });
                  if (requestIfNeeded) {
                      this.requestCameraPermission();
                  } else {
                      if (this.data.cameraEnabled) {
                          logger?.warn('权限未授予，但开关状态为开，自动关闭开关。');
                          this.setData({ cameraEnabled: false });
                          wx.setStorageSync('cameraEnabled', false);
                      }
                  }
              }
          },
          fail: (err) => {
              logger?.error('wx.getSetting 失败:', err);
              this.setData({ cameraAuthorized: false, cameraActive: false, cameraContext: null });
          }
      });
  },
  
  // 拍照功能
  takePhoto: function() {
    if (!this.data.cameraContext) {
      this.setData({
        cameraContext: wx.createCameraContext()
      });
    }
    
    this.data.cameraContext.takePhoto({
      quality: 'high',
      success: (res) => {
        this.setData({
          photoSrc: res.tempImagePath
        });
        
        // 保存照片到本地
        this.savePhotoToLocal(res.tempImagePath);
      },
      fail: (error) => {
        console.error('拍照失败:', error);
        wx.showToast({
          title: '拍照失败',
          icon: 'none'
        });
      }
    });
  },
  
  // 保存照片到本地
  savePhotoToLocal: function(photoPath) {
    const photoInfo = {
      path: photoPath,
      timestamp: new Date().getTime()
    };
    
    // 如果已有选中楼层，更新相关信息
    if (this.data.selectedFloor) {
      const updatedFloor = {
        ...this.data.selectedFloor,
        photoInfo: photoInfo
      };
      
      this.setData({
        selectedFloor: updatedFloor
      });
      
      // 更新全局数据和本地存储
      app.globalData.selectedFloor = updatedFloor;
      wx.setStorageSync('selectedFloor', updatedFloor);
      
      // 更新停车记录
      const parkingRecords = app.globalData.parkingRecords || [];
      const index = parkingRecords.findIndex(item => 
        item.timestamp === this.data.selectedFloor.timestamp);
      
      if (index !== -1) {
        parkingRecords[index] = updatedFloor;
        app.globalData.parkingRecords = parkingRecords;
        wx.setStorageSync('parkingRecords', parkingRecords);
      }
    }
  },

  // 选择楼层
  selectFloor: function (e) {
    const index = e.currentTarget.dataset.index;
    const floor = this.data.floors[index];
    const timestamp = new Date().getTime();
    const recordId = `record_${timestamp}_${Math.random().toString(36).substr(2, 5)}`;

    const newRecord = {
      ...floor,
      timestamp: timestamp,
      recordId: recordId,
      formattedTime: this.formatDateTime(timestamp),
      photoInfo: null 
    };
    logger?.info('选择楼层 (ID: ' + recordId + '): ', newRecord.name);

    this.setData({
      selectedFloor: newRecord,
      photoSrc: '' 
    });
    this.updateTimeInfo(timestamp);

    // 先保存基础记录
    this.saveRecord(newRecord);
    logger?.info('基础记录已保存 (ID: ' + recordId + ')');
    
    // 尝试自动拍照
    if (this.data.cameraActive && !this.data.cameraErrorOccurred && this.data.cameraContext) {
      logger?.info('尝试自动拍照 (记录ID: ' + recordId + ')');
      this.takePhotoAndUpdateRecord(recordId, timestamp);
    } else {
       let reason = "";
       if (!this.data.cameraActive) reason = "相机未激活";
       else if (this.data.cameraErrorOccurred) reason = "相机错误";
       else if (!this.data.cameraContext) reason = "相机实例丢失";
       else reason = "未知原因";
       logger?.warn('未执行自动拍照，原因: ' + reason + '. 当前相机状态:', {
           active: this.data.cameraActive,
           error: this.data.cameraErrorOccurred,
           context: !!this.data.cameraContext
       });
       // 可选：给用户一个温和提示照片未拍
       // wx.showToast({ title: '照片未拍摄', icon: 'none' });
    }
  },
  
  // Take photo and link it to an existing record
  takePhotoAndUpdateRecord: function(recordId, timestamp) {
    logger?.info(`执行拍照并更新记录 (ID: ${recordId})...`);
    if (!this.data.cameraContext) { 
       logger?.error('拍照前检查：cameraContext 不存在!');
       wx.showToast({ title: '拍照功能异常', icon: 'none' });
       return;
    }
    
    this.data.cameraContext.takePhoto({
      quality: 'high',
      success: (res) => {
        const photoPath = res.tempImagePath;
        logger?.info('拍照 API 成功，照片路径:', photoPath);
        this.setData({ photoSrc: photoPath });

        const photoInfo = {
          path: photoPath,
          timestamp: timestamp 
        };

        let parkingRecords = app.globalData.parkingRecords || [];
        let recordUpdated = false;
        let updatedRecord = null;
        parkingRecords = parkingRecords.map(record => {
          if (record.recordId === recordId) {
            recordUpdated = true;
            updatedRecord = { ...record, photoInfo: photoInfo };
            return updatedRecord;
          }
          return record;
        });

        if (recordUpdated) {
          logger?.info('记录已找到，准备更新存储...');
          app.globalData.parkingRecords = parkingRecords;
          wx.setStorageSync('parkingRecords', parkingRecords);

          if (this.data.selectedFloor && this.data.selectedFloor.recordId === recordId) {
            this.setData({ selectedFloor: updatedRecord });
             logger?.info('页面 selectedFloor 数据已同步更新照片信息');
          }
           wx.showToast({ title: '照片已关联保存', icon: 'success' });
        } else {
          logger?.error('严重错误：未能找到记录ID [' + recordId + '] 来更新照片信息。');
           wx.showToast({ title: '记录关联照片失败', icon: 'error' });
        }
      },
      fail: (error) => {
        logger?.error('拍照 API 失败:', error);
        if (error.errMsg && error.errMsg.includes('cancel')) {
            wx.showToast({ title: '拍照取消', icon: 'none' });
        } else {
            wx.showToast({ title: '拍照失败', icon: 'none' });
        }
      }
    });
  },

  // Unified record saving function
  saveRecord: function(recordToSave) {
    if (!recordToSave || !recordToSave.recordId) {
        console.error("无效记录，无法保存:", recordToSave);
        return;
    }
    console.log(`保存/更新记录到存储 (ID: ${recordToSave.recordId})`);
    app.globalData.selectedFloor = recordToSave;
    wx.setStorageSync('selectedFloor', recordToSave);

    let parkingRecords = app.globalData.parkingRecords || [];
    const existingIndex = parkingRecords.findIndex(item => item.recordId === recordToSave.recordId);

    if (existingIndex !== -1) {
      parkingRecords[existingIndex] = recordToSave;
      console.log(`记录 [${recordToSave.recordId}] 在历史列表中已更新.`);
    } else {
      parkingRecords.unshift(recordToSave);
      console.log(`记录 [${recordToSave.recordId}] 已添加到历史列表.`);
    }

    app.globalData.parkingRecords = parkingRecords;
    wx.setStorageSync('parkingRecords', parkingRecords);
  },

  // 更新时间信息显示
  updateTimeInfo: function(timestamp) {
    if (!timestamp) return;
    
    const formattedTime = this.formatDateTime(timestamp);
    const dayText = this.getDayText(timestamp);
    
    this.setData({
      parkingTime: formattedTime,
      dayText: dayText
    });
  },
  
  // 格式化日期时间
  formatDateTime: function(timestamp) {
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const hour = date.getHours().toString().padStart(2, '0');
    const minute = date.getMinutes().toString().padStart(2, '0');
    
    return `${year}-${month}-${day} ${hour}:${minute}`;
  },
  
  // 获取"今天"、"昨天"、"前天"的文本
  getDayText: function(timestamp) {
    const now = new Date();
    const targetDate = new Date(timestamp);
    
    // 重置时间部分，只比较日期
    now.setHours(0, 0, 0, 0);
    targetDate.setHours(0, 0, 0, 0);
    
    // 计算相差的天数
    const diffDays = Math.floor((now - targetDate) / (24 * 60 * 60 * 1000));
    
    if (diffDays === 0) {
      return '（今天）';
    } else if (diffDays === 1) {
      return '（昨天）';
    } else if (diffDays === 2) {
      return '（前天）';
    } else {
      return '';
    }
  },

  // --- Camera Activation and Permission --- 
  requestCameraPermission: function() {
      logger?.info('请求相机权限...');
      wx.authorize({
          scope: 'scope.camera',
          success: () => {
              logger?.info('用户同意授权');
              this.setData({ cameraAuthorized: true });
              if (this.data.cameraEnabled) {
                  this.activateCameraComponent(); 
              }
          },
          fail: () => {
              logger?.warn('用户拒绝授权');
              this.setData({ cameraEnabled: false, cameraAuthorized: false, cameraActive: false, cameraContext: null });
              wx.setStorageSync('cameraEnabled', false);
              wx.showModal({
                  title: '相机权限请求',
                  content: '您需要授权相机权限才能使用拍照功能。是否前往设置页面开启权限？',
                  confirmText: '去设置',
                  cancelText: '取消',
                  success: (res) => {
                      if (res.confirm) {
                          wx.openSetting(); 
                      }
                  }
              });
          }
      });
  },

  activateCameraComponent: function() {
      if (!this.data.cameraEnabled || !this.data.cameraAuthorized) {
          logger?.info('activateCameraComponent called but conditions not met.');
          this.setData({ cameraActive: false, cameraContext: null }); 
          return;
      }
      logger?.info('激活相机组件...');
      this.setData({ 
          cameraActive: true,       
          cameraErrorOccurred: false, 
          cameraContext: null       
      }, () => {
          wx.nextTick(() => {
              try {
                  logger?.info('尝试创建 camera context...');
                  const ctx = wx.createCameraContext();
                  if (ctx) {
                      logger?.info('wx.createCameraContext 成功');
                      this.setData({ cameraContext: ctx });
                  } else {
                      logger?.error('wx.createCameraContext 返回了 null/undefined');
                      throw new Error('createCameraContext returned invalid context');
                  }
              } catch (error) {
                  logger?.error("创建 camera context 时出错:", error);
                  this.handleCameraError({ detail: { errMsg: 'createContext failed: ' + error.message } });
              }
          });
      });
  },

  // --- Camera Component Event Handlers --- 
  handleCameraError: function(e) {
    // **** 这是最关键的日志！****
    logger?.error('相机组件 binderror 事件触发:', e.detail);
    const errMsg = e.detail && e.detail.errMsg ? e.detail.errMsg : '未知相机错误';
    this.setData({ 
      cameraErrorOccurred: true, 
      cameraActive: false, 
      cameraContext: null 
    });
    wx.showToast({ title: `相机错误: ${errMsg}`, icon: 'none', duration: 3000 });
  },

  // --- Manual Photo Taking --- 
  // manualTakePhoto: function() { ... }
  
  // Preview the currently displayed photo (either just taken or loaded)
  previewCurrentImage: function() {
    if (this.data.photoSrc) {
      wx.previewImage({
        urls: [this.data.photoSrc]
      });
    }
  },
}) 