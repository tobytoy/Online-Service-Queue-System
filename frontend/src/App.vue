<template>
  <div class="p-4">
    <h1 class="text-2xl font-bold mb-4">線上取號系統</h1>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div>
        <h2 class="text-xl font-semibold mb-2">客戶端</h2>
        <button @click="takeNumber" class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
          點擊取號
        </button>
        <div v-if="myTicket" class="mt-4 p-4 border rounded">
          <h3 class="font-bold">您的號碼</h3>
          <p>號碼: {{ myTicket.id }}</p>
          <p>狀態: {{ myTicket.status }}</p>
        </div>
      </div>
      <div>
        <h2 class="text-xl font-semibold mb-2">服務窗口狀態</h2>
        <div v-for="window in serviceWindows" :key="window.id" class="mb-2 p-2 border rounded">
          <p class="font-bold">{{ window.name }}</p>
          <p>當前號碼: {{ window.serving_ticket_id || '無' }}</p>
        </div>
      </div>
    </div>
    <div class="mt-8">
        <h2 class="text-xl font-semibold mb-2">管理者介面</h2>
        <div class="flex space-x-2">
            <select v-model="selectedWindow" class="border p-2 rounded">
                <option value="free">自由等待區</option>
                <option v-for="window in serviceWindows" :key="window.id" :value="window.id">
                    {{ window.name }}
                </option>
            </select>
            <button @click="addNumber" class="bg-green-500 hover:bg-green-700 text-white font-bold py-2 px-4 rounded">
                新增號碼
            </button>
            <button @click="nextNumber" class="bg-yellow-500 hover:bg-yellow-700 text-white font-bold py-2 px-4 rounded">
                下一位
            </button>
        </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'

const serviceWindows = ref([])
const myTicket = ref(null)
const selectedWindow = ref('free')

const fetchServiceWindows = async () => {
  const response = await fetch('/api/service_windows')
  serviceWindows.value = await response.json()
}

const takeNumber = async () => {
  const response = await fetch('/api/tickets', { method: 'POST' })
  myTicket.value = await response.json()
  alert(`您的號碼是 ${myTicket.value.id}`)
}

const addNumber = async () => {
    let url = '/api/tickets';
    let options = { method: 'POST' };

    if (selectedWindow.value !== 'free') {
        url = `/api/service_windows/${selectedWindow.value}/tickets`;
    }

    const response = await fetch(url, options);
    const newTicket = await response.json();
    alert(`已新增號碼 ${newTicket.id}`);
    fetchServiceWindows();
};

const nextNumber = async () => {
    if (selectedWindow.value === 'free') {
        alert('請選擇一個服務窗口');
        return;
    }
    const response = await fetch(`/api/service_windows/${selectedWindow.value}/next`, { method: 'POST' });
    const updatedWindow = await response.json();
    alert(`窗口 ${updatedWindow.name} 的下一位是 ${updatedWindow.serving_ticket_id}`);
    fetchServiceWindows();
};

onMounted(() => {
  fetchServiceWindows()
})
</script>
