<template>
  <Layout>
    <div class="predict-view">
      <div class="header">
        <h2 class="title"><el-icon><MagicStick /></el-icon>销量预测</h2>
        <p class="subtitle">基于随机森林算法，智能预估淘宝商品潜在销量</p>
      </div>

      <el-row :gutter="20">
        <el-col :xs="24" :md="10">
          <el-card class="form-card" shadow="hover">
            <template #header>
              <div class="card-header">
                <span>商品参数输入</span>
                <div class="card-header-actions">
                  <el-button type="primary" link @click="resetForm">重置</el-button>
                </div>
              </div>
            </template>

            <div class="sample-section">
              <span class="sample-label">快速填充示例:</span>
              <div class="sample-tags">
                <el-tag 
                  v-for="sample in samples" 
                  :key="sample.name" 
                  class="sample-tag" 
                  effect="plain"
                  round
                  @click="fillSample(sample)"
                >
                  {{ sample.name }}
                </el-tag>
              </div>
            </div>

            <el-form :model="form" label-width="100px" label-position="top">
              <el-form-item label="商品标题">
                <el-input v-model="form.title" placeholder="请输入完整商品标题" clearable />
              </el-form-item>
              
              <el-row :gutter="15">
                <el-col :span="12">
                  <el-form-item label="店铺名称">
                    <el-input v-model="form.shop" placeholder="店铺名" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="商品品牌">
                    <el-select v-model="form.product_brand" placeholder="选择或搜索" filterable allow-create clearable style="width: 100%">
                      <el-option v-for="b in options.brands" :key="b" :label="b" :value="b" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="15">
                <el-col :span="12">
                  <el-form-item label="预计售价 (元)">
                    <el-input-number v-model="form.price" :precision="2" :step="10" style="width: 100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="发货地址">
                    <el-select v-model="form.ship_address" placeholder="选择省份" filterable style="width: 100%">
                      <el-option v-for="a in options.addresses" :key="a" :label="a" :value="a" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-form-item label="特点列表 (逗号分隔)">
                <el-input v-model="form.features" type="textarea" placeholder="例: 包邮,正品,厂家直销" rows="2" />
              </el-form-item>

              <el-form-item label="卖点描述">
                <el-input v-model="form.selling_points" type="textarea" placeholder="例: 爆款直降,限时优惠" rows="2" />
              </el-form-item>

              <el-button type="primary" class="predict-btn" :loading="loading" @click="handlePredict">
                立即分析预测
              </el-button>
            </el-form>
          </el-card>
        </el-col>

        <el-col :xs="24" :md="14">
          <el-card class="result-card" shadow="always" v-loading="loading">
            <template #header>
              <span>分析预测报告</span>
            </template>
            <div v-if="predictionResult" class="result-content">
              <div class="prediction-score">
                <div class="score-label">预估付款人数</div>
                <div class="score-value">{{ predictionResult.prediction }} <small>人</small></div>
              </div>
              
              <el-divider />
              
              <div class="info-grid">
                <div class="info-item">
                  <div class="i-label">核心算法</div>
                  <div class="i-value">{{ predictionResult.model_info.algorithm }}</div>
                </div>
                <div class="info-item">
                  <div class="i-label">训练样本规模</div>
                  <div class="i-value">{{ predictionResult.model_info.training_samples }} 条数据</div>
                </div>
                <div class="info-item">
                  <div class="i-label">特征维度</div>
                  <div class="i-value">{{ predictionResult.model_info.features_used.join(', ') }}</div>
                </div>
              </div>

              <div class="disclaimer">
                <el-alert title="算法说明" type="info" :closable="false" show-icon>
                  基于随机森林回归模型综合计算标题长度、特点标签密度及市场品牌溢价得出的预估值，仅供业务参考。
                </el-alert>
              </div>
            </div>
            <div v-else class="empty-state">
              <el-empty description="在左侧输入参数并点击预测按钮开始分析" />
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { MagicStick } from '@element-plus/icons-vue'
import Layout from '../components/Layout.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const form = ref({
  title: '',
  shop: '',
  price: 99.0,
  ship_address: '',
  features: '',
  selling_points: '',
  product_brand: ''
})

const options = ref({
  brands: [],
  addresses: []
})

const samples = [
  {
    name: '华为 Mate 70 Pro',
    data: {
      title: 'HUAWEI Mate 70 Pro 第二代红枫影像 鸿蒙AI 智能手机',
      shop: '华为官方旗舰店',
      price: 6999,
      ship_address: '广东 深圳',
      features: '品牌,刷新率,屏幕尺寸,充电功率,电池容量,机身内存ROM',
      selling_points: '高端旗舰, 5G自研芯片, 极致拍照',
      product_brand: '华为'
    }
  },
  {
    name: '红米 K80',
    data: {
      title: 'Redmi K80 骁龙8s 第四代 性能旗舰 电竞拍照手机',
      shop: '小米官方旗舰店',
      price: 2499,
      ship_address: '北京',
      features: '品牌,分辨率,刷新率,屏幕尺寸,电池容量',
      selling_points: '至高性价比, 游戏玩家首选, 极速响应',
      product_brand: '小米'
    }
  },
  {
    name: '入门备用机',
    data: {
      title: '新款全网通智能手机 大电池大屏幕 老人学生专用备用机',
      shop: '淘宝优质店铺',
      price: 499,
      ship_address: '广东 深圳',
      features: '电池容量,大屏幕,简单好用',
      selling_points: '长续航, 实用之选, 百元机王者',
      product_brand: '其他'
    }
  }
]

const loading = ref(false)
const predictionResult = ref(null)

const loadOptions = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/app/products/filter_options/`)
    const data = await res.json()
    options.value.brands = data.brands || []
    options.value.addresses = data.addresses || []
  } catch (e) {
    console.error('加载选项失败', e)
  }
}

const handlePredict = async () => {
  if (!form.value.title) {
    ElMessage.warning('请输入商品标题')
    return
  }
  
  loading.value = true
  try {
    const res = await fetch(`${API_BASE_URL}/app/predict_pay_count/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form.value)
    })
    const data = await res.json()
    if (res.ok) {
      predictionResult.value = data
      ElMessage.success('预测分析完成')
    } else {
      ElMessage.error(data.message || '分析失败')
    }
  } catch (e) {
    ElMessage.error('网络错误，请稍后再试')
  } finally {
    loading.value = false
  }
}

const resetForm = () => {
  form.value = {
    title: '',
    shop: '',
    price: 99.0,
    ship_address: '',
    features: '',
    selling_points: '',
    product_brand: ''
  }
  predictionResult.value = null
}

const fillSample = (sample) => {
  form.value = { ...sample.data }
  ElMessage.info(`已应用示例: ${sample.name}`)
}

onMounted(() => {
  loadOptions()
})
</script>

<style scoped>
.predict-view {
  padding: 24px;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.title {
  font-size: 2.4rem;
  color: #303133;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.subtitle {
  color: #909399;
  font-size: 1.1rem;
}

.form-card, .result-card {
  border-radius: 12px;
  height: 100%;
}

.sample-section {
  margin-bottom: 20px;
  padding: 12px;
  background: #f8f9fa;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.sample-label {
  font-size: 0.85rem;
  color: #909399;
  white-space: nowrap;
}

.sample-tags {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.sample-tag {
  cursor: pointer;
  transition: all 0.2s;
}

.sample-tag:hover {
  background-color: #409eff;
  color: white;
  border-color: #409eff;
}

.predict-btn {
  width: 100%;
  margin-top: 20px;
  height: 44px;
  font-size: 1.1rem;
}

.prediction-score {
  text-align: center;
  padding: 40px 0;
  background: linear-gradient(135deg, rgba(64, 158, 255, 0.1) 0%, rgba(103, 194, 58, 0.1) 100%);
  border-radius: 16px;
  margin-bottom: 30px;
}

.score-label {
  font-size: 1.2rem;
  color: #606266;
  margin-bottom: 15px;
}

.score-value {
  font-size: 4rem;
  font-weight: 900;
  color: #409eff;
}

.score-value small {
  font-size: 1.5rem;
  font-weight: normal;
  color: #909399;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 24px;
  margin-bottom: 24px;
}

.i-label {
  color: #909399;
  font-size: 0.9rem;
  margin-bottom: 6px;
}

.i-value {
  color: #303133;
  font-weight: bold;
  font-size: 1rem;
}

.disclaimer {
  margin-top: 40px;
}

.empty-state {
  padding: 100px 0;
}
</style>
