<template>
  <div class="min-h-screen bg-gray-50">
    <nav class="bg-white border-b px-6 py-4">
      <div class="flex items-center justify-between max-w-6xl mx-auto">
        <router-link to="/" class="text-xl font-bold text-gray-800">GW.Content</router-link>
        <router-link to="/new" class="bg-blue-500 text-white px-4 py-2 rounded-lg hover:bg-blue-600">
          新建项目
        </router-link>
      </div>
    </nav>
    <main class="max-w-6xl mx-auto p-6">
      <router-view />
    </main>
  </div>
</template>
