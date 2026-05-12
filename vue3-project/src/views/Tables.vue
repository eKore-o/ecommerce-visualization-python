<template>
  <Layout page-title="商品数据">
    <div class="container-fluid mt-4">
      <!-- 筛选区域 -->
      <el-card class="mb-4" shadow="never">
        <div class="filter-section">
          <div class="row align-items-center mb-3">
            <div class="col-auto">
              <label class="filter-label">关键词筛选：</label>
            </div>
            <div class="col">
              <el-select
                v-model="selectedBrands"
                multiple
                placeholder="请选择关键词"
                style="width: 100%"
                @change="handleFilterChange"
              >
                <el-option
                  v-for="brand in brands"
                  :key="brand"
                  :label="brand"
                  :value="brand"
                />
              </el-select>
            </div>
            <div class="col-auto">
              <el-button type="default" @click="handleReset">
                <el-icon class="mr-2"><Refresh /></el-icon>
                重置筛选
              </el-button>
            </div>
          </div>
          
          <div class="row align-items-center">
            <div class="col-auto">
              <label class="filter-label">地址筛选：</label>
            </div>
            <div class="col">
              <div class="address-tags">
                <el-tag
                  v-for="address in addresses"
                  :key="address"
                  :type="selectedAddresses.includes(address) ? 'primary' : 'info'"
                  class="address-tag"
                  @click="toggleAddress(address)"
                >
                  {{ address }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 导出按钮 -->
      <div class="export-buttons mb-4">
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

      <!-- 商品卡片展示 -->
      <div v-if="loading" class="text-center py-5">
        <el-icon class="is-loading" size="32"><Loading /></el-icon>
        <p>加载中...</p>
      </div>
      
      <div v-else-if="products.length === 0" class="text-center py-5">
        <p class="text-muted">暂无商品数据</p>
      </div>
      
      <div v-else class="product-grid">
        <div
          v-for="product in products"
          :key="product.id"
          class="product-card"
        >
          <div class="product-image-wrapper" @click="$router.push(`/product/${product.id}`)">
            <img
              :src="product.image_url || '/assets/img/theme/bootstrap.jpg'"
              :alt="product.title"
              class="product-image"
              @error="handleImageError"
            />
            <div v-if="product.selling_points" class="selling-points">
              {{ product.selling_points }}
            </div>
            <div class="image-overlay">
              <el-icon class="overlay-icon"><View /></el-icon>
              <span>查看详情</span>
            </div>
          </div>
          <div class="product-info">
            <h5 class="product-title" :title="product.title">
              {{ product.title || '无标题' }}
            </h5>
            <div class="product-details">
              <div class="detail-item">
                <el-icon class="detail-icon shop-icon"><Shop /></el-icon>
                <span class="detail-label">店铺：</span>
                <span class="detail-value shop-value">{{ product.shop || '未知' }}</span>
              </div>
              <div class="detail-item">
                <el-icon class="detail-icon price-icon"><Money /></el-icon>
                <span class="detail-label">价格：</span>
                <span class="detail-value price">¥{{ product.price || '0.00' }}</span>
              </div>
              <div class="detail-item">
                <el-icon class="detail-icon address-icon"><Location /></el-icon>
                <span class="detail-label">发货地址：</span>
                <span class="detail-value address-value">{{ product.ship_address || '未知' }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 分页 -->
      <div v-if="totalPages > 0" class="pagination-wrapper mt-4">
        <el-card shadow="never">
          <div class="pagination-container">
            <div class="pagination-info">
              当前第 {{ currentPage }} 页 / 共 {{ totalPages }} 页
            </div>
            <div class="pagination-buttons">
              <el-button
                :disabled="currentPage === 1"
                @click="goToPage(1)"
              >
                首页
              </el-button>
              <el-button
                v-if="currentPage > 2"
                @click="goToPage(currentPage - 2)"
              >
                {{ currentPage - 2 }}
              </el-button>
              <el-button
                v-if="currentPage > 1"
                @click="goToPage(currentPage - 1)"
              >
                {{ currentPage - 1 }}
              </el-button>
              <el-button type="primary" disabled>
                {{ currentPage }}
              </el-button>
              <el-button
                v-if="currentPage < totalPages"
                @click="goToPage(currentPage + 1)"
              >
                {{ currentPage + 1 }}
              </el-button>
              <el-button
                v-if="currentPage < totalPages - 1"
                @click="goToPage(currentPage + 2)"
              >
                {{ currentPage + 2 }}
              </el-button>
              <el-button
                :disabled="currentPage === totalPages"
                @click="goToPage(totalPages)"
              >
                尾页
              </el-button>
            </div>
            <div class="pagination-jump">
              <span>跳转到：</span>
              <el-input-number
                v-model="jumpPage"
                :min="1"
                :max="totalPages"
                :precision="0"
                style="width: 100px"
                @keyup.enter="handleJump"
              />
              <el-button type="primary" @click="handleJump">跳转</el-button>
            </div>
          </div>
        </el-card>
      </div>
    </div>
  </Layout>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, Loading, Refresh, View, Shop, Money, Location } from '@element-plus/icons-vue'
import Layout from '../components/Layout.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const products = ref([])
const brands = ref([])
const addresses = ref([])
const selectedBrands = ref([])
const selectedAddresses = ref([])
const loading = ref(false)
const exporting = ref(false)

const currentPage = ref(1)
const totalPages = ref(0)
const pageSize = 10
const jumpPage = ref(1)

// 加载筛选选项
const loadFilterOptions = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/app/products/filter_options/`)
    const data = await res.json()
    brands.value = data.brands || []
    addresses.value = data.addresses || []
  } catch (e) {
    console.error('加载筛选选项失败', e)
  }
}

// 加载商品列表
const loadProducts = async () => {
  loading.value = true
  try {
    const params = new URLSearchParams()
    params.append('page', currentPage.value)
    params.append('page_size', pageSize)
    
    selectedBrands.value.forEach(brand => {
      params.append('brands', brand)
    })
    
    selectedAddresses.value.forEach(address => {
      params.append('addresses', address)
    })
    
    const res = await fetch(`${API_BASE_URL}/app/products/?${params.toString()}`)
    const data = await res.json()
    
    products.value = data.products || []
    totalPages.value = data.total_pages || 0
    currentPage.value = data.page || 1
  } catch (e) {
    ElMessage.error('加载商品数据失败')
    console.error(e)
  } finally {
    loading.value = false
  }
}

// 筛选变化
const handleFilterChange = () => {
  currentPage.value = 1
  loadProducts()
}

// 切换地址选择
const toggleAddress = (address) => {
  const index = selectedAddresses.value.indexOf(address)
  if (index > -1) {
    selectedAddresses.value.splice(index, 1)
  } else {
    selectedAddresses.value.push(address)
  }
  handleFilterChange()
}

// 跳转页面
const goToPage = (page) => {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
    loadProducts()
    // 滚动到顶部
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

// 跳转到指定页
const handleJump = () => {
  if (jumpPage.value >= 1 && jumpPage.value <= totalPages.value) {
    goToPage(jumpPage.value)
  } else {
    ElMessage.warning(`请输入1-${totalPages.value}之间的页码`)
  }
}

// 导出数据
const handleExport = async (type) => {
  exporting.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/app/products/export/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({
        type: type,
        brands: selectedBrands.value,
        addresses: selectedAddresses.value
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
    let filename = `商品数据_${new Date().getTime()}`
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

// 图片加载错误处理
const handleImageError = (e) => {
  e.target.src = '/assets/img/theme/bootstrap.jpg'
}

// 打开详情页
const openDetail = (url) => {
  if (url) {
    window.open(url, '_blank')
  } else {
    ElMessage.warning('该商品暂无详情页链接')
  }
}

// 重置筛选
const handleReset = () => {
  selectedBrands.value = []
  selectedAddresses.value = []
  currentPage.value = 1
  loadProducts()
  ElMessage.success('已重置筛选条件')
}

onMounted(() => {
  loadFilterOptions()
  loadProducts()
})
</script>

<style scoped>
.filter-section {
  padding: 1rem 0;
}

.filter-label {
  font-weight: 600;
  color: #303133;
  margin-right: 10px;
}

.address-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.address-tag {
  cursor: pointer;
}

.export-buttons {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.mr-2 {
  margin-right: 8px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 2rem;
}

.product-card {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

/* 移除悬浮特效 */
/* .product-card:hover { ... } */

.product-image-wrapper {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background-color: #f5f7fa;
  cursor: pointer;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* 移除缩放效果 */
/* .product-image-wrapper:hover .product-image { ... } */

.image-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
  color: white;
}

.product-image-wrapper:hover .image-overlay {
  opacity: 1;
}

.overlay-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.selling-points {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(255, 0, 0, 0.8);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  max-width: calc(100% - 20px);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.product-info {
  padding: 15px;
}

.product-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 12px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  min-height: 48px;
}

.product-details {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.detail-item {
  display: flex;
  align-items: center;
  font-size: 14px;
  gap: 6px;
}

.detail-icon {
  font-size: 16px;
  flex-shrink: 0;
}

.shop-icon {
  color: #409EFF;
}

.price-icon {
  color: #F56C6C;
}

.address-icon {
  color: #67C23A;
}

.detail-label {
  color: #909399;
  min-width: 70px;
  flex-shrink: 0;
}

.detail-value {
  color: #303133;
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.detail-value.price {
  color: #F56C6C;
  font-weight: 600;
  font-size: 16px;
}

.shop-value {
  color: #409EFF;
  font-weight: 500;
}

.address-value {
  color: #67C23A;
  font-weight: 500;
}

.pagination-wrapper {
  margin-top: 2rem;
}

.pagination-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
  padding: 1rem 0;
}

.pagination-info {
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.pagination-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.pagination-jump {
  display: flex;
  align-items: center;
  gap: 10px;
}

.pagination-jump span {
  font-size: 14px;
  color: #606266;
}

@media (max-width: 768px) {
  .product-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 15px;
  }
  
  .pagination-container {
    flex-direction: column;
    align-items: stretch;
  }
  
  .pagination-buttons {
    justify-content: center;
  }
  
  .pagination-jump {
    justify-content: center;
  }
}
</style>
