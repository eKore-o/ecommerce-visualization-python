<template>
  <Layout>
    <div class="clustering-view">
      <div class="header">
        <h2 class="title"><el-icon><DataLine /></el-icon> 商品市场聚类分析</h2>
        <p class="subtitle">基于 K-Means 演算法，自动识别商品的价格-销量分群，洞查市场格局</p>
      </div>

      <el-row :gutter="20">
        <el-col :span="24">
          <el-card class="chart-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>聚类分布散点图 (价格 vs 付款人数)</span>
                <el-button type="primary" :loading="loading" @click="fetchData">刷新数据</el-button>
              </div>
            </template>
            <div ref="chartRef" class="chart-container" v-loading="loading"></div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" class="info-row">
        <el-col v-for="cluster in clusterInfo" :key="cluster.cluster_id" :xs="24" :sm="8">
          <el-card class="cluster-stat-card" shadow="hover">
            <template #header>
              <div class="cluster-header">
                <span class="cluster-dot" :style="{ backgroundColor: getClusterColor(cluster.cluster_id) }"></span>
                <strong>{{ cluster.name }}</strong>
              </div>
            </template>
            <div class="stat-body">
              <div class="stat-item">
                <span class="label">商品规模</span>
                <span class="value">{{ cluster.count }} 件</span>
              </div>
              <div class="stat-item">
                <span class="label">平均价格</span>
                <span class="value">¥ {{ getAverage(cluster.points, 'price') }}</span>
              </div>
              <div class="stat-item">
                <span class="label">平均付款人数</span>
                <span class="value">{{ getAverage(cluster.points, 'pay_count') }} 人</span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import * as echarts from 'echarts'
import { DataLine } from '@element-plus/icons-vue'
import Layout from '../components/Layout.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const chartRef = ref(null)
const loading = ref(false)
const clusterInfo = ref([])
let myChart = null

const clusterColors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#9b59b6']

const getClusterColor = (id) => clusterColors[id % clusterColors.length]

const getAverage = (points, key) => {
  if (!points || points.length === 0) return 0
  const sum = points.reduce((acc, p) => acc + (p[key] || 0), 0)
  return (sum / points.length).toFixed(2)
}

const fetchData = async () => {
  loading.value = true
  try {
    const res = await fetch(`${API_BASE_URL}/app/cluster_analysis/`)
    const data = await res.json()
    if (res.ok) {
      clusterInfo.value = data.clusters
      renderChart(data.clusters)
    }
  } catch (e) {
    console.error('获取聚类数据失败', e)
  } finally {
    loading.value = false
  }
}

const renderChart = (clusters) => {
  if (!chartRef.value) return
  if (!myChart) {
    myChart = echarts.init(chartRef.value)
  }

  const series = clusters.map((cluster, index) => ({
    name: cluster.name,
    type: 'scatter',
    data: cluster.points.map(p => [p.price || 1, p.pay_count || 1, p.title]),
    itemStyle: {
      color: getClusterColor(cluster.cluster_id),
      opacity: 0.7
    },
    symbolSize: (data) => {
      // 优化气泡大小：使用对数缩放，避免销量极高点遮挡全图
      return Math.min(Math.max(Math.log10(data[1] || 1) * 8, 6), 25)
    },
    emphasis: {
      focus: 'series',
      label: {
        show: true,
        formatter: (params) => params.data[2],
        position: 'top',
        color: '#333',
        fontSize: 10
      }
    }
  }))

  const option = {
    title: { show: false },
    tooltip: {
      padding: 10,
      backgroundColor: 'rgba(255, 255, 255, 0.98)',
      borderColor: '#eee',
      borderWidth: 1,
      formatter: (params) => {
        return `
          <div style="font-weight:bold;margin-bottom:5px">${params.data[2]}</div>
          <div style="font-size:12px;color:#666">
            价格: <span style="color:#f56c6c">¥${params.data[0]}</span><br/>
            销量: <span style="color:#409eff">${params.data[1]}</span>
          </div>
        `
      }
    },
    legend: {
      top: 10,
      right: 20
    },
    grid: {
      left: '5%',
      right: '10%',
      bottom: '10%',
      top: '15%',
      containLabel: true
    },
    xAxis: {
      name: '价格 (对数轴/元)',
      type: 'log',
      logBase: 10,
      min: 1,
      splitLine: { lineStyle: { type: 'dashed', color: '#eee' } },
      axisLabel: {
        formatter: (value) => value >= 1000 ? (value / 1000) + 'k' : value
      }
    },
    yAxis: {
      name: '付款人数 (对数轴)',
      type: 'log',
      logBase: 10,
      min: 1,
      splitLine: { lineStyle: { type: 'dashed', color: '#eee' } },
      axisLabel: {
        formatter: (value) => value >= 1000 ? (value / 1000) + 'k' : value
      }
    },
    series: series
  }

  myChart.setOption(option)
}

const handleResize = () => {
  myChart && myChart.resize()
}

onMounted(() => {
  fetchData()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  myChart && myChart.dispose()
})
</script>

<style scoped>
.clustering-view {
  padding: 24px;
  max-width: 1400px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.title {
  font-size: 2.22rem;
  color: #303133;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.subtitle {
  color: #909399;
}

.chart-card {
  border-radius: 12px;
  margin-bottom: 30px;
}

.chart-container {
  height: 500px;
  width: 100%;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-row {
  margin-top: 10px;
}

.cluster-stat-card {
  border-radius: 12px;
  margin-bottom: 20px;
}

.cluster-header {
  display: flex;
  align-items: center;
  gap: 10px;
}

.cluster-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.stat-body {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.stat-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-item .label {
  color: #909399;
  font-size: 0.9rem;
}

.stat-item .value {
  color: #303133;
  font-weight: bold;
}
</style>
