<template>
  <div class="big-screen">
    <canvas ref="bgCanvasRef" class="bg-canvas"></canvas>
    <!-- 顶部装饰头部 -->
    <header class="screen-header">
      <div class="header-left">
        <div class="header-decoration"></div>
      </div>
      <div class="header-main" @click="$router.push('/dashboard')">
        <h1 class="title">淘宝数据分析监控大屏</h1>
      </div>
      <div class="header-right">
        <span class="time">{{ currentTime }}</span>
        <span class="status"><span class="dot"></span></span>
      </div>
    </header>
    
    <div class="screen-content main-layout">
      <!-- 左侧栏：3个图表 -->
      <aside class="side-col left-col">
        <div class="panel-box">
          <div class="panel-title">商品销量分析排行</div>
          <div ref="chart1Ref" class="chart-container"></div>
          <div class="panel-corner"></div>
        </div>
        <div class="panel-box">
          <div class="panel-title">TOP店铺销售占比</div>
          <div ref="chart5Ref" class="chart-container"></div>
          <div class="panel-corner"></div>
        </div>
        <div class="panel-box">
          <div class="panel-title">热门搜索关键词</div>
          <div ref="chart3Ref" class="chart-container"></div>
          <div class="panel-corner"></div>
        </div>
      </aside>

      <!-- 中间栏：指标 + 地图 -->
      <main class="center-col">
        <!-- 核心指标行 -->
        <div class="metrics-row">
          <div class="metric-item">
            <div class="m-label">商品总数</div>
            <div class="m-value">{{ totalProducts }} <small>件</small></div>
          </div>
          <div class="metric-item">
            <div class="m-label">店铺总数</div>
            <div class="m-value">{{ totalShops }} <small>家</small></div>
          </div>
          <div class="metric-item">
            <div class="m-label">分析类别</div>
            <div class="m-value">{{ categoryCount }} <small>类</small></div>
          </div>
        </div>
        
        <!-- 大地图区域 -->
        <div class="map-container">
          <div class="map-title">全国地域销量分布图</div>
          <div ref="chart4Ref" class="chart-container center-map"></div>
          <!-- 装饰性元素 -->
          <div class="map-decoration-1"></div>
          <div class="map-decoration-2"></div>
        </div>
      </main>

      <!-- 右侧栏：3个图表 -->
      <aside class="side-col right-col">
        <div class="panel-box">
          <div class="panel-title">商品核心特点分布</div>
          <div ref="chart6Ref" class="chart-container"></div>
          <div class="panel-corner"></div>
        </div>
        <div class="panel-box">
          <div class="panel-title">价格区间明细</div>
          <div ref="chart7Ref" class="chart-container"></div>
          <div class="panel-corner"></div>
        </div>
        <div class="panel-box">
          <div class="panel-title">商品平均价格趋势</div>
          <div ref="chart2Ref" class="chart-container"></div>
          <div class="panel-corner"></div>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

// 实时时间
const currentTime = ref('')
const updateTime = () => {
  const now = new Date()
  currentTime.value = now.toLocaleString()
}
let timeTimer = null

const chart1Ref = ref(null) // 商品销量分析
const chart2Ref = ref(null) // 商品平均价格分析
const chart3Ref = ref(null) // 标题词云
const chart4Ref = ref(null) // 不同发货地址销量
const chart5Ref = ref(null) // 店铺销量分析
const chart6Ref = ref(null) // 商品特点分布
const chart7Ref = ref(null) // 价格区间明细
const bgCanvasRef = ref(null) // 动态背景 Canvas

// 核心指标数据
const totalProducts = ref(0)
const totalShops = ref(0)
const categoryCount = ref(0)

let charts = {}

// 预定义配色方案
const colorPalette = {
  blue: '#5470c6',
  green: '#91cc75',
  purple: '#9a60b4',
  orange: '#fac858',
  red: '#ee6666',
  cyan: '#73c0de',
  violet: '#3ba272',
  pink: '#fc8452',
  teal: '#ea7ccc',
  brown: '#8a2be2'
}

const barColors = [
  '#00d2ff', '#00ffcc', '#00ff5f', '#f9ff45', '#ff9f00',
  '#ff45e3', '#9645ff', '#4560ff', '#00eaff', '#00ff8e'
]

const mapColors = ['#08173d', '#0d35a1', '#1a5cad', '#00d2ff', '#00ffcc']

// 加载词云库 (修复路径：/assets/...)
const loadWordCloud = () => {
  return new Promise((resolve) => {
    if (!window.echarts) {
      window.echarts = echarts
    }
    if (window._wordCloudLoaded) {
      resolve(true)
      return
    }
    const script = document.createElement('script')
    // 兼容用户环境：优先使用 /public 路径，若不成功尝试根路径
    script.src = '/public/assets/js/plugins/chart.js/dist/echarts-wordcloud.min.js'
    script.onload = () => {
      window._wordCloudLoaded = true
      setTimeout(() => resolve(true), 50)
    }
    script.onerror = () => {
      resolve(false)
    }
    document.head.appendChild(script)
  })
}

// 加载中国地图 (修复路径：/assets/...)
const loadChinaMap = () => {
  return new Promise((resolve) => {
    if (!window.echarts) {
      window.echarts = echarts
    }
    if (echarts.getMap && echarts.getMap('china')) {
      resolve(true)
      return
    }
    if (window._chinaMapLoading) {
      const timer = setInterval(() => {
        if (echarts.getMap && echarts.getMap('china')) {
          clearInterval(timer)
          resolve(true)
        }
      }, 100)
      setTimeout(() => {
        clearInterval(timer)
        resolve(!!(echarts.getMap && echarts.getMap('china')))
      }, 3000)
      return
    }

    window._chinaMapLoading = true
    const script = document.createElement('script')
    script.src = '/public/assets/js/plugins/chart.js/dist/china.js'
    script.onload = () => {
      window._chinaMapLoading = false
      setTimeout(() => resolve(!!(echarts.getMap && echarts.getMap('china'))), 50)
    }
    script.onerror = () => {
      window._chinaMapLoading = false
      resolve(false)
    }
    document.head.appendChild(script)
  })
}

// 确保 DOM 元素已经有宽高再初始化
const waitDomReady = (el) => {
  return new Promise((resolve) => {
    let count = 0
    const check = () => {
      // 只要有一点高度就算 ready，避免 0 高度
      if (el && (el.clientWidth > 0 || el.clientHeight > 0)) {
        resolve(true)
      } else if (count > 30) {
        // 超时也尝试初始化，万一 echarts 能自己修正
        console.warn('Chart init timeout, forcing init')
        resolve(true)
      } else {
        count++
        setTimeout(check, 100)
      }
    }
    check()
  })
}

// 加载全量统计数据
const loadTotalStats = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/app/dashboard_stats/`, { credentials: 'include' })
    const data = await res.json()
    if (data.stats) {
      totalProducts.value = data.stats.data_count || 0
      totalShops.value = data.stats.shop_count || 0
      categoryCount.value = data.stats.product_count || 0
    }
  } catch (e) {
    console.error('加载全量统计失败:', e)
  }
}

// 动态背景粒子系统
let animationId = null
const initDynamicBg = () => {
  if (!bgCanvasRef.value) return
  const canvas = bgCanvasRef.value
  const ctx = canvas.getContext('2d')
  let particles = []
  const particleCount = 80
  
  const resize = () => {
    canvas.width = window.innerWidth
    canvas.height = window.innerHeight
  }
  
  class Particle {
    constructor() {
      this.init()
    }
    init() {
      this.x = Math.random() * canvas.width
      this.y = Math.random() * canvas.height
      this.vx = (Math.random() - 0.5) * 0.4
      this.vy = (Math.random() - 0.5) * 0.4
      this.size = Math.random() * 2 + 1
    }
    update() {
      this.x += this.vx
      this.y += this.vy
      if (this.x < 0 || this.x > canvas.width) this.vx *= -1
      if (this.y < 0 || this.y > canvas.height) this.vy *= -1
    }
    draw() {
      ctx.fillStyle = 'rgba(0, 210, 255, 0.4)'
      ctx.beginPath()
      ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2)
      ctx.fill()
    }
  }
  
  const createParticles = () => {
    particles = []
    for (let i = 0; i < particleCount; i++) {
      particles.push(new Particle())
    }
  }
  
  const drawLines = () => {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx = particles[i].x - particles[j].x
        const dy = particles[i].y - particles[j].y
        const dist = Math.sqrt(dx * dx + dy * dy)
        if (dist < 150) {
          ctx.strokeStyle = `rgba(0, 210, 255, ${0.12 * (1 - dist / 150)})`
          ctx.lineWidth = 0.5
          ctx.beginPath()
          ctx.moveTo(particles[i].x, particles[i].y)
          ctx.lineTo(particles[j].x, particles[j].y)
          ctx.stroke()
        }
      }
    }
  }
  
  const animate = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)
    particles.forEach(p => {
      p.update()
      p.draw()
    })
    drawLines()
    animationId = requestAnimationFrame(animate)
  }
  
  window.addEventListener('resize', resize)
  resize()
  createParticles()
  animate()
}

// 自动轮播 Tooltip 逻辑已移除

// 初始化所有图表
const initAllCharts = async () => {
  await nextTick()
  initDynamicBg() // 启动动态粒子背景
  loadTotalStats() // 加载全量指标
  // 给一点时间让 CSS 渲染完成
  setTimeout(async () => {
    const refs = [chart1Ref, chart2Ref, chart3Ref, chart4Ref, chart5Ref, chart6Ref, chart7Ref]
    const inits = [initChart1, initChart2, initChart3, initChart4, initChart5, initChart6, initChart7]
    
    for (let i = 0; i < refs.length; i++) {
      if (refs[i].value) {
        const ready = await waitDomReady(refs[i].value)
        if (ready) await inits[i]()
      }
    }
  }, 300)
}

// 图表1：商品销量分析
const initChart1 = async () => {
  if (!chart1Ref.value) return
  
  try {
    const res = await fetch(`${API_BASE_URL}/app/part1/data/`, { credentials: 'include' })
    const data = await res.json()
    const chartData = (data.data || []).map(item => ({
      name: item.name || '',
      value: typeof item.value === 'number' ? item.value : parseFloat(item.value) || 0
    })).filter(item => item.name && item.value > 0)
    
    if (charts.chart1) charts.chart1.dispose()
    charts.chart1 = echarts.init(chart1Ref.value)
    
    const sortedData = [...chartData].sort((a, b) => b.value - a.value).slice(0, 10)
    charts.chart1.setOption({
      tooltip: { 
        trigger: 'axis',
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        borderColor: '#00d2ff',
        borderWidth: 1,
        textStyle: { color: '#fff' },
        formatter: '{b}: {c}'
      },
      grid: { 
        left: '5%', 
        right: '5%', 
        bottom: '5%',
        top: '15%',
        containLabel: true 
      },
      xAxis: { 
        type: 'category', 
        data: sortedData.map(item => item.name), 
        axisLine: { lineStyle: { color: '#1a5cad' } },
        axisLabel: { 
          rotate: 45, 
          interval: 0,
          color: '#5fb4fa'
        },
        axisTick: { alignWithLabel: true }
      },
      yAxis: { 
        type: 'value', 
        name: '销量',
        nameTextStyle: { color: '#5fb4fa' },
        axisLine: { lineStyle: { color: '#1a5cad' } },
        axisLabel: { color: '#5fb4fa' },
        splitLine: { lineStyle: { color: 'rgba(26, 92, 173, 0.2)', type: 'dashed' } }
      },
      series: [{
        name: '销量',
        type: 'bar',
        data: sortedData.map(item => item.value),
        animationDuration: 2000,
        animationEasing: 'cubicOut',
        itemStyle: { 
          color: barColors[0],
          borderRadius: [4, 4, 0, 0]
        },
        label: {
          show: false
        }
      }]
    })
  } catch (e) {
    console.error('加载商品销量分析失败:', e)
  }
}

// 图表2：商品平均价格分析
const initChart2 = async () => {
  if (!chart2Ref.value) return
  
  try {
    const res = await fetch(`${API_BASE_URL}/app/part7/data/`, { credentials: 'include' })
    const data = await res.json()
    const chartData = (data.data || []).map(item => ({
      name: item.name || '',
      value: typeof item.value === 'number' ? item.value : parseFloat(item.value) || 0
    })).filter(item => item.name && item.value > 0)
    
    if (charts.chart2) charts.chart2.dispose()
    charts.chart2 = echarts.init(chart2Ref.value)
    
    const sortedData = [...chartData].sort((a, b) => b.value - a.value).slice(0, 10)
    charts.chart2.setOption({
      tooltip: { 
        trigger: 'axis',
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        borderColor: '#00d2ff',
        borderWidth: 1,
        textStyle: { color: '#fff' },
        formatter: '{b}: ¥{c}'
      },
      grid: { 
        left: '5%', 
        right: '8%', 
        bottom: '5%',
        top: '15%',
        containLabel: true 
      },
      xAxis: { 
        type: 'value', 
        name: '平均价格(元)',
        nameTextStyle: { color: '#5fb4fa' },
        axisLine: { lineStyle: { color: '#1a5cad' } },
        axisLabel: { color: '#5fb4fa' },
        splitLine: { lineStyle: { color: 'rgba(26, 92, 173, 0.2)', type: 'dashed' } }
      },
      yAxis: { 
        type: 'category', 
        data: sortedData.map(item => item.name), 
        axisLine: { lineStyle: { color: '#1a5cad' } },
        axisLabel: { 
          interval: 0,
          color: '#5fb4fa'
        },
        axisTick: { alignWithLabel: true }
      },
      series: [{
        name: '平均价格',
        type: 'bar',
        data: sortedData.map(item => item.value),
        animationDuration: 2000,
        animationEasing: 'cubicOut',
        itemStyle: { 
          color: barColors[1],
          borderRadius: [0, 4, 4, 0]
        },
        label: {
          show: false
        }
      }]
    })
  } catch (e) {
    console.error('加载商品平均价格分析失败:', e)
  }
}

// 图表3：标题词云
const initChart3 = async () => {
  if (!chart3Ref.value) return
  
  const loaded = await loadWordCloud()
  if (!loaded) return
  
  try {
    const res = await fetch(`${API_BASE_URL}/app/part6/data/`, { credentials: 'include' })
    const data = await res.json()
    const chartData = (data.data || []).map(item => ({
      name: item.name || '',
      value: typeof item.value === 'number' ? item.value : parseInt(item.value) || 0
    })).filter(item => item.name && item.value > 0)
    
    if (charts.chart3) charts.chart3.dispose()
    charts.chart3 = echarts.init(chart3Ref.value)
    
    charts.chart3.setOption({
      tooltip: { 
        trigger: 'item', 
        formatter: '{b}: {c}',
        backgroundColor: 'rgba(10, 30, 65, 0.9)',
        borderColor: '#1a5cad',
        borderWidth: 1,
        textStyle: { color: '#fff' }
      },
      series: [{
        type: 'wordCloud',
        gridSize: 8,
        sizeRange: [14, 50],
        rotationRange: [0, 0],
        shape: 'circle',
        width: '100%',
        height: '100%',
        drawOutOfBound: false,
        textStyle: {
          fontFamily: 'Microsoft YaHei',
          fontWeight: 'bold',
          color: function() {
            return barColors[Math.floor(Math.random() * barColors.length)]
          }
        },
        emphasis: {
          focus: 'self',
          textStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0, 0, 0, 0.3)'
          }
        },
        data: chartData.slice(0, 50)
      }]
    })
  } catch (e) {
    console.error('加载标题词云失败:', e)
  }
}

// 图表4：不同发货地址销量
const initChart4 = async () => {
  if (!chart4Ref.value) return
  
  try {
    const mapLoaded = await loadChinaMap()
    if (!mapLoaded) {
      console.error('中国地图加载失败')
      return
    }

    const res = await fetch(`${API_BASE_URL}/app/part2/data/`, { credentials: 'include' })
    const data = await res.json()
    console.log(data)
    const chartData = (data.data || []).map(item => ({
      name: item.name || '',
      value: typeof item.value === 'number' ? item.value : parseFloat(item.value) || 0
    })).filter(item => item.name && item.value > 0)
    
    if (charts.chart4) charts.chart4.dispose()
    charts.chart4 = echarts.init(chart4Ref.value)
    
    charts.chart4.setOption({
      tooltip: {
        trigger: 'item',
        backgroundColor: 'rgba(10, 30, 65, 0.9)',
        borderColor: '#1a5cad',
        borderWidth: 1,
        textStyle: { color: '#fff' },
        formatter: function(params) {
          const val = params.value;
          const status = isNaN(val) ? '暂无数据' : `¥${Math.floor(val)}`;
          return `${params.name}<br/>销售额: ${status}`;
        }
      },
      visualMap: {
        min: 0,
        max: Math.max(...chartData.map(item => item.value), 1),
        left: '2%',
        bottom: '2%',
        text: ['高', '低'],
        textStyle: { color: '#5fb4fa' },
        calculable: true,
        inRange: {
          color: mapColors
        }
      },
      series: [
        {
          name: '销售额',
          type: 'map',
          map: 'china',
          animationDuration: 2000,
          animationEasing: 'cubicOut',
          roam: false,
          zoom: 1.2,
          layoutCenter: ['50%', '50%'],
          layoutSize: '100%',
          label: {
            show: true,
            fontSize: 10,
            color: '#fff'
          },
          itemStyle: {
            areaColor: '#091632',
            borderColor: '#1e5a9a',
            borderWidth: 1.2,
            shadowColor: 'rgba(0, 210, 255, 0.2)',
            shadowBlur: 10
          },
          emphasis: {
            label: { 
              show: true,
              color: '#fff',
              fontWeight: 'bold'
            },
            itemStyle: {
              areaColor: barColors[0],
              borderColor: barColors[0]
            }
          },
          data: chartData
        }
      ]
    })
  } catch (e) {
    console.error('加载不同发货地址销量失败:', e)
  }
}

// 图表5：店铺销量分析
const initChart5 = async () => {
  if (!chart5Ref.value) return
  
  try {
    const res = await fetch(`${API_BASE_URL}/app/part3/data/`, { credentials: 'include' })
    const data = await res.json()
    const chartData = (data.data || []).map(item => ({
      name: item.name || '',
      value: typeof item.value === 'number' ? item.value : parseFloat(item.value) || 0
    })).filter(item => item.name && item.value > 0)
    
    if (charts.chart5) charts.chart5.dispose()
    charts.chart5 = echarts.init(chart5Ref.value)
    
    const sortedData = [...chartData].sort((a, b) => b.value - a.value).slice(0, 8)
    charts.chart5.setOption({
      tooltip: { 
        trigger: 'item', 
        backgroundColor: 'rgba(0, 0, 0, 0.85)',
        borderColor: '#00d2ff',
        borderWidth: 1,
        textStyle: { color: '#fff' },
        formatter: '{a} <br/>{b}: {c} ({d}%)' 
      },
      legend: { 
        orient: 'horizontal', 
        bottom: '0%',
        left: 'center',
        textStyle: { color: '#5fb4fa', fontSize: 10 },
        itemWidth: 10,
        itemHeight: 10,
        data: sortedData.map(item => item.name) 
      },
      series: [{
        name: '销量',
        type: 'pie',
        radius: ['35%', '60%'],
        center: ['50%', '45%'],
        animationDuration: 2000,
        animationEasing: 'cubicOut',
        avoidLabelOverlap: true,
        itemStyle: { 
          borderRadius: 4, 
          borderColor: 'rgba(10, 30, 65, 0.8)', 
          borderWidth: 1 
        },
        label: { 
          show: true, 
          position: 'outside',
          formatter: '{b}',
          color: '#fff',
          fontSize: 10
        },
        labelLine: {
          show: true,
          length: 5,
          length2: 5
        },
        data: sortedData.map((item, index) => ({ 
          value: item.value, 
          name: item.name,
          itemStyle: {
            color: barColors[index % barColors.length]
          }
        }))
      }]
    })
  } catch (e) {
    console.error('加载店铺销量分析失败:', e)
  }
}

// 图表6：商品特点分布
const initChart6 = async () => {
  if (!chart6Ref.value) return
  
  try {
    const res = await fetch(`${API_BASE_URL}/app/part5/data/`, { credentials: 'include' })
    const data = await res.json()
    const treeData = data.data || []
    
    if (charts.chart6) charts.chart6.dispose()
    charts.chart6 = echarts.init(chart6Ref.value)
    
    charts.chart6.setOption({
      tooltip: {
        backgroundColor: 'rgba(10, 30, 65, 0.9)',
        borderColor: '#00d2ff',
        borderWidth: 1,
        textStyle: { color: '#fff' },
        formatter: function (info) {
          const value = info.value
          const name = info.name
          return [
            '<div style="font-weight: bold; color: #00d2ff;">' + echarts.format.encodeHTML(name) + '</div>',
            '出现频次: ' + echarts.format.addCommas(value)
          ].join('')
        }
      },
      series: [{
        name: '商品特点分布',
        type: 'treemap',
        visibleMin: 300,
        roam: false,
        backgroundColor: 'transparent',
        nodeClick: false,
        label: { 
          show: true, 
          formatter: '{b}',
          color: '#fff',
          fontWeight: 'bold',
          fontSize: 12
        },
        itemStyle: { 
          borderColor: 'rgba(2, 9, 20, 0.5)',
          borderWidth: 1,
          gapWidth: 1
        },
        levels: [
          {
            itemStyle: {
              borderWidth: 1,
              gapWidth: 2
            }
          }
        ],
        data: treeData,
        animationDuration: 2000,
        animationEasing: 'cubicOut',
        color: barColors
      }]
    })
  } catch (e) {
    console.error('加载商品特点分布失败:', e)
  }
}

// 图表7：价格区间明细
const initChart7 = async () => {
  if (!chart7Ref.value) return
  
  try {
    const res = await fetch(`${API_BASE_URL}/app/part4/data/`, { credentials: 'include' })
    const data = await res.json()
    const chartData = (data.data || []).map(item => ({
      name: item.name || '',
      value: typeof item.value === 'number' ? item.value : parseInt(item.value) || 0
    })).filter(item => item.name && item.value > 0)
    
    if (charts.chart7) charts.chart7.dispose()
    charts.chart7 = echarts.init(chart7Ref.value)
    
    const sortedData = [...chartData].sort((a, b) => b.value - a.value)
    charts.chart7.setOption({
      tooltip: { 
        trigger: 'item',
        backgroundColor: 'rgba(10, 30, 65, 0.9)',
        borderColor: '#00d2ff',
        borderWidth: 1,
        textStyle: { color: '#fff' },
        formatter: '{b}<br/>占比: {c}'
      },
      series: [{
        name: '商品数量',
        type: 'funnel',
        left: '5%',
        top: '10%',
        bottom: '5%',
        width: '90%',
        min: 0,
        max: Math.max(...sortedData.map(d => d.value), 1),
        minSize: '0%',
        maxSize: '100%',
        sort: 'descending',
        gap: 4,
        label: {
          show: true,
          position: 'inside',
          formatter: '{b}: {c}',
          color: '#fff',
          fontWeight: 'bold'
        },
        labelLine: { show: false },
        itemStyle: {
          borderColor: '#fff',
          borderWidth: 1
        },
        animationDuration: 2000,
        animationEasing: 'cubicOut',
        data: sortedData.map((item, index) => ({
          value: item.value,
          name: item.name,
          itemStyle: {
            color: barColors[index % barColors.length]
          }
        }))
      }]
    })
  } catch (e) {
    console.error('加载价格区间明细失败:', e)
  }
}

// 窗口大小变化时调整图表
const handleResize = () => {
  Object.values(charts).forEach(chart => {
    if (chart) chart.resize()
  })
}

onMounted(() => {
  initAllCharts()
  updateTime()
  timeTimer = setInterval(updateTime, 1000)
  window.addEventListener('resize', handleResize)
})

onBeforeUnmount(() => {
  if (timeTimer) clearInterval(timeTimer)
  if (animationId) cancelAnimationFrame(animationId)
  window.removeEventListener('resize', handleResize)
  Object.values(charts).forEach(chart => {
    if (chart) chart.dispose()
  })
  charts = {}
})
</script>

<style scoped>
/* 基础容器 */
.big-screen {
  position: relative;
  background: #020914;
  height: 100vh;
  width: 100vw;
  padding: 0;
  margin: 0;
  color: #fff;
  font-family: "Microsoft YaHei", sans-serif;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.bg-canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}

.big-screen::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(rgba(18, 16, 16, 0) 0%, rgba(0, 210, 255, 0.02) 50%, rgba(18, 16, 16, 0) 100%);
  background-size: 100% 200%;
  animation: scan 8s linear infinite;
  z-index: 100;
  pointer-events: none;
}

@keyframes scan {
  0% { background-position: 0 -100%; }
  100% { background-position: 0 100%; }
}

/* 顶部头部 */
.screen-header {
  height: 80px;
  width: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 40px;
  background: linear-gradient(to bottom, rgba(10, 30, 65, 0.8) 0%, transparent 100%);
  position: relative;
  z-index: 10;
}

.header-main {
  text-align: center;
  flex: 1;
  cursor: pointer;
}

.header-main .title {
  font-size: 2.2rem;
  letter-spacing: 4px;
  margin: 0;
  color: #00d2ff;
  font-weight: 900;
  text-shadow: 0 0 15px rgba(0, 210, 255, 0.8);
}

.header-main .sub-title {
  font-size: 0.8rem;
  color: rgba(0, 210, 255, 0.6);
  letter-spacing: 2px;
  margin-top: 5px;
}

.header-left, .header-right {
  width: 350px;
  color: #00d2ff;
}

.header-right {
  display: flex;
  justify-content: flex-end;
  gap: 20px;
  align-items: center;
}

.header-decoration {
  width: 100%;
  height: 2px;
  background: linear-gradient(90deg, #00d2ff, transparent);
  position: relative;
}

/* 三栏布局 */
.main-layout {
  flex: 1;
  display: flex;
  padding: 10px 20px;
  gap: 20px;
  box-sizing: border-box;
}

.side-col {
  width: 25%;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.center-col {
  width: 50%;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

/* 面板样式 */
.panel-box {
  flex: 1;
  background: rgba(6, 30, 93, 0.2);
  border: 1px solid rgba(0, 210, 255, 0.3);
  position: relative;
  display: flex;
  flex-direction: column;
  padding: 10px;
  box-shadow: inset 0 0 15px rgba(0, 210, 255, 0.1);
}

.panel-title {
  font-size: 1rem;
  color: #00d2ff;
  border-left: 4px solid #00d2ff;
  padding-left: 10px;
  margin-bottom: 10px;
  font-weight: bold;
}

.chart-container {
  flex: 1;
  width: 100%;
}

/* 中间栏指标 */
.metrics-row {
  display: flex;
  justify-content: space-around;
  padding: 15px;
  border: 1px dashed rgba(0, 210, 255, 0.3);
  background: rgba(10, 30, 65, 0.2);
}

.metric-item {
  text-align: center;
}

.m-label {
  font-size: 0.8rem;
  color: rgba(0, 210, 255, 0.7);
  margin-bottom: 5px;
}

.m-value {
  font-size: 1.5rem;
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
  color: #fff;
}

.m-value.highlight {
  color: #f9ff45;
  text-shadow: 0 0 10px rgba(249, 255, 69, 0.5);
}

.m-value small {
  font-size: 0.7rem;
  font-weight: normal;
  margin-left: 2px;
}

/* 地图区域 */
.map-container {
  flex: 1;
  position: relative;
  display: flex;
  flex-direction: column;
  border: 1px solid rgba(0, 210, 255, 0.2);
  background: rgba(10, 30, 65, 0.1);
  overflow: hidden;
}

.center-map {
  flex: 1;
  width: 100%;
  height: 100%;
}

.map-title {
  text-align: center;
  padding: 10px;
  font-size: 1.1rem;
  color: #00d2ff;
  letter-spacing: 2px;
}

/* 地图容器内的装饰动画元素 */
.map-decoration-1, .map-decoration-2 {
  position: absolute;
  border-radius: 50%;
  border: 1px solid rgba(0, 210, 255, 0.4);
  pointer-events: none;
}

.map-decoration-1 {
  width: 200px;
  height: 200px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-width: 2px;
  box-shadow: 0 0 20px rgba(0, 210, 255, 0.2);
  animation: pulse 4s ease-in-out infinite;
}

.map-decoration-2 {
  width: 150px;
  height: 150px;
  top: 20%;
  left: 10%;
  opacity: 0.3;
  border-style: dashed;
  animation: rotate 20s linear infinite;
}

@keyframes pulse {
  0% { transform: translate(-50%, -50%) scale(0.95); opacity: 0.3; }
  50% { transform: translate(-50%, -50%) scale(1.05); opacity: 0.6; }
  100% { transform: translate(-50%, -50%) scale(0.95); opacity: 0.3; }
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 装饰角 */
.panel-corner::before, .panel-corner::after,
.panel-box::before, .panel-box::after {
  content: "";
  position: absolute;
  width: 15px;
  height: 15px;
  border-color: #00d2ff;
  border-style: solid;
  pointer-events: none;
}

.panel-box::before { top: -1px; left: -1px; border-width: 2px 0 0 2px; }
.panel-box::after { top: -1px; right: -1px; border-width: 2px 2px 0 0; }
.panel-corner::before { bottom: -1px; left: -1px; border-width: 0 0 2px 2px; }
.panel-corner::after { bottom: -1px; right: -1px; border-width: 0 2px 2px 0; }

.dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  background: #00ffcc;
  border-radius: 50%;
  box-shadow: 0 0 10px #00ffcc;
  margin-left: 10px;
}
</style>