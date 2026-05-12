<template>
  <Layout page-title="标题词云分析">
    <div class="container-fluid mt-4">
      <!-- 导出区域 -->
      <el-card class="mb-4" shadow="never">
        <div class="export-section">
          <div class="export-buttons">
            <el-button type="success" @click="handleExport('excel')" :loading="exporting">
              <el-icon class="mr-2"><Document /></el-icon>
              导出Excel
            </el-button>
            <el-button type="warning" @click="handleExport('csv')" :loading="exporting">
              <el-icon class="mr-2"><Document /></el-icon>
              导出CSV
            </el-button>
            <el-button type="info" @click="handleExport('txt')" :loading="exporting">
              <el-icon class="mr-2"><Document /></el-icon>
              导出TXT
            </el-button>
          </div>
        </div>
      </el-card>

      <!-- 图表区域 -->
      <el-card shadow="never">
        <template #header>
          <div class="card-header">
            <h3 class="mb-0">标题词云分析</h3>
          </div>
        </template>
        <div class="chart-container">
          <div v-if="loading" class="text-center py-5">
            <el-icon class="is-loading" size="32"><Loading /></el-icon>
            <p>加载中...</p>
          </div>
          <div v-else-if="chartData.length === 0" class="text-center py-5">
            <p class="text-muted">暂无数据</p>
          </div>
          <div v-else>
            <div ref="chartRef" class="chart"></div>
          </div>
        </div>
      </el-card>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, Loading } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import Layout from '../components/Layout.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const chartData = ref([])
const loading = ref(false)
const exporting = ref(false)

const chartRef = ref(null)
let chart = null

// 加载词云库（确保全局挂载 echarts，并避免重复加载）
const loadWordCloud = () => {
  return new Promise((resolve) => {
    // 确保插件能找到全局 echarts
    if (!window.echarts) {
      window.echarts = echarts
    }
    // 已加载则直接返回
    if (window._wordCloudLoaded) {
      resolve(true)
      return
    }

    const script = document.createElement('script')
    script.src = '/public/assets/js/plugins/chart.js/dist/echarts-wordcloud.min.js'
    script.onload = () => {
      window._wordCloudLoaded = true
      // 略微延迟保证插件完成注册
      setTimeout(() => resolve(true), 50)
    }
    script.onerror = () => {
      ElMessage.error('加载词云库失败')
      resolve(false)
    }
    document.head.appendChild(script)
  })
}

// 加载数据
const loadData = async () => {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE_URL}/app/part6/data/`, {
      credentials: 'include'
    })
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ message: '获取数据失败' }))
      throw new Error(errorData.message || '获取数据失败')
    }
    
    const data = await res.json()
    
    chartData.value = (data.data || []).map(item => ({
      name: item.name || '',
      value: typeof item.value === 'number' ? item.value : parseInt(item.value) || 0
    })).filter(item => item.name && item.value > 0)
    
    await nextTick()
    setTimeout(() => {
      initChart()
    }, 200)
  } catch (e) {
    ElMessage.error(e.message || '加载数据失败')
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 初始化图表
const initChart = async () => {
  if (!chartRef.value || chartData.value.length === 0) {
    return
  }
  
  // 加载词云库
  const loaded = await loadWordCloud()
  if (!loaded) {
    return
  }
  
  if (chart) {
    chart.dispose()
    chart = null
  }
  
  chart = echarts.init(chartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c}'
    },
    series: [
      {
        type: 'wordCloud',
        gridSize: 2,
        sizeRange: [12, 60],
        rotationRange: [-90, 90],
        shape: 'pentagon',
        width: '100%',
        height: '100%',
        drawOutOfBound: true,
        textStyle: {
          fontFamily: 'sans-serif',
          fontWeight: 'bold',
          color: function() {
            return 'rgb(' + [
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160),
              Math.round(Math.random() * 160)
            ].join(',') + ')'
          }
        },
        emphasis: {
          focus: 'self',
          textStyle: {
            shadowBlur: 10,
            shadowColor: '#333'
          }
        },
        data: chartData.value
      }
    ]
  }
  
  chart.setOption(option, true)
  
  setTimeout(() => {
    if (chart) {
      chart.resize()
    }
  }, 100)
}

// 导出数据
const handleExport = async (type) => {
  exporting.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/app/part6/export/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        type: type
      })
    })
    
    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.message || '导出失败')
    }
    
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    
    const contentDisposition = response.headers.get('Content-Disposition')
    let filename = `标题词云分析_${new Date().getTime()}`
    if (contentDisposition) {
      const filenameMatch = contentDisposition.match(/filename="?(.+)"?/i)
      if (filenameMatch) {
        filename = filenameMatch[1]
      }
    }
    
    a.download = filename
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    window.URL.revokeObjectURL(url)
    
    ElMessage.success('导出成功')
  } catch (e) {
    ElMessage.error(e.message || '导出失败')
    console.error(e)
  } finally {
    exporting.value = false
  }
}

// 窗口大小变化时调整图表
const handleResize = () => {
  if (chart) {
    chart.resize()
  }
}

onMounted(() => {
  loadData()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  if (chart) {
    chart.dispose()
    chart = null
  }
})
</script>

<style scoped>
.export-section {
  padding: 1rem 0;
}

.export-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.mr-2 {
  margin-right: 8px;
}

.chart-container {
  min-height: 600px;
  padding: 1rem;
  position: relative;
}

.chart {
  width: 100%;
  height: 600px;
  min-height: 600px;
}

.card-header {
  padding: 1rem 0;
}
</style>

