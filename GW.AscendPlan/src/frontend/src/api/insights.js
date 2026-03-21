import { api } from './request'

export const insightsApi = {
  // 访谈文稿管理
  transcripts: {
    // 获取文稿列表
    list: (params = {}) => {
      return api.get('/insights/transcripts/', params)
    },

    // 获取文稿详情
    get: (id) => {
      return api.get(`/insights/transcripts/${id}/`)
    },

    // 创建文稿
    create: (transcriptData) => {
      return api.post('/insights/transcripts/', transcriptData)
    },

    // 更新文稿
    update: (id, transcriptData) => {
      return api.put(`/insights/transcripts/${id}/`, transcriptData)
    },

    // 部分更新文稿
    patch: (id, transcriptData) => {
      return api.patch(`/insights/transcripts/${id}/`, transcriptData)
    },

    // 删除文稿
    delete: (id) => {
      return api.delete(`/insights/transcripts/${id}/`)
    },

    // 分析文稿
    analyze: (id, templateId = null) => {
      return api.post(`/insights/transcripts/${id}/analyze/`, {
        template_id: templateId
      })
    },

    // 获取分析结果
    getAnalysisResult: (id) => {
      return api.get(`/insights/transcripts/${id}/analysis_result/`)
    }
  },

  // 洞察分析管理
  analysis: {
    // 获取分析列表
    list: (params = {}) => {
      return api.get('/insights/analysis/', params)
    },

    // 获取分析详情
    get: (id) => {
      return api.get(`/insights/analysis/${id}/`)
    },

    // 更新分析
    update: (id, analysisData) => {
      return api.put(`/insights/analysis/${id}/`, analysisData)
    },

    // 部分更新分析
    patch: (id, analysisData) => {
      return api.patch(`/insights/analysis/${id}/`, analysisData)
    },

    // 删除分析
    delete: (id) => {
      return api.delete(`/insights/analysis/${id}/`)
    },

    // 审核分析
    review: (id, reviewData) => {
      return api.post(`/insights/analysis/${id}/review/`, reviewData)
    },

    // 获取分析统计
    statistics: () => {
      return api.get('/insights/analysis/statistics/')
    }
  },

  // 分析模板管理
  templates: {
    // 获取模板列表
    list: (params = {}) => {
      return api.get('/insights/templates/', params)
    },

    // 获取模板详情
    get: (id) => {
      return api.get(`/insights/templates/${id}/`)
    },

    // 创建模板
    create: (templateData) => {
      return api.post('/insights/templates/', templateData)
    },

    // 更新模板
    update: (id, templateData) => {
      return api.put(`/insights/templates/${id}/`, templateData)
    },

    // 部分更新模板
    patch: (id, templateData) => {
      return api.patch(`/insights/templates/${id}/`, templateData)
    },

    // 删除模板
    delete: (id) => {
      return api.delete(`/insights/templates/${id}/`)
    },

    // 激活模板
    activate: (id) => {
      return api.post(`/insights/templates/${id}/activate/`)
    },

    // 停用模板
    deactivate: (id) => {
      return api.post(`/insights/templates/${id}/deactivate/`)
    }
  },

  // 分析日志管理
  logs: {
    // 获取日志列表
    list: (params = {}) => {
      return api.get('/insights/logs/', params)
    },

    // 获取日志详情
    get: (id) => {
      return api.get(`/insights/logs/${id}/`)
    },

    // 获取日志统计
    statistics: () => {
      return api.get('/insights/logs/statistics/')
    }
  },

  // 客户洞察管理
  customerInsights: {
    // 获取客户洞察摘要列表
    list: (params = {}) => {
      return api.get('/insights/customer-insights/', params)
    },

    // 获取特定客户的详细洞察报告
    get: (customerId) => {
      return api.get(`/insights/customer-insights/${customerId}/`)
    },

    // 生成客户洞察报告
    generateReport: (customerId, options = {}) => {
      return api.post(`/insights/customer-insights/${customerId}/generate/`, options)
    },

    // 导出客户洞察报告
    exportReport: (customerId, format = 'pdf') => {
      return api.download(
        `/insights/customer-insights/${customerId}/export/`,
        `customer_insights_${customerId}.${format}`,
        { params: { format } }
      )
    }
  },

  // 批量操作
  batch: {
    // 批量分析文稿
    analyzeTranscripts: (transcriptIds, templateId = null) => {
      return api.post('/insights/batch/analyze/', {
        transcript_ids: transcriptIds,
        template_id: templateId
      })
    },

    // 批量审核分析
    reviewAnalysis: (analysisIds, reviewData) => {
      return api.post('/insights/batch/review/', {
        analysis_ids: analysisIds,
        ...reviewData
      })
    },

    // 批量删除文稿
    deleteTranscripts: (transcriptIds) => {
      return api.post('/insights/batch/delete-transcripts/', {
        transcript_ids: transcriptIds
      })
    },

    // 批量删除分析
    deleteAnalysis: (analysisIds) => {
      return api.post('/insights/batch/delete-analysis/', {
        analysis_ids: analysisIds
      })
    }
  },

  // 搜索和过滤
  search: {
    // 搜索文稿
    transcripts: (query, filters = {}) => {
      return api.get('/insights/search/transcripts/', {
        q: query,
        ...filters
      })
    },

    // 搜索分析结果
    analysis: (query, filters = {}) => {
      return api.get('/insights/search/analysis/', {
        q: query,
        ...filters
      })
    },

    // 全文搜索
    fullText: (query, scope = 'all') => {
      return api.get('/insights/search/full-text/', {
        q: query,
        scope
      })
    }
  },

  // 导入导出
  importExport: {
    // 导入文稿
    importTranscripts: (file, options = {}) => {
      const formData = new FormData()
      formData.append('file', file)
      Object.entries(options).forEach(([key, value]) => {
        formData.append(key, value)
      })
      return api.upload('/insights/import/transcripts/', formData)
    },

    // 导出文稿
    exportTranscripts: (filters = {}, format = 'xlsx') => {
      return api.download(
        '/insights/export/transcripts/',
        `transcripts_export.${format}`,
        { params: { ...filters, format } }
      )
    },

    // 导出分析结果
    exportAnalysis: (filters = {}, format = 'xlsx') => {
      return api.download(
        '/insights/export/analysis/',
        `analysis_export.${format}`,
        { params: { ...filters, format } }
      )
    },

    // 导入模板
    importTemplates: (file) => {
      const formData = new FormData()
      formData.append('file', file)
      return api.upload('/insights/import/templates/', formData)
    },

    // 导出模板
    exportTemplates: (templateIds = [], format = 'json') => {
      return api.download(
        '/insights/export/templates/',
        `templates_export.${format}`,
        { params: { template_ids: templateIds.join(','), format } }
      )
    }
  }
}