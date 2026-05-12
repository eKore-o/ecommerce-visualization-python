<template>
  <Layout page-title="城市销量分析">
    <div class="container-fluid mt-4">
      <!-- 筛选和导出区域 -->
      <el-card class="mb-4" shadow="never">
        <div class="filter-export-section">
          <div class="row align-items-center mb-3">
            <div class="col-auto">
              <label class="filter-label">城市筛选：</label>
            </div>
            <div class="col">
              <el-select
                v-model="selectedNames"
                multiple
                placeholder="请选择城市（不选则显示全部）"
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
                <el-option label="中国地图" value="map" />
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
            <h3 class="mb-0">城市销量分析</h3>
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

    <!-- 颜色自定义对话框 -->
    <el-dialog
      v-model="showColorDialog"
      title="自定义图表颜色"
      width="600px"
    >
      <div class="color-custom-section">
        <div v-if="chartType === 'map'" class="color-item">
          <label>地图颜色（起始）：</label>
          <el-color-picker v-model="customColors.mapStart" />
          <span class="color-value">{{ customColors.mapStart }}</span>
        </div>
        <div v-if="chartType === 'map'" class="color-item">
          <label>地图颜色（结束）：</label>
          <el-color-picker v-model="customColors.mapEnd" />
          <span class="color-value">{{ customColors.mapEnd }}</span>
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
  </Layout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
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
const chartType = ref('map') // 默认地图

const chartRef = ref(null)
let chart = null
const showColorDialog = ref(false)

// 自定义颜色配置
const customColors = ref({
  mapStart: '#e0f3ff',
  mapEnd: '#0066cc',
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
  mapStart: '#e0f3ff',
  mapEnd: '#0066cc',
  barStart: '#83bff6',
  barMiddle: '#188df0',
  barEnd: '#188df0',
  pieScheme: 'default',
  lineColor: '#5e72e4',
  lineAreaStart: 'rgba(94, 114, 228, 0.3)',
  lineAreaEnd: 'rgba(94, 114, 228, 0.1)'
}

// 饼图颜色方案
const pieColorSchemes = {
  default: ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4', '#ea7ccc'],
  blue: ['#1e3a8a', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'],
  green: ['#065f46', '#10b981', '#34d399', '#6ee7b7', '#d1fae5'],
  red: ['#991b1b', '#ef4444', '#f87171', '#fca5a5', '#fee2e2'],
  purple: ['#581c87', '#9333ea', '#a855f7', '#c084fc', '#e9d5ff']
}

// 加载地图数据
const loadChinaMap = async () => {
  // 方法1: 使用动态 script 标签加载本地文件
  return new Promise((resolve) => {
    // 检查是否已经注册
    if (echarts.getMap('china')) {
      resolve(true)
      return
    }
    
    // 创建 script 标签加载本地文件
    const script = document.createElement('script')
    script.src = '/public/assets/js/plugins/chart.js/dist/china.js'
    script.onload = () => {
      // 等待一下确保脚本执行完成
      setTimeout(() => {
        if (echarts.getMap('china')) {
          resolve(true)
        } else {
          // 如果 script 标签加载失败，尝试从 CDN 加载
          loadFromCDN().then(resolve)
        }
      }, 100)
    }
    script.onerror = () => {
      // 如果本地加载失败，尝试从 CDN 加载
      loadFromCDN().then(resolve)
    }
    document.head.appendChild(script)
  })
}

// 从 CDN 加载地图数据
const loadFromCDN = async () => {
  try {
    const response = await fetch('https://geo.datav.aliyun.com/areas_v3/bound/100000_full.json')
    if (response.ok) {
      const chinaJson = await response.json()
      echarts.registerMap('china', chinaJson)
      return true
    }
  } catch (e) {
    console.error('加载CDN地图数据失败:', e)
  }
  
  ElMessage.warning('地图数据加载失败，将使用简化地图')
  return false
}

// 测试假数据（使用完整名称）
const getMockData = () => {
  return [
    { name: '北京市', value: 1157830 },
    { name: '天津市', value: 822242 },
    { name: '河北省', value: 819811 },
    { name: '山西省', value: 274143 },
    { name: '内蒙古自治区', value: 110000 },
    { name: '辽宁省', value: 100091 },
    { name: '吉林省', value: 1000 },
    { name: '黑龙江省', value: 10100 },
    { name: '上海市', value: 4599080 },
    { name: '江苏省', value: 3278630 },
    { name: '浙江省', value: 6708000 },
    { name: '安徽省', value: 8186150 },
    { name: '福建省', value: 5115990 },
    { name: '江西省', value: 756411 },
    { name: '山东省', value: 1481400 },
    { name: '河南省', value: 9350850 },
    { name: '湖北省', value: 3905760 },
    { name: '湖南省', value: 9640160 },
    { name: '广东省', value: 5123820 },
    { name: '广西壮族自治区', value: 56936 },
    { name: '海南省', value: 0 },
    { name: '重庆市', value: 1267060 },
    { name: '四川省', value: 981241 },
    { name: '贵州省', value: 297686 },
    { name: '云南省', value: 540000 },
    { name: '西藏自治区', value: 0 },
    { name: '陕西省', value: 63133 },
    { name: '甘肃省', value: 0 },
    { name: '青海省', value: 0 },
    { name: '宁夏回族自治区', value: 0 },
    { name: '新疆维吾尔自治区', value: 0 },
    { name: '台湾省', value: 0 },
    { name: '香港特别行政区', value: 101 },
    { name: '澳门特别行政区', value: 0 }
  ]
}

// 加载数据
const loadData = async (filtered = false) => {
  loading.value = true
  try {
    let url = `${API_BASE_URL}/app/part2/data/`
    if (filtered && selectedNames.value.length > 0) {
      const params = new URLSearchParams()
      selectedNames.value.forEach(name => {
        params.append('names', name)
      })
      url = `${API_BASE_URL}/app/part2/filtered/?${params.toString()}`
    }
    
    const res = await fetch(url, {
      credentials: 'include'
    })
    
    if (!res.ok) {
      const errorData = await res.json().catch(() => ({ message: '获取数据失败' }))
      throw new Error(errorData.message || '获取数据失败')
    }
    
    const data = await res.json()
    
    // 处理数据，确保格式为 {name:xx, value:xx} 的列表
    // 后端已经返回完整名称（如"河南省"），直接使用
    chartData.value = (data.data || []).map(item => {
      // 确保 value 是数字类型
      const value = typeof item.value === 'number' ? item.value : parseFloat(item.value) || 0
      // 确保 name 是字符串（完整名称）
      const name = String(item.name || '').trim()
      
      return {
        name: name, // 完整名称，用于地图匹配和显示
        value: value
      }
    }).filter(item => item.name && item.value > 0) // 过滤掉无效数据
    
    if (!filtered) {
      names.value = data.names || []
    }
    
    console.log('加载的数据:', {
      chartData: chartData.value,
      names: names.value,
      dataFormat: chartData.value.map(item => ({ name: item.name, value: item.value }))
    })
    
    // 等待DOM更新后再初始化图表
    await nextTick()
    setTimeout(() => {
      initChart()
    }, 200)
  } catch (e) {
    ElMessage.error(e.message || '加载数据失败')
    console.error('加载数据错误:', e)
    chartData.value = []
  } finally {
    loading.value = false
  }
}

// 初始化图表
const initChart = async () => {
  if (!chartRef.value || chartData.value.length === 0) {
    console.log('图表容器不存在或数据为空', {
      hasRef: !!chartRef.value,
      dataLength: chartData.value.length
    })
    return
  }
  
  // 如果是地图类型，先加载地图数据
  if (chartType.value === 'map') {
    await loadChinaMap()
  }
  
  // 如果图表已存在，先销毁
  if (chart) {
    chart.dispose()
    chart = null
  }
  
  // 初始化图表
  chart = echarts.init(chartRef.value)
  
  // 根据图表类型设置不同的配置
  let option = {}
  
  if (chartType.value === 'map') {
    // 准备地图数据，确保格式为 {name: string, value: number} 的数组
    // 后端已经返回完整名称（如"河南省"），直接使用
    const mapData = chartData.value.map(item => {
      return {
        name: String(item.name || '').trim(),
        value: typeof item.value === 'number' ? item.value : parseFloat(item.value) || 0
      }
    }).filter(item => item.name && item.value >= 0)
    
    console.log('地图数据格式:', mapData)
    
    // 中国地图配置
    option = {
      tooltip: {
        trigger: 'item',
        formatter: function(params) {
          if (params.data) {
            return `${params.name}<br/>销售额: ${params.value}`
          }
          return params.name
        }
      },
      visualMap: {
        min: 0,
        max: Math.max(...chartData.value.map(item => item.value), 1),
        left: 'left',
        top: 'bottom',
        text: ['高', '低'],
        calculable: true,
        inRange: {
          color: [customColors.value.mapStart, customColors.value.mapEnd]
        }
      },
      series: [
        {
          name: '销售额',
          type: 'map',
          map: 'china',
          roam: false,
          label: {
            show: true,
            fontSize: 10
          },
          emphasis: {
            label: {
              show: true
            }
          },
          data: mapData
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
        name: '销售额'
      },
      series: [
        {
          name: '销售额',
          type: 'bar',
          data: sortedData.map(item => item.value),
          itemStyle: {
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: customColors.value.barStart },
              { offset: 0.5, color: customColors.value.barMiddle },
              { offset: 1, color: customColors.value.barEnd }
            ])
          },
          emphasis: {
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: customColors.value.barStart },
                { offset: 0.7, color: customColors.value.barMiddle },
                { offset: 1, color: customColors.value.barEnd }
              ])
            }
          }
        }
      ]
    }
  } else if (chartType.value === 'pie') {
    // 饼图配置
    const sortedData = [...chartData.value].sort((a, b) => b.value - a.value).slice(0, 20) // 只显示前20个
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
          name: '销售额',
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
          emphasis: {
            label: {
              show: true,
              fontSize: '16',
              fontWeight: 'bold'
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
        name: '销售额'
      },
      series: [
        {
          name: '销售额',
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
  
  // 确保图表正确渲染
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

// 导出数据
const handleExport = async (type) => {
  exporting.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/app/part2/export/`, {
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
    
    // 下载文件
    const blob = await response.blob()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    
    const contentDisposition = response.headers.get('Content-Disposition')
    let filename = `城市销售额分析_${new Date().getTime()}`
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
  white-space: nowrap;
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
