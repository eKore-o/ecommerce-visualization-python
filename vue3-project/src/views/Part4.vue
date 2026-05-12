<template>
  <Layout page-title="价格区间分析">
    <div class="container-fluid mt-4">
      <!-- 筛选和导出区域 -->
      <el-card class="mb-4" shadow="never">
        <div class="filter-export-section">
          <div class="row align-items-center mb-3">
            <div class="col-auto">
              <label class="filter-label">价格区间筛选：</label>
            </div>
            <div class="col">
              <el-select
                v-model="selectedNames"
                multiple
                placeholder="请选择价格区间（不选则显示全部）"
                style="width: 100%"
                @change="handleFilterChange"
              >
                <el-option
                  v-for="name in names"
                  :key="name"
                  :label="name"
                  :value="name"
                />
              </el-select>
            </div>
            <div class="col-auto">
              <label class="filter-label">图表类型：</label>
            </div>
            <div class="col-auto">
              <el-select
                v-model="chartType"
                placeholder="选择图表类型"
                style="width: 200px"
                @change="handleChartTypeChange"
              >
                <el-option label="漏斗图" value="funnel" />
                <el-option label="柱状图" value="bar" />
                <el-option label="饼图" value="pie" />
                <el-option label="折线图" value="line" />
              </el-select>
            </div>
            <div class="col-auto">
              <el-button type="primary" @click="showColorDialog = true">
                <el-icon class="mr-2"><Brush /></el-icon>
                自定义颜色
              </el-button>
            </div>
          </div>
          
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
            <h3 class="mb-0">价格区间分析</h3>
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

    <!-- 颜色自定义对话框 -->
    <el-dialog
      v-model="showColorDialog"
      title="自定义图表颜色"
      width="600px"
    >
      <div class="color-custom-section">
        <div v-if="chartType === 'funnel'" class="color-item">
          <label>漏斗图颜色方案：</label>
          <el-select v-model="customColors.funnelScheme" style="width: 200px">
            <el-option label="默认" value="default" />
            <el-option label="蓝色系" value="blue" />
            <el-option label="绿色系" value="green" />
            <el-option label="红色系" value="red" />
            <el-option label="紫色系" value="purple" />
          </el-select>
        </div>
        <div v-if="chartType === 'bar'" class="color-item">
          <label>柱状图颜色（起始）：</label>
          <el-color-picker v-model="customColors.barStart" />
          <span class="color-value">{{ customColors.barStart }}</span>
        </div>
        <div v-if="chartType === 'bar'" class="color-item">
          <label>柱状图颜色（中间）：</label>
          <el-color-picker v-model="customColors.barMiddle" />
          <span class="color-value">{{ customColors.barMiddle }}</span>
        </div>
        <div v-if="chartType === 'bar'" class="color-item">
          <label>柱状图颜色（结束）：</label>
          <el-color-picker v-model="customColors.barEnd" />
          <span class="color-value">{{ customColors.barEnd }}</span>
        </div>
        <div v-if="chartType === 'pie'" class="color-item">
          <label>饼图颜色方案：</label>
          <el-select v-model="customColors.pieScheme" style="width: 200px">
            <el-option label="默认" value="default" />
            <el-option label="蓝色系" value="blue" />
            <el-option label="绿色系" value="green" />
            <el-option label="红色系" value="red" />
            <el-option label="紫色系" value="purple" />
          </el-select>
        </div>
        <div v-if="chartType === 'line'" class="color-item">
          <label>折线图颜色：</label>
          <el-color-picker v-model="customColors.lineColor" />
          <span class="color-value">{{ customColors.lineColor }}</span>
        </div>
        <div v-if="chartType === 'line'" class="color-item">
          <label>折线图填充颜色（起始）：</label>
          <el-color-picker v-model="customColors.lineAreaStart" />
          <span class="color-value">{{ customColors.lineAreaStart }}</span>
        </div>
        <div v-if="chartType === 'line'" class="color-item">
          <label>折线图填充颜色（结束）：</label>
          <el-color-picker v-model="customColors.lineAreaEnd" />
          <span class="color-value">{{ customColors.lineAreaEnd }}</span>
        </div>
      </div>
      <template #footer>
        <el-button @click="showColorDialog = false">取消</el-button>
        <el-button type="primary" @click="applyColors">应用</el-button>
        <el-button type="warning" @click="resetColors">重置</el-button>
      </template>
    </el-dialog>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, Loading, Brush } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import Layout from '../components/Layout.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const names = ref([])
const selectedNames = ref([])
const chartData = ref([])
const loading = ref(false)
const exporting = ref(false)
const chartType = ref('funnel') // 默认漏斗图
const showColorDialog = ref(false)

const chartRef = ref(null)
let chart = null

// 自定义颜色配置
const customColors = ref({
  funnelScheme: 'default',
  barStart: '#83bff6',
  barMiddle: '#188df0',
  barEnd: '#188df0',
  pieScheme: 'default',
  lineColor: '#5e72e4',
  lineAreaStart: 'rgba(94, 114, 228, 0.3)',
  lineAreaEnd: 'rgba(94, 114, 228, 0.1)'
})

// 默认颜色配置
const defaultColors = {
  funnelScheme: 'default',
  barStart: '#83bff6',
  barMiddle: '#188df0',
  barEnd: '#188df0',
  pieScheme: 'default',
  lineColor: '#5e72e4',
  lineAreaStart: 'rgba(94, 114, 228, 0.3)',
  lineAreaEnd: 'rgba(94, 114, 228, 0.1)'
}

// 漏斗图颜色方案
const funnelColorSchemes = {
  default: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
  blue: ['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'],
  green: ['#065f46', '#10b981', '#34d399', '#6ee7b7', '#d1fae5'],
  red: ['#991b1b', '#ef4444', '#f87171', '#fca5a5', '#fee2e2'],
  purple: ['#581c87', '#9333ea', '#a855f7', '#c084fc', '#e9d5ff']
}

// 饼图颜色方案
const pieColorSchemes = {
  default: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
  blue: ['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'],
  green: ['#065f46', '#10b981', '#34d399', '#6ee7b7', '#d1fae5'],
  red: ['#991b1b', '#ef4444', '#f87171', '#fca5a5', '#fee2e2'],
  purple: ['#581c87', '#9333ea', '#a855f7', '#c084fc', '#e9d5ff']
}

// 加载数据
const loadData = async (filtered = false) => {
  loading.value = true
  try {
    let url = `${API_BASE_URL}/app/part4/data/`
    if (filtered && selectedNames.value.length > 0) {
      const params = new URLSearchParams()
      selectedNames.value.forEach(name => {
        params.append('names', name)
      })
      url = `${API_BASE_URL}/app/part4/filtered/?${params.toString()}`
    }
    
    const res = await fetch(url, {
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
    
    if (!filtered) {
      names.value = data.names || []
    }
    
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
const initChart = () => {
  if (!chartRef.value || chartData.value.length === 0) {
    return
  }
  
  if (chart) {
    chart.dispose()
    chart = null
  }
  
  chart = echarts.init(chartRef.value)
  
  let option = {}
  
  if (chartType.value === 'funnel') {
    // 漏斗图配置
    const sortedData = [...chartData.value].sort((a, b) => b.value - a.value)
    const colorScheme = funnelColorSchemes[customColors.value.funnelScheme] || funnelColorSchemes.default
    option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        data: sortedData.map(item => item.name)
      },
      series: [
        {
          name: '商品数量',
          type: 'funnel',
          left: '10%',
          top: 60,
          bottom: 60,
          width: '80%',
          min: 0,
          max: Math.max(...sortedData.map(item => item.value)),
          minSize: '0%',
          maxSize: '100%',
          sort: 'descending',
          gap: 2,
          label: {
            show: true,
            position: 'inside',
            formatter: '{b}: {c}'
          },
          labelLine: {
            length: 10,
            lineStyle: {
              width: 1,
              type: 'solid'
            }
          },
          itemStyle: {
            borderColor: '#fff',
            borderWidth: 1
          },
          emphasis: {
            label: {
              fontSize: 20
            }
          },
          data: sortedData.map((item, index) => ({
            value: item.value,
            name: item.name,
            itemStyle: {
              color: colorScheme[index % colorScheme.length]
            }
          }))
        }
      ]
    }
  } else if (chartType.value === 'bar') {
    // 柱状图配置
    const sortedData = [...chartData.value].sort((a, b) => b.value - a.value)
    option = {
      tooltip: {
        trigger: 'axis',
        axisPointer: {
          type: 'shadow'
        }
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        data: sortedData.map(item => item.name),
        axisLabel: {
          rotate: 45,
          interval: 0
        }
      },
      yAxis: {
        type: 'value',
        name: '商品数量'
      },
      series: [
        {
          name: '商品数量',
          type: 'bar',
          data: sortedData.map(item => item.value),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: customColors.value.barStart },
              { offset: 0.5, color: customColors.value.barMiddle },
              { offset: 1, color: customColors.value.barEnd }
            ])
          }
        }
      ]
    }
  } else if (chartType.value === 'pie') {
    // 饼图配置
    const sortedData = [...chartData.value].sort((a, b) => b.value - a.value)
    const colorScheme = pieColorSchemes[customColors.value.pieScheme] || pieColorSchemes.default
    option = {
      tooltip: {
        trigger: 'item',
        formatter: '{a} <br/>{b}: {c} ({d}%)'
      },
      legend: {
        orient: 'vertical',
        left: 'left',
        data: sortedData.map(item => item.name)
      },
      color: colorScheme,
      series: [
        {
          name: '商品数量',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: {
            borderRadius: 10,
            borderColor: '#fff',
            borderWidth: 2
          },
          label: {
            show: true,
            formatter: '{b}: {c}'
          },
          data: sortedData.map(item => ({
            value: item.value,
            name: item.name
          }))
        }
      ]
    }
  } else if (chartType.value === 'line') {
    // 折线图配置
    const sortedData = [...chartData.value].sort((a, b) => b.value - a.value)
    option = {
      tooltip: {
        trigger: 'axis'
      },
      grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
      },
      xAxis: {
        type: 'category',
        boundaryGap: false,
        data: sortedData.map(item => item.name),
        axisLabel: {
          rotate: 45,
          interval: 0
        }
      },
      yAxis: {
        type: 'value',
        name: '商品数量'
      },
      series: [
        {
          name: '商品数量',
          type: 'line',
          smooth: true,
          data: sortedData.map(item => item.value),
          itemStyle: {
            color: customColors.value.lineColor
          },
          areaStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: customColors.value.lineAreaStart },
              { offset: 1, color: customColors.value.lineAreaEnd }
            ])
          }
        }
      ]
    }
  }
  
  chart.setOption(option, true)
  
  setTimeout(() => {
    if (chart) {
      chart.resize()
    }
  }, 100)
}

// 筛选变化
const handleFilterChange = () => {
  loadData(true)
}

// 图表类型变化
const handleChartTypeChange = () => {
  initChart()
}

// 应用颜色
const applyColors = () => {
  showColorDialog.value = false
  initChart()
  ElMessage.success('颜色已应用')
}

// 重置颜色
const resetColors = () => {
  customColors.value = { ...defaultColors }
  ElMessage.info('颜色已重置为默认值')
}

// 导出数据
const handleExport = async (type) => {
  exporting.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/app/part4/export/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        type: type,
        names: selectedNames.value
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
    let filename = `价格区间分析_${new Date().getTime()}`
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
.filter-export-section {
  padding: 1rem 0;
}

.filter-label {
  font-weight: 600;
  color: #303133;
  margin-right: 10px;
}

.export-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-top: 1rem;
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

.row {
  display: flex;
  flex-wrap: wrap;
  margin: 0 -15px;
}

.col,
.col-auto {
  padding: 0 15px;
}

.col {
  flex: 1;
}

.col-auto {
  flex: 0 0 auto;
}

.align-items-center {
  align-items: center;
}

.mb-3 {
  margin-bottom: 1rem;
}

.color-custom-section {
  padding: 1rem 0;
}

.color-item {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
  gap: 1rem;
}

.color-item label {
  min-width: 150px;
  font-weight: 500;
  color: #303133;
}

.color-value {
  color: #909399;
  font-size: 12px;
  margin-left: 0.5rem;
}
</style>

