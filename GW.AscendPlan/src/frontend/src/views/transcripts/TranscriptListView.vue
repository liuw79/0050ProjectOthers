<template>
  <div class="transcript-list">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="page-title">
        <h1>访谈文稿</h1>
        <p class="page-description">管理和查看所有访谈录音的文字转录内容。</p>
      </div>
      
      <div class="page-actions">
        <el-button
          type="primary"
          :icon="Plus"
          @click="showUploadDialog = true"
        >
          上传录音
        </el-button>
        
        <el-button
          :icon="Download"
          @click="handleBatchExport"
          :disabled="!selectedTranscripts.length"
        >
          批量导出
        </el-button>
      </div>
    </div>
    
    <!-- 搜索筛选 -->
    <el-card class="search-card" shadow="never">
      <el-form
        :model="searchForm"
        :inline="true"
        class="search-form"
        @submit.prevent="handleSearch"
      >
        <el-form-item label="客户姓名">
          <el-input
            v-model="searchForm.customer_name"
            placeholder="请输入客户姓名"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="预约编号">
          <el-input
            v-model="searchForm.appointment_id"
            placeholder="请输入预约编号"
            clearable
            style="width: 200px"
          />
        </el-form-item>
        
        <el-form-item label="转录状态">
          <el-select
            v-model="searchForm.status"
            placeholder="请选择状态"
            clearable
            style="width: 150px"
          >
            <el-option label="处理中" value="processing" />
            <el-option label="已完成" value="completed" />
            <el-option label="失败" value="failed" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="创建时间">
          <el-date-picker
            v-model="searchForm.date_range"
            type="daterange"
            range-separator="至"
            start-placeholder="开始日期"
            end-placeholder="结束日期"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
            style="width: 240px"
          />
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            搜索
          </el-button>
          
          <el-button @click="handleReset">
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
    
    <!-- 数据表格 -->
    <el-card class="table-card" shadow="never">
      <div class="table-header">
        <div class="table-info">
          <span>共 {{ pagination.total }} 条记录</span>
          <span v-if="selectedTranscripts.length" class="selected-info">
            已选择 {{ selectedTranscripts.length }} 项
          </span>
        </div>
        
        <div class="table-actions">
          <el-button
            size="small"
            :icon="Refresh"
            @click="loadTranscripts"
          >
            刷新
          </el-button>
          
          <el-dropdown @command="handleBatchAction">
            <el-button size="small" :disabled="!selectedTranscripts.length">
              批量操作
              <el-icon class="el-icon--right">
                <ArrowDown />
              </el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="export">导出文稿</el-dropdown-item>
                <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      
      <el-table
        v-loading="loading"
        :data="transcripts"
        @selection-change="handleSelectionChange"
        @sort-change="handleSortChange"
        stripe
        style="width: 100%"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column
          prop="id"
          label="ID"
          width="80"
          sortable="custom"
        />
        
        <el-table-column
          prop="customer_name"
          label="客户姓名"
          min-width="120"
          show-overflow-tooltip
        >
          <template #default="{ row }">
            <el-link
              type="primary"
              @click="$router.push(`/customers/${row.customer_id}`)"
            >
              {{ row.customer_name }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="appointment_id"
          label="预约编号"
          width="120"
          show-overflow-tooltip
        >
          <template #default="{ row }">
            <el-link
              type="primary"
              @click="$router.push(`/appointments/${row.appointment_id}`)"
            >
              #{{ row.appointment_id }}
            </el-link>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="title"
          label="文稿标题"
          min-width="200"
          show-overflow-tooltip
        />
        
        <el-table-column
          prop="duration"
          label="录音时长"
          width="100"
          align="center"
        >
          <template #default="{ row }">
            {{ formatDuration(row.duration) }}
          </template>
        </el-table-column>
        
        <el-table-column
          prop="word_count"
          label="字数"
          width="80"
          align="center"
        >
          <template #default="{ row }">
            {{ row.word_count || '--' }}
          </template>
        </el-table-column>
        
        <el-table-column
          prop="status"
          label="状态"
          width="100"
          align="center"
        >
          <template #default="{ row }">
            <el-tag
              :type="getStatusType(row.status)"
              size="small"
            >
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="progress"
          label="进度"
          width="120"
          align="center"
        >
          <template #default="{ row }">
            <el-progress
              v-if="row.status === 'processing'"
              :percentage="row.progress || 0"
              :stroke-width="6"
              :show-text="false"
            />
            <span v-else-if="row.status === 'completed'" class="text-success">
              100%
            </span>
            <span v-else class="text-danger">
              --
            </span>
          </template>
        </el-table-column>
        
        <el-table-column
          prop="created_at"
          label="创建时间"
          width="160"
          sortable="custom"
        >
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column
          label="操作"
          width="200"
          fixed="right"
        >
          <template #default="{ row }">
            <div class="action-buttons">
              <el-button
                size="small"
                type="primary"
                link
                @click="handleView(row)"
              >
                查看
              </el-button>
              
              <el-button
                v-if="row.status === 'completed'"
                size="small"
                type="primary"
                link
                @click="handleEdit(row)"
              >
                编辑
              </el-button>
              
              <el-button
                v-if="row.status === 'completed'"
                size="small"
                type="primary"
                link
                @click="handleExport(row)"
              >
                导出
              </el-button>
              
              <el-button
                v-if="row.status === 'failed'"
                size="small"
                type="warning"
                link
                @click="handleRetry(row)"
              >
                重试
              </el-button>
              
              <el-popconfirm
                title="确定要删除这个文稿吗？"
                @confirm="handleDelete(row)"
              >
                <template #reference>
                  <el-button
                    size="small"
                    type="danger"
                    link
                  >
                    删除
                  </el-button>
                </template>
              </el-popconfirm>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-container">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </el-card>
    
    <!-- 上传录音对话框 -->
    <el-dialog
      v-model="showUploadDialog"
      title="上传录音文件"
      width="600px"
      :close-on-click-modal="false"
    >
      <el-form
        ref="uploadFormRef"
        :model="uploadForm"
        :rules="uploadRules"
        label-width="100px"
      >
        <el-form-item label="关联预约" prop="appointment_id">
          <el-select
            v-model="uploadForm.appointment_id"
            placeholder="请选择关联的预约"
            filterable
            remote
            :remote-method="searchAppointments"
            :loading="searchingAppointments"
            style="width: 100%"
          >
            <el-option
              v-for="appointment in appointmentOptions"
              :key="appointment.id"
              :label="`#${appointment.id} - ${appointment.customer_name} (${formatDate(appointment.appointment_date)})`"
              :value="appointment.id"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="文稿标题" prop="title">
          <el-input
            v-model="uploadForm.title"
            placeholder="请输入文稿标题"
            maxlength="100"
            show-word-limit
          />
        </el-form-item>
        
        <el-form-item label="录音文件" prop="file" required>
          <el-upload
            ref="uploadRef"
            :file-list="uploadForm.fileList"
            :auto-upload="false"
            :on-change="handleFileChange"
            :on-remove="handleFileRemove"
            :before-upload="beforeUpload"
            accept=".mp3,.wav,.m4a,.aac,.flac"
            drag
          >
            <el-icon class="el-icon--upload">
              <UploadFilled />
            </el-icon>
            <div class="el-upload__text">
              将录音文件拖到此处，或<em>点击上传</em>
            </div>
            <template #tip>
              <div class="el-upload__tip">
                支持 MP3、WAV、M4A、AAC、FLAC 格式，文件大小不超过 100MB
              </div>
            </template>
          </el-upload>
        </el-form-item>
        
        <el-form-item label="备注">
          <el-input
            v-model="uploadForm.notes"
            type="textarea"
            :rows="3"
            placeholder="请输入备注信息"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="showUploadDialog = false">
            取消
          </el-button>
          <el-button
            type="primary"
            :loading="uploading"
            @click="handleUpload"
          >
            {{ uploading ? '上传中...' : '开始转录' }}
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Plus,
  Download,
  Refresh,
  ArrowDown,
  UploadFilled
} from '@element-plus/icons-vue'
import { appointmentsApi } from '@/api/appointments'
import dayjs from 'dayjs'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const uploading = ref(false)
const searchingAppointments = ref(false)
const showUploadDialog = ref(false)
const uploadFormRef = ref()
const uploadRef = ref()
const transcripts = ref([])
const selectedTranscripts = ref([])
const appointmentOptions = ref([])

// 搜索表单
const searchForm = reactive({
  customer_name: '',
  appointment_id: '',
  status: '',
  date_range: []
})

// 上传表单
const uploadForm = reactive({
  appointment_id: '',
  title: '',
  file: null,
  fileList: [],
  notes: ''
})

// 上传表单验证规则
const uploadRules = {
  appointment_id: [
    { required: true, message: '请选择关联的预约', trigger: 'change' }
  ],
  title: [
    { required: true, message: '请输入文稿标题', trigger: 'blur' },
    { min: 2, max: 100, message: '标题长度在 2 到 100 个字符', trigger: 'blur' }
  ]
}

// 分页数据
const pagination = reactive({
  page: 1,
  size: 20,
  total: 0
})

// 排序数据
const sortData = reactive({
  prop: 'created_at',
  order: 'descending'
})

// 方法
const formatDate = (date) => {
  return date ? dayjs(date).format('YYYY-MM-DD HH:mm') : '--'
}

const formatDuration = (seconds) => {
  if (!seconds) return '--'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = seconds % 60
  
  if (hours > 0) {
    return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
  }
  return `${minutes}:${secs.toString().padStart(2, '0')}`
}

const getStatusType = (status) => {
  const statusMap = {
    processing: 'warning',
    completed: 'success',
    failed: 'danger'
  }
  return statusMap[status] || 'info'
}

const getStatusText = (status) => {
  const statusMap = {
    processing: '处理中',
    completed: '已完成',
    failed: '失败'
  }
  return statusMap[status] || '未知'
}

const loadTranscripts = async () => {
  try {
    loading.value = true
    const params = {
      page: pagination.page,
      size: pagination.size,
      sort_by: sortData.prop,
      sort_order: sortData.order === 'ascending' ? 'asc' : 'desc',
      ...searchForm
    }
    
    // 处理日期范围
    if (searchForm.date_range && searchForm.date_range.length === 2) {
      params.start_date = searchForm.date_range[0]
      params.end_date = searchForm.date_range[1]
    }
    
    const response = await appointmentsApi.getTranscripts(params)
    transcripts.value = response.data.items
    pagination.total = response.data.total
  } catch (error) {
    ElMessage.error(error.message || '获取文稿列表失败')
    console.error('获取文稿列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  pagination.page = 1
  loadTranscripts()
}

const handleReset = () => {
  Object.keys(searchForm).forEach(key => {
    if (Array.isArray(searchForm[key])) {
      searchForm[key] = []
    } else {
      searchForm[key] = ''
    }
  })
  handleSearch()
}

const handleSelectionChange = (selection) => {
  selectedTranscripts.value = selection
}

const handleSortChange = ({ prop, order }) => {
  sortData.prop = prop
  sortData.order = order
  loadTranscripts()
}

const handleSizeChange = (size) => {
  pagination.size = size
  pagination.page = 1
  loadTranscripts()
}

const handleCurrentChange = (page) => {
  pagination.page = page
  loadTranscripts()
}

const handleView = (row) => {
  router.push(`/transcripts/${row.id}`)
}

const handleEdit = (row) => {
  router.push(`/transcripts/${row.id}/edit`)
}

const handleExport = async (row) => {
  try {
    const response = await appointmentsApi.exportTranscript(row.id)
    // 创建下载链接
    const blob = new Blob([response.data], { type: 'application/octet-stream' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `${row.title || `文稿_${row.id}`}.docx`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error(error.message || '导出失败')
    console.error('导出失败:', error)
  }
}

const handleRetry = async (row) => {
  try {
    await appointmentsApi.retryTranscript(row.id)
    ElMessage.success('重新转录任务已提交')
    loadTranscripts()
  } catch (error) {
    ElMessage.error(error.message || '重试失败')
    console.error('重试失败:', error)
  }
}

const handleDelete = async (row) => {
  try {
    await appointmentsApi.deleteTranscript(row.id)
    ElMessage.success('删除成功')
    loadTranscripts()
  } catch (error) {
    ElMessage.error(error.message || '删除失败')
    console.error('删除失败:', error)
  }
}

const handleBatchAction = async (command) => {
  if (!selectedTranscripts.value.length) {
    ElMessage.warning('请先选择要操作的文稿')
    return
  }
  
  const ids = selectedTranscripts.value.map(item => item.id)
  
  try {
    if (command === 'export') {
      await handleBatchExport()
    } else if (command === 'delete') {
      await ElMessageBox.confirm(
        `确定要删除选中的 ${ids.length} 个文稿吗？`,
        '批量删除',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      )
      
      await appointmentsApi.batchDeleteTranscripts(ids)
      ElMessage.success('批量删除成功')
      loadTranscripts()
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error(error.message || '操作失败')
      console.error('批量操作失败:', error)
    }
  }
}

const handleBatchExport = async () => {
  if (!selectedTranscripts.value.length) {
    ElMessage.warning('请先选择要导出的文稿')
    return
  }
  
  try {
    const ids = selectedTranscripts.value.map(item => item.id)
    const response = await appointmentsApi.batchExportTranscripts(ids)
    
    // 创建下载链接
    const blob = new Blob([response.data], { type: 'application/zip' })
    const url = window.URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = `文稿批量导出_${dayjs().format('YYYY-MM-DD')}.zip`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('批量导出成功')
  } catch (error) {
    ElMessage.error(error.message || '批量导出失败')
    console.error('批量导出失败:', error)
  }
}

const searchAppointments = async (query) => {
  if (!query) {
    appointmentOptions.value = []
    return
  }
  
  try {
    searchingAppointments.value = true
    const response = await appointmentsApi.searchAppointments({
      keyword: query,
      status: 'completed',
      limit: 20
    })
    appointmentOptions.value = response.data.items
  } catch (error) {
    console.error('搜索预约失败:', error)
  } finally {
    searchingAppointments.value = false
  }
}

const handleFileChange = (file, fileList) => {
  uploadForm.fileList = fileList
  uploadForm.file = file.raw
  
  // 自动生成标题
  if (!uploadForm.title && file.name) {
    const nameWithoutExt = file.name.replace(/\.[^/.]+$/, '')
    uploadForm.title = nameWithoutExt
  }
}

const handleFileRemove = () => {
  uploadForm.fileList = []
  uploadForm.file = null
}

const beforeUpload = (file) => {
  const isValidType = ['audio/mpeg', 'audio/wav', 'audio/mp4', 'audio/aac', 'audio/flac'].includes(file.type)
  const isLt100M = file.size / 1024 / 1024 < 100
  
  if (!isValidType) {
    ElMessage.error('只能上传音频文件！')
    return false
  }
  if (!isLt100M) {
    ElMessage.error('文件大小不能超过 100MB！')
    return false
  }
  return true
}

const handleUpload = async () => {
  if (!uploadForm.file) {
    ElMessage.error('请选择要上传的录音文件')
    return
  }
  
  try {
    await uploadFormRef.value.validate()
  } catch (error) {
    ElMessage.error('请检查表单填写是否正确')
    return
  }
  
  try {
    uploading.value = true
    
    const formData = new FormData()
    formData.append('file', uploadForm.file)
    formData.append('appointment_id', uploadForm.appointment_id)
    formData.append('title', uploadForm.title)
    formData.append('notes', uploadForm.notes)
    
    await appointmentsApi.uploadTranscript(formData)
    ElMessage.success('录音上传成功，转录任务已开始')
    
    // 重置表单
    uploadForm.appointment_id = ''
    uploadForm.title = ''
    uploadForm.file = null
    uploadForm.fileList = []
    uploadForm.notes = ''
    
    showUploadDialog.value = false
    loadTranscripts()
  } catch (error) {
    ElMessage.error(error.message || '上传失败')
    console.error('上传失败:', error)
  } finally {
    uploading.value = false
  }
}

// 生命周期
onMounted(() => {
  loadTranscripts()
})
</script>

<style lang="scss" scoped>
.transcript-list {
  padding: 24px;
  background: var(--el-bg-color-page);
  min-height: calc(100vh - #{$header-height});
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  
  .page-title {
    h1 {
      margin: 0 0 8px 0;
      font-size: 28px;
      font-weight: 600;
      color: var(--el-text-color-primary);
    }
    
    .page-description {
      margin: 0;
      color: var(--el-text-color-secondary);
      font-size: 14px;
    }
  }
  
  .page-actions {
    display: flex;
    gap: 12px;
  }
}

.search-card {
  margin-bottom: 16px;
  
  .search-form {
    .el-form-item {
      margin-bottom: 16px;
    }
  }
}

.table-card {
  .table-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    
    .table-info {
      display: flex;
      align-items: center;
      gap: 16px;
      color: var(--el-text-color-secondary);
      font-size: 14px;
      
      .selected-info {
        color: var(--el-color-primary);
      }
    }
    
    .table-actions {
      display: flex;
      gap: 8px;
    }
  }
  
  .action-buttons {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }
  
  .pagination-container {
    display: flex;
    justify-content: center;
    margin-top: 24px;
  }
}

.text-success {
  color: var(--el-color-success);
}

.text-danger {
  color: var(--el-color-danger);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

// 响应式适配
@include respond-to(md) {
  .transcript-list {
    padding: 16px;
  }
  
  .page-header {
    flex-direction: column;
    gap: 16px;
    
    .page-actions {
      align-self: stretch;
      
      .el-button {
        flex: 1;
      }
    }
  }
  
  .search-form {
    .el-form-item {
      width: 100%;
      
      .el-input,
      .el-select,
      .el-date-picker {
        width: 100% !important;
      }
    }
  }
  
  .table-header {
    flex-direction: column;
    gap: 12px;
    
    .table-info,
    .table-actions {
      align-self: stretch;
    }
    
    .table-actions {
      .el-button {
        flex: 1;
      }
    }
  }
  
  .action-buttons {
    flex-direction: column;
    
    .el-button {
      width: 100%;
    }
  }
}

@include respond-to(sm) {
  .search-form {
    .el-form-item {
      .el-button {
        width: 100%;
        margin-top: 8px;
      }
    }
  }
}
</style>