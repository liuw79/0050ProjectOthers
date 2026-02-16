<template>
  <div class="mb-6">
    <h3 class="font-medium text-gray-700 mb-2">{{ title }}</h3>
    <div class="space-y-2">
      <div
        v-for="material in materials"
        :key="material.id"
        class="border rounded-lg overflow-hidden"
      >
        <div
          @click="toggle(material.id)"
          class="flex items-center p-3 cursor-pointer hover:bg-gray-50"
          :class="selected.includes(material.id) ? 'bg-blue-50' : ''"
        >
          <input
            type="checkbox"
            :checked="selected.includes(material.id)"
            @change="toggle(material.id)"
            class="mr-3"
          />
          <span class="font-medium">{{ material.title }}</span>
          <span v-if="material.content" class="ml-auto text-sm text-gray-400">
            {{ material.content.length }} 字
          </span>
        </div>

        <!-- 内容预览 -->
        <div v-if="expanded === material.id" class="px-3 pb-3 pt-0">
          <div class="bg-gray-50 rounded p-3 text-sm text-gray-600 whitespace-pre-wrap max-h-64 overflow-auto">
            {{ material.content }}
          </div>
        </div>
        <div v-else-if="material.content" class="px-3 pb-3 pt-0">
          <div class="text-sm text-gray-500 line-clamp-2">
            {{ material.content.slice(0, 100) }}...
            <button @click.stop="expanded = material.id" class="text-blue-500 ml-1">展开</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';

const props = defineProps({
  title: String,
  materials: { type: Array, default: () => [] },
  selected: { type: Array, default: () => [] },
});

const emit = defineEmits(['update:selected']);

const expanded = ref(null);

function toggle(id) {
  const newSelected = [...props.selected];
  const idx = newSelected.indexOf(id);
  if (idx >= 0) newSelected.splice(idx, 1);
  else newSelected.push(id);
  emit('update:selected', newSelected);
}
</script>
