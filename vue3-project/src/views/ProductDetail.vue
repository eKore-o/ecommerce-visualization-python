<template>
  <Layout page-title="商品详情">
    <div class="container-fluid mt-4">
      <el-card v-if="loading" class="text-center py-5" shadow="never">
        <el-icon class="is-loading" size="32"><Loading /></el-icon>
        <p>加载中...</p>
      </el-card>

      <el-card v-else-if="!product" class="text-center py-5" shadow="never">
        <el-result icon="warning" title="未找到商品" sub-title="该商品可能已被删除或路径不正确">
          <template #extra>
            <el-button type="primary" @click="$router.push('/tables')">返回列表</el-button>
          </template>
        </el-result>
      </el-card>

      <div v-else class="detail-container">
        <!-- 面包屑导航 -->
        <el-breadcrumb separator="/" class="custom-breadcrumb mb-4">
          <el-breadcrumb-item :to="{ path: '/dashboard' }">
            <el-icon class="mr-1"><HomeFilled /></el-icon>首页
          </el-breadcrumb-item>
          <el-breadcrumb-item :to="{ path: '/tables' }">商品数据</el-breadcrumb-item>
          <el-breadcrumb-item>商品详情</el-breadcrumb-item>
        </el-breadcrumb>

        <div class="row">
          <!-- 左侧：图片 -->
          <div class="col-md-5">
            <el-card class="image-card" :body-style="{ padding: '0px' }" shadow="never">
              <img
                :src="product.image_url || '/assets/img/theme/bootstrap.jpg'"
                class="detail-image"
                @error="handleImageError"
              />
            </el-card>
          </div>

          <!-- 右侧：基本信息 -->
          <div class="col-md-7">
            <div class="info-content">
              <h1 class="product-title">{{ product.title }}</h1>
              
              <div class="price-section mb-4">
                <span class="price-label">价格：</span>
                <span class="price-value">¥{{ product.price }}</span>
              </div>

              <div class="other-info mb-4">
                <p><strong>店铺：</strong> <span class="text-primary">{{ product.shop }}</span></p>
                <p><strong>销量：</strong> {{ product.pay_count }} 件</p>
                <p><strong>发货地：</strong> {{ product.ship_address }}</p>
                <p><strong>分类/品牌：</strong> {{ product.product_brand }}</p>
              </div>

              <div class="action-buttons mb-4">
                <el-button type="danger" size="large" @click="goExternal(product.detail_url)">
                  <el-icon class="mr-2"><ShoppingCart /></el-icon>
                  前往淘宝购买
                </el-button>
                <el-button type="default" size="large" @click="$router.back()">返回</el-button>
              </div>

              <el-divider v-if="product.selling_points">商品亮点</el-divider>
              <div v-if="product.selling_points" class="selling-points-box">
                {{ product.selling_points }}
              </div>
            </div>
          </div>
        </div>

        <!-- 下方：详细信息/特点 -->
        <div class="row mt-4">
          <div class="col-12">
            <el-card class="features-card" shadow="never">
              <template #header>
                <div class="card-header">
                  <span>商品特点</span>
                </div>
              </template>
              <div class="features-list">
                <template v-if="product.features">
                  <el-tag
                    v-for="(feature, index) in product.features.split(' ')"
                    :key="index"
                    class="m-1"
                    type="info"
                  >
                    {{ feature }}
                  </el-tag>
                </template>
                <p v-else class="text-muted">暂无特点信息</p>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Loading, ShoppingCart, HomeFilled } from '@element-plus/icons-vue'
import Layout from '../components/Layout.vue'

const route = useRoute()
const router = useRouter()
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const product = ref(null)
const loading = ref(true)

const loadDetail = async () => {
  const id = route.params.id
  loading.value = true
  try {
    const res = await fetch(`${API_BASE_URL}/app/products/detail/${id}/`)
    if (!res.ok) throw new Error('获取失败')
    const data = await res.json()
    product.value = data.data
  } catch (e) {
    ElMessage.error('加载商品详情失败')
    console.error(e)
  } finally {
    loading.value = false
  }
}

const handleImageError = (e) => {
  e.target.src = '/assets/img/theme/bootstrap.jpg'
}

const goExternal = (url) => {
  if (url) {
    window.open(url, '_blank')
  } else {
    ElMessage.warning('暂无外部购买链接')
  }
}

onMounted(() => {
  loadDetail()
})
</script>

<style scoped>
.detail-container {
  max-width: 1200px;
  margin: 0 auto;
}

.custom-breadcrumb {
  font-size: 14px;
  padding: 10px 0;
}

.mr-1 {
  margin-right: 4px;
}

.detail-image {
  width: 100%;
  height: auto;
  display: block;
}

.product-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #303133;
  line-height: 1.4;
  margin-bottom: 20px;
}

.price-section {
  background: #fdf6f6;
  padding: 15px;
  border-radius: 8px;
}

.price-label {
  font-size: 1rem;
  color: #909399;
}

.price-value {
  font-size: 2.5rem;
  color: #f56c6c;
  font-weight: 700;
}

.other-info p {
  font-size: 1.1rem;
  margin-bottom: 12px;
  color: #606266;
}

.selling-points-box {
  padding: 15px;
  background: #f0f9eb;
  color: #67c23a;
  border-radius: 8px;
  line-height: 1.6;
}

.card-header {
  font-weight: 600;
}

.mr-2 {
  margin-right: 8px;
}

.m-1 {
  margin: 4px;
}
</style>
