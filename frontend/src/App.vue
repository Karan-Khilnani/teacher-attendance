<template>
  <div class="min-h-screen bg-cover bg-center relative" :style="{ backgroundImage: `url('/assets/bg.jpg')` }" >

<!-- HEADER -->
<div class="sticky top-0 z-50 backdrop-blur bg-white/70 border-b">
  <div class="max-w-6xl mx-auto px-6 py-4 flex justify-between items-center">
    <div>
      <h1 class="text-2xl font-bold text-gray-800">📚 Teacher Attendance</h1>
      <p class="text-sm text-gray-500">{{ currentDate }}</p>
    </div>

    <div class="flex gap-2">
      <button 
  @click="markAll('PRESENT')" 
  class="bg-green-500 text-white px-3 py-2 rounded-lg text-sm">
  Mark All Present
</button>

<button 
  @click="markAll('ABSENT')" 
  class="bg-red-500 text-white px-3 py-2 rounded-lg text-sm">
  Mark All Absent
</button>
    </div>
  </div>
</div>

<div class="max-w-6xl mx-auto p-6">

  <!-- SEARCH + PROGRESS -->
  <div class="flex justify-between items-center mb-4">
    <input v-model="search" placeholder="Search student..."
      class="px-4 py-2 border rounded-lg w-64 focus:ring-2 focus:ring-blue-400"/>

    <div class="text-sm text-gray-600">
      {{ completedCount }}/{{ students.length }} marked
    </div>
  </div>

  <!-- LOADING -->
  <div v-if="isLoading" class="space-y-3">
    <div v-for="i in 6" :key="i" class="h-12 bg-gray-200 rounded animate-pulse"></div>
  </div>

  <!-- TABLE -->
  <div v-else class="bg-white rounded-xl shadow overflow-hidden">
    <table class="w-full">
      <thead class="bg-gray-50 text-gray-600 text-sm">
        <tr>
          <th class="p-4 text-left">Roll</th>
          <th class="p-4 text-left">Name</th>
          <th class="p-4 text-center">Status</th>
        </tr>
      </thead>

      <tbody>
        <tr v-for="student in filteredStudents" :key="student.id"
          class="border-t hover:bg-gray-50 transition">

          <td class="p-4 font-mono text-sm">{{ student.roll_number }}</td>
          <td class="p-4 font-medium">{{ student.name }}</td>

          <td class="p-4 text-center">
            <div class="flex justify-center gap-2">

          <button
            @click="markAttendance(student.id, 'PRESENT')"
            :class="[
              'px-3 py-1 rounded-full text-sm border',
              attendance[student.id] === 'PRESENT'
                ? 'bg-green-500 text-white border-green-500'
                : 'bg-white text-gray-600'
            ]"
          >
            ✔ Present
          </button>
          <button
            @click="markAttendance(student.id, 'ABSENT')"
            :class="[
            'px-3 py-1 rounded-full text-sm border',
            attendance[student.id] === 'ABSENT'
              ? 'bg-red-500 text-white border-red-500'
              : 'bg-white text-gray-600'
          ]"
          >
            ✔ Absent
          </button>

            </div>
          </td>

        </tr>
      </tbody>
    </table>
  </div>

</div>

<!-- SAVE BAR -->
<div class="fixed bottom-0 left-0 right-0 bg-white border-t p-4 flex justify-between items-center">
  <p class="text-sm text-gray-600">
    Ready to save today's attendance
  </p>

  <button
    :disabled="completedCount !== students.length || saving"
    @click="submitAttendance"
    class="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white px-6 py-2 rounded-lg shadow">
    {{ saving ? 'Saving...' : 'Save Attendance' }}
  </button>
</div>


  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import axios from 'axios'

interface Student {
  id: number;
  name: string;
  roll_number: string;
}

const students = ref<Student[]>([])
const attendance = ref<Record<number, string>>({})
const isLoading = ref(true)
const saving = ref(false)
const search = ref('')

// DATE
const rawDate = new Date()
const currentDateApi = rawDate.toISOString().split('T')[0]

const currentDate = new Date().toLocaleDateString('en-IN', {
  timeZone: 'Asia/Kolkata',
  weekday: 'long',
  year: 'numeric',
  month: 'long',
  day: 'numeric'
})

// FETCH
onMounted(async () => {
  try {
    const res = await axios.get('http://127.0.0.1:8000/api/students/')
    students.value = res.data

    students.value.forEach(s => {
      attendance.value[s.id] = 'PRESENT'
    })

  } catch (err) {
    console.error(err)
  } finally {
    isLoading.value = false
  }
})

// COMPUTED
const filteredStudents = computed(() =>
  students.value.filter(s =>
    s.name.toLowerCase().includes(search.value.toLowerCase()) ||
    s.roll_number.includes(search.value)
  )
)

const completedCount = computed(() =>
  Object.keys(attendance.value).length
)

// ACTIONS
const markAttendance = (id: number, status: string) => {
  attendance.value[id] = status
}

const markAll = (status: string) => {
  students.value.forEach(s => {
    attendance.value[s.id] = status
  })
}

// SAVE
const submitAttendance = async () => {
  saving.value = true

  try {
    await Promise.all(
      students.value.map(s =>
        axios.post('http://127.0.0.1:8000/api/attendance/', {
          student: s.id,
          date: currentDateApi,
          status: attendance.value[s.id]
        })
      )
    )

    alert('✅ Attendance saved successfully')

  } catch (err) {
    alert('❌ Error saving attendance')
  } finally {
    saving.value = false
  }
}
</script>


