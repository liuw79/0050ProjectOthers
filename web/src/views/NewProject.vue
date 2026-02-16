<template>
  <div class="max-w-3xl mx-auto">
    <!-- Step 指示器 -->
    <div class="flex items-center mb-8">
      <div :class="stepClass(1)">1. 确定选题</div>
      <div class="flex-1 h-1 mx-4" :class="step >= 2 ? 'bg-blue-500' : 'bg-gray-200'"></div>
      <div :class="stepClass(2)">2. 素材准备</div>
      <div class="flex-1 h-1 mx-4" :class="step >= 3 ? 'bg-blue-500' : 'bg-gray-200'"></div>
      <div :class="stepClass(3)">3. 生成内容</div>
    </div>

    <!-- Step 1: 确定选题 -->
    <div v-if="step === 1" class="bg-white rounded-lg p-6 shadow-sm">
      <h2 class="text-xl font-bold mb-4">你想写什么？</h2>

      <!-- 方式一：选课程 -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">方式一：选择课程</label>
        <div class="flex flex-wrap gap-2">
          <button
            v-for="course in courses"
            :key="course.id"
            @click="toggleCourse(course.id)"
            :class="selectedCourses.includes(course.id) ? 'bg-blue-500 text-white' : 'bg-gray-100 text-gray-700'"
            class="px-4 py-2 rounded-lg hover:opacity-80"
          >
            {{ course.name }}
          </button>
        </div>
      </div>

      <!-- 方式二：关键词 -->
      <div class="mb-6">
        <label class="block text-sm font-medium text-gray-700 mb-2">方式二：输入关键词或想法</label>
        <textarea
          v-model="keywords"
          placeholder="例如：组织撕裂、第一曲线、战略共识"
          class="w-full border rounded-lg p-3 h-24"
        ></textarea>
      </div>

      <button
        @click="suggestTopics"
        :disabled="loading"
        class="w-full bg-blue-500 text-white py-3 rounded-lg hover:bg-blue-600 disabled:opacity-50"
      >
        {{ loading ? 'AI 分析中...' : 'AI 帮我找选题 →' }}
      </button>

      <!-- 推荐选题 -->
      <div v-if="suggestedTopics.length > 0" class="mt-6">
        <h3 class="font-medium mb-3">📋 推荐选题（点击选择）</h3>
        <div class="space-y-2">
          <button
            v-for="(topic, i) in suggestedTopics"
            :key="i"
            @click="selectedTopic = topic.title"
            :class="selectedTopic === topic.title ? 'border-blue-500 bg-blue-50' : 'border-gray-200'"
            class="w-full text-left border rounded-lg p-3 hover:border-blue-300"
          >
            <div class="font-medium">{{ topic.title }}</div>
            <div class="text-sm text-gray-500">{{ topic.angle }}</div>
          </button>
        </div>

        <!-- 自定义选题 -->
        <div class="mt-4">
          <label class="block text-sm font-medium text-gray-700 mb-2">或者自己写一个：</label>
          <input
            v-model="customTopic"
            type="text"
            placeholder="输入你的选题..."
            class="w-full border rounded-lg p-3"
          />
        </div>

        <button
          @click="confirmTopic"
          :disabled="!selectedTopic && !customTopic"
          class="mt-4 w-full bg-green-500 text-white py-3 rounded-lg hover:bg-green-600 disabled:opacity-50"
        >
          确认选题 →
        </button>
      </div>
    </div>

    <!-- Step 2: 素材准备 -->
    <div v-if="step === 2" class="bg-white rounded-lg p-6 shadow-sm">
      <h2 class="text-xl font-bold mb-2">Step 2: 素材准备</h2>
      <p class="text-gray-500 mb-4">选题：{{ finalTopic }}</p>

      <div v-if="loadingMaterials" class="text-center py-8 text-gray-500">
        AI 正在准备素材...
      </div>

      <div v-else>
        <!-- 课程素材 -->
        <MaterialSection
          title="📦 课程素材"
          :materials="materials.course"
          v-model:selected="selectedMaterials"
        />

        <!-- 用户画像 -->
        <MaterialSection
          title="👤 用户画像"
          :materials="materials.profile"
          v-model:selected="selectedMaterials"
        />

        <!-- 高维品牌 -->
        <MaterialSection
          title="🏢 高维品牌"
          :materials="materials.brand"
          v-model:selected="selectedMaterials"
        />

        <!-- 参考标题 -->
        <MaterialSection
          title="📝 参考标题"
          :materials="materials.reference"
          v-model:selected="selectedMaterials"
        />

        <div class="flex gap-4 mt-6">
          <button
            @click="previewPrompt"
            class="flex-1 border border-blue-500 text-blue-500 py-3 rounded-lg hover:bg-blue-50"
          >
            预览 Prompt
          </button>
          <button
            @click="step = 3"
            :disabled="selectedMaterials.length === 0"
            class="flex-1 bg-green-500 text-white py-3 rounded-lg hover:bg-green-600 disabled:opacity-50"
          >
            开始写作 →
          </button>
        </div>
      </div>
    </div>

    <!-- Step 3: 生成内容 -->
    <div v-if="step === 3" class="bg-white rounded-lg p-6 shadow-sm">
      <h2 class="text-xl font-bold mb-4">Step 3: 生成内容</h2>

      <div v-if="!generatedContent" class="text-center py-8">
        <button
          @click="generateContent"
          :disabled="generating"
          class="bg-blue-500 text-white px-8 py-3 rounded-lg hover:bg-blue-600 disabled:opacity-50"
        >
          {{ generating ? 'AI 写作中...' : '生成文章' }}
        </button>
      </div>

      <div v-else>
        <div class="prose max-w-none mb-6" v-html="renderedContent"></div>
        <div class="flex gap-4">
          <button @click="copyContent" class="flex-1 border py-2 rounded-lg hover:bg-gray-50">
            复制
          </button>
          <button @click="saveProject" class="flex-1 bg-green-500 text-white py-2 rounded-lg hover:bg-green-600">
            保存
          </button>
        </div>
      </div>
    </div>

    <!-- Prompt 预览弹窗 -->
    <div v-if="showPromptPreview" class="fixed inset-0 bg-black/50 flex items-center justify-center p-4" @click.self="showPromptPreview = false">
      <div class="bg-white rounded-lg p-6 max-w-3xl max-h-[80vh] overflow-auto">
        <h3 class="font-bold mb-4">AI 将收到的完整 Prompt</h3>
        <pre class="bg-gray-100 p-4 rounded text-sm whitespace-pre-wrap">{{ previewPromptText }}</pre>
        <button @click="showPromptPreview = false" class="mt-4 w-full bg-gray-200 py-2 rounded-lg">关闭</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';
import MaterialSection from '../components/MaterialSection.vue';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:3000';

const step = ref(1);
const courses = ref([]);
const selectedCourses = ref([]);
const keywords = ref('');
const loading = ref(false);
const suggestedTopics = ref([]);
const selectedTopic = ref('');
const customTopic = ref('');
const finalTopic = ref('');
const loadingMaterials = ref(false);
const materials = ref({ course: [], profile: [], brand: [], reference: [] });
const selectedMaterials = ref([]);
const showPromptPreview = ref(false);
const previewPromptText = ref('');
const generating = ref(false);
const generatedContent = ref('');

const stepClass = (n) => `px-4 py-2 rounded-full ${step.value >= n ? 'bg-blue-500 text-white' : 'bg-gray-200 text-gray-500'}`;

// 加载课程列表
async function loadCourses() {
  try {
    const res = await fetch(`${API_BASE}/api/courses`);
    const data = await res.json();
    if (data.success) courses.value = data.courses;
  } catch (e) {
    console.error('加载课程失败', e);
  }
}
loadCourses();

function toggleCourse(id) {
  const idx = selectedCourses.value.indexOf(id);
  if (idx >= 0) selectedCourses.value.splice(idx, 1);
  else selectedCourses.value.push(id);
}

async function suggestTopics() {
  loading.value = true;
  try {
    const res = await fetch(`${API_BASE}/api/topics/suggest`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        courseIds: selectedCourses.value,
        keywords: keywords.value,
      }),
    });
    const data = await res.json();
    if (data.success) suggestedTopics.value = data.topics;
  } finally {
    loading.value = false;
  }
}

function confirmTopic() {
  finalTopic.value = customTopic.value || selectedTopic.value;
  step.value = 2;
  loadMaterials();
}

async function loadMaterials() {
  loadingMaterials.value = true;
  try {
    const res = await fetch(`${API_BASE}/api/suggest-materials`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: finalTopic.value,
        courseIds: selectedCourses.value,
      }),
    });
    const data = await res.json();
    if (data.success) {
      materials.value = data.materials;
      // 默认全选
      selectedMaterials.value = [
        ...data.materials.profile.map(m => m.id),
        ...data.materials.brand.map(m => m.id),
        ...data.materials.reference.map(m => m.id),
        ...data.materials.course.map(m => m.id),
      ];
    }
  } finally {
    loadingMaterials.value = false;
  }
}

async function previewPrompt() {
  const res = await fetch(`${API_BASE}/api/write/preview`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: finalTopic.value,
      materialIds: selectedMaterials.value,
    }),
  });
  const data = await res.json();
  if (data.success) {
    previewPromptText.value = data.prompt;
    showPromptPreview.value = true;
  }
}

async function generateContent() {
  generating.value = true;
  try {
    const res = await fetch(`${API_BASE}/api/write/generate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title: finalTopic.value,
        materialIds: selectedMaterials.value,
      }),
    });
    const data = await res.json();
    if (data.success) generatedContent.value = data.content;
  } finally {
    generating.value = false;
  }
}

const renderedContent = computed(() => {
  if (!generatedContent.value) return '';
  return generatedContent.value
    .replace(/^## (.+)$/gm, '<h2 class="text-xl font-bold mt-6 mb-2">$1</h2>')
    .replace(/^### (.+)$/gm, '<h3 class="text-lg font-bold mt-4 mb-2">$1</h3>')
    .replace(/\n\n/g, '</p><p class="my-3">')
    .replace(/\n/g, '<br>');
});

function copyContent() {
  navigator.clipboard.writeText(generatedContent.value);
  alert('已复制');
}

function saveProject() {
  alert('保存功能待实现');
}
</script>
