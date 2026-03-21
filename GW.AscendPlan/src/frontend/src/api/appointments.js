import { api } from './request'

export const appointmentsApi = {
  // 客户管理
  customers: {
    // 获取客户列表
    list: (params = {}) => {
      return api.get('/appointments/customers/', params)
    },

    // 获取客户详情
    get: (id) => {
      return api.get(`/appointments/customers/${id}/`)
    },

    // 创建客户
    create: (customerData) => {
      return api.post('/appointments/customers/', customerData)
    },

    // 更新客户
    update: (id, customerData) => {
      return api.put(`/appointments/customers/${id}/`, customerData)
    },

    // 部分更新客户
    patch: (id, customerData) => {
      return api.patch(`/appointments/customers/${id}/`, customerData)
    },

    // 删除客户
    delete: (id) => {
      return api.delete(`/appointments/customers/${id}/`)
    }
  },

  // 预约管理
  appointments: {
    // 获取预约列表
    list: (params = {}) => {
      return api.get('/appointments/appointments/', params)
    },

    // 获取预约详情
    get: (id) => {
      return api.get(`/appointments/appointments/${id}/`)
    },

    // 创建预约
    create: (appointmentData) => {
      return api.post('/appointments/appointments/', appointmentData)
    },

    // 更新预约
    update: (id, appointmentData) => {
      return api.put(`/appointments/appointments/${id}/`, appointmentData)
    },

    // 部分更新预约
    patch: (id, appointmentData) => {
      return api.patch(`/appointments/appointments/${id}/`, appointmentData)
    },

    // 删除预约
    delete: (id) => {
      return api.delete(`/appointments/appointments/${id}/`)
    },

    // 获取今日预约
    today: () => {
      return api.get('/appointments/appointments/today/')
    },

    // 获取即将到来的预约
    upcoming: () => {
      return api.get('/appointments/appointments/upcoming/')
    },

    // 获取可用时间段
    availableSlots: (date) => {
      return api.get('/appointments/appointments/available_slots/', { date })
    },

    // 确认预约
    confirm: (id) => {
      return api.post(`/appointments/appointments/${id}/confirm/`)
    },

    // 取消预约
    cancel: (id, reason = '') => {
      return api.post(`/appointments/appointments/${id}/cancel/`, { reason })
    },

    // 完成预约
    complete: (id, notes = '') => {
      return api.post(`/appointments/appointments/${id}/complete/`, { notes })
    },

    // 重新安排预约
    reschedule: (id, newDateTime) => {
      return api.post(`/appointments/appointments/${id}/reschedule/`, {
        new_date_time: newDateTime
      })
    }
  },

  // 预约记录管理
  notes: {
    // 获取预约记录列表
    list: (params = {}) => {
      return api.get('/appointments/appointment-notes/', params)
    },

    // 获取预约记录详情
    get: (id) => {
      return api.get(`/appointments/appointment-notes/${id}/`)
    },

    // 创建预约记录
    create: (noteData) => {
      return api.post('/appointments/appointment-notes/', noteData)
    },

    // 更新预约记录
    update: (id, noteData) => {
      return api.put(`/appointments/appointment-notes/${id}/`, noteData)
    },

    // 部分更新预约记录
    patch: (id, noteData) => {
      return api.patch(`/appointments/appointment-notes/${id}/`, noteData)
    },

    // 删除预约记录
    delete: (id) => {
      return api.delete(`/appointments/appointment-notes/${id}/`)
    },

    // 根据预约ID获取记录
    getByAppointment: (appointmentId) => {
      return api.get('/appointments/appointment-notes/', {
        appointment: appointmentId
      })
    }
  },

  // 统计信息
  statistics: {
    // 获取预约统计
    appointments: (params = {}) => {
      return api.get('/appointments/appointments/statistics/', params)
    },

    // 获取客户统计
    customers: (params = {}) => {
      return api.get('/appointments/customers/statistics/', params)
    }
  }
}