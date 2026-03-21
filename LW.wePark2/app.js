App({
  globalData: {
    selectedFloor: null,
    parkingRecords: []
  },
  onLaunch: function() {
    // 加载本地存储的数据
    const selectedFloor = wx.getStorageSync('selectedFloor');
    const parkingRecords = wx.getStorageSync('parkingRecords') || [];
    
    this.globalData.selectedFloor = selectedFloor;
    this.globalData.parkingRecords = parkingRecords;
  }
}) 