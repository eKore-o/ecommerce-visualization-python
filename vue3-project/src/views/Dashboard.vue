<template>
  <Layout page-title="主页">
    <!-- Header -->
    <div class="header bg-gradient-primary pb-8 pt-5 pt-md-8">
      <div class="container-fluid">
        <div class="header-body">
          <StatsCards :stats="stats" />
        </div>
      </div>
    </div>
    <div class="container-fluid mt--7">
      <div class="row">
        <div class="col-xl-8 mb-5 mb-xl-0">
          <el-card class="card  shadow" shadow="never">
            <template #header>
              <div class="card-header bg-transparent">
                <div class="row align-items-center">
                  <div class="col">
                    <h2  style="color: black;">近一周登录人数</h2>
                  </div>
                </div>
              </div>
            </template>
            <div class="card-body">
              <div class="chart">
                <div ref="loginChartRef" class="chart-canvas"></div>
              </div>
            </div>
          </el-card>
        </div>
        <div class="col-xl-4">
          <el-card class="card shadow" shadow="never">
            <template #header>
              <div class="card-header bg-transparent">
                <div class="row align-items-center">
                  <div class="col">
                    <h6 class="text-uppercase text-muted ls-1 mb-1">商品统计</h6>
                    <h2 class="mb-0">各品牌商品数量</h2>
                  </div>
                </div>
              </div>
            </template>
            <div class="card-body">
              <div class="chart">
                <div ref="productChartRef" class="chart-canvas"></div>
              </div>
            </div>
          </el-card>
        </div>
      </div>
     
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Layout from '../components/Layout.vue'
import StatsCards from '../components/StatsCards.vue'
import * as echarts from 'echarts'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const stats = ref({
  user_count: 0,
  data_count: 0,
  city_count: 0,
  product_count: 0
})

const loginChartRef = ref(null)
const productChartRef = ref(null)
let loginChart = null
let productChart = null

const loginStats = ref([])
const productGroups = ref([])

const initLoginChart = () => {
  if (!loginChartRef.value) return
  if (!loginChart) {
    loginChart = echarts.init(loginChartRef.value)
  }

  const dates = loginStats.value.map(item => item.date)
  const counts = loginStats.value.map(item => item.count)

  const option = {
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
      data: dates
    },
    yAxis: {
      type: 'value',
      name: '人数'
    },
    series: [
      {
        name: '登录人数',
        type: 'line',
        smooth: true,
        data: counts,
        itemStyle: {
          color: '#5e72e4'
        }
      }
    ]
  }

  loginChart.setOption(option)
}

const initProductChart = () => {
  if (!productChartRef.value) return
  if (!productChart) {
    productChart = echarts.init(productChartRef.value)
  }

  const names = productGroups.value.map(item => item.name)
  const counts = productGroups.value.map(item => item.count)

  const option = {
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
      type: 'value',
      name: '数量'
    },
    yAxis: {
      type: 'category',
      data: names,
      inverse: true
    },
    series: [
      {
        name: '商品数量',
        type: 'bar',
        data: counts,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(1, 0, 0, 0, [
            { offset: 0, color: '#11cdef' },
            { offset: 1, color: '#1171ef' }
          ])
        },
        barWidth: 14
      }
    ]
  }

  productChart.setOption(option)
}

const fetchDashboardData = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/app/dashboard_stats/`)
    const data = await res.json()
    stats.value = data.stats || stats.value
    loginStats.value = data.login_stats || []
    productGroups.value = data.product_groups || []

    initLoginChart()
    initProductChart()
  } catch (e) {
    console.error('获取 Dashboard 数据失败', e)
  }
}

const handleResize = () => {
  loginChart && loginChart.resize()
  productChart && productChart.resize()
}

onMounted(() => {
  fetchDashboardData()
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
  if (loginChart) {
    loginChart.dispose()
    loginChart = null
  }
  if (productChart) {
    productChart.dispose()
    productChart = null
  }
})
</script>

<style scoped>
.bg-gradient-default {
  background: linear-gradient(87deg, #172b4d 0, #1a174d 100%) !important;
}

.chart {
  position: relative;
  height: 300px;
}

.chart-canvas {
  height: 300px !important;
}

.nav-pills .nav-link {
  color: rgba(255, 255, 255, 0.5);
  background-color: transparent;
  border-radius: 0.375rem;
}

.nav-pills .nav-link.active {
  color: #fff;
  background-color: rgba(255, 255, 255, 0.1);
}
</style>

