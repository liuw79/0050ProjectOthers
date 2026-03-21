// history.js
const app = getApp();

Page({
  data: {
    parkingRecords: []
  },

  // 添加分享功能
  onShareAppMessage: function() {
    let title = '我的停车记录';
    if (this.data.parkingRecords && this.data.parkingRecords.length > 0) {
      const latestRecord = this.data.parkingRecords[0];
      title = '我最近停在了' + latestRecord.name + '，' + latestRecord.formattedTime;
    }
    return {
      title: title,
      path: '/pages/index/index',
      imageUrl: '/images/share.png'
    }
  },

  onShow: function () {
    // 每次页面显示时更新记录
    this.loadParkingRecords();
  },
  
  // 加载停车记录
  loadParkingRecords: function() {
    const parkingRecords = app.globalData.parkingRecords || [];
    
    // 更新每条记录的dayText（今天/昨天/前天）
    const updatedRecords = parkingRecords.map(record => {
      return {
        ...record,
        dayText: this.getDayText(record.timestamp)
      };
    });
    
    this.setData({
      parkingRecords: updatedRecords
    });
  },
  
  // 查看照片
  viewPhoto: function(e) {
    const photoPath = e.currentTarget.dataset.photo;
    if (!photoPath) {
      wx.showToast({
        title: '照片不存在',
        icon: 'none'
      });
      return;
    }
    
    wx.previewImage({
      urls: [photoPath],
      current: photoPath
    });
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
  
  // 导出停车记录
  exportRecords: function() {
    const { parkingRecords } = this.data;
    
    if (parkingRecords.length === 0) {
      wx.showToast({
        title: '暂无记录可导出',
        icon: 'none'
      });
      return;
    }
    
    // 生成CSV格式的导出数据
    let csvContent = '停车楼层,停车时间\n';
    parkingRecords.forEach(record => {
      csvContent += `${record.name},${record.formattedTime}\n`;
    });
    
    // 将导出数据保存到剪贴板
    wx.setClipboardData({
      data: csvContent,
      success: () => {
        wx.showModal({
          title: '导出成功',
          content: '停车记录已复制到剪贴板，您可以粘贴到文本编辑器或表格软件中保存。',
          showCancel: false
        });
      },
      fail: () => {
        wx.showToast({
          title: '导出失败',
          icon: 'none'
        });
      }
    });
    
    // 记录到导出日志
    console.log('导出记录：', csvContent);
  },
  
  // 清空历史记录
  clearHistory: function() {
    wx.showModal({
      title: '提示',
      content: '确定要清空所有停车记录吗？',
      success: (res) => {
        if (res.confirm) {
          // 清空记录
          app.globalData.parkingRecords = [];
          wx.setStorageSync('parkingRecords', []);
          this.setData({
            parkingRecords: []
          });
          wx.showToast({
            title: '已清空',
            icon: 'success'
          });
        }
      }
    });
  }
}) 