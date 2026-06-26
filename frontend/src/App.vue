<template>
  <div class="min-h-screen bg-gray-100 p-6">
    <div class="max-w-4xl mx-auto bg-white shadow-md rounded-lg overflow-hidden">
      
      <div class="bg-blue-600 text-white p-6 flex justify-between items-center">
        <div>
          <h1 class="text-2xl font-bold">Teacher Attendance Portal</h1>
          <p class="text-sm opacity-90">Mark attendance for your class</p>
        </div>
        <div class="bg-blue-700 px-4 py-2 rounded text-sm font-semibold">
          Date: {{ currentDate }}
        </div>
      </div>

      <div class="p-6">
        <h2 class="text-xl font-semibold text-gray-700 mb-4">Student Roster</h2>
        
        <div class="overflow-x-auto">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-gray-50 border-b border-gray-200">
                <th class="p-4 font-semibold text-gray-600">Roll No.</th>
                <th class="p-4 font-semibold text-gray-600">Student Name</th>
                <th class="p-4 font-semibold text-gray-600 text-center">Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="student in students" :key="student.id" class="border-b border-gray-100 hover:bg-gray-50">
                <td class="p-4 font-mono text-sm text-gray-600">{{ student.roll_number }}</td>
                <td class="p-4 font-medium text-gray-800">{{ student.name }}</td>
                <td class="p-4 text-center">
                  <div class="inline-flex rounded-md shadow-sm" role="group">
                    <button 
                      @click="markAttendance(student.id, 'PRESENT')"
                      :class="[
                        'px-4 py-2 text-sm font-medium rounded-l-lg border',
                        attendance[student.id] === 'PRESENT' 
                          ? 'bg-green-500 text-white border-green-500' 
                          : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'
                      ]"
                    >
                      Present
                    </button>
                    <button 
                      @click="markAttendance(student.id, 'ABSENT')"
                      :class="[
                        'px-4 py-2 text-sm font-medium rounded-r-lg border-t border-b border-r',
                        attendance[student.id] === 'ABSENT' 
                          ? 'bg-red-500 text-white border-red-500' 
                          : 'bg-white text-gray-700 border-gray-200 hover:bg-gray-50'
                      ]"
                    >
                      Absent
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <div class="mt-6 flex justify-end">
          <button 
            @click="submitAttendance"
            class="bg-blue-600 hover:bg-blue-700 text-white font-semibold px-6 py-2 rounded-lg shadow transition"
          >
            Save Attendance
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue' // <-- Added onMounted here
import axios from 'axios'

// Format today's date for display and API payloads
const rawDate = new Date()
const currentDateApi = rawDate.toISOString().split('T')[0]

// Format today's date nicely
const currentDate = new Date().toLocaleDateString('en-US', {
   timeZone: 'Asia/Kolkata', weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
})

interface Student {
  id: number;
  name: string;
  roll_number: string;
}

// Start with an empty array so Django can fill it!
const students = ref<Student[]>([])
const attendance = ref<Record<number, string>>({})
const isLoading = ref(true)

// 1. Fetch live student records from Django when the portal loads
onMounted(async () => {
  try {
    const response = await axios.get<Student[]>('http://127.0.0.1:8000/api/students/')
    students.value = response.data // <-- This puts your database records into the UI
    
    // Pre-populate all live students to 'PRESENT' status automatically
    students.value.forEach(student => {
      attendance.value[student.id] = 'PRESENT'
    })
  } catch (error: any) {
    console.error("Error fetching students:", error)
    alert(`Failed to load student roster: ${error.message}`)
  } finally {
    isLoading.value = false
  }
})

const markAttendance = (studentId: number, status: string) => {
  attendance.value[studentId] = status
}

// 2. Submit saved attendance rows back to your Django DB
const submitAttendance = async () => {
  let savedCount = 0;
  let duplicateCount = 0;

  // Loops sequentially to handle database writes cleanly
  for (const student of students.value) {
    try {
      await axios.post('http://127.0.0.1:8000/api/attendance/', {
        student: student.id,
        date: currentDateApi,
        status: attendance.value[student.id]
      })
      savedCount++;
    } catch (error: any) {
      if (error.response?.status === 400 && JSON.stringify(error.response.data).includes('unique')) {
        duplicateCount++;
      } else {
        console.error("Unexpected error for student:", student.id, error)
      }
    }
  }

  if (savedCount > 0) {
    alert(`🎉 Successfully saved attendance for ${savedCount} students!`);
  } else if (duplicateCount > 0) {
    alert("⚠️ Attendance for today has already been locked in. To change it, update the existing rows in Django Admin.");
  }
}
</script>