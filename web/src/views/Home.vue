<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">写作项目</h1>
    <div v-if="projects.length === 0" class="text-gray-500">
      暂无项目，点击右上角"新建项目"开始
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
const projects = ref([]);
</script>
