<template>
  <div class="row">
    <div class="col-xl-3 col-lg-6">
      <el-card class="card card-stats mb-4 mb-xl-0" shadow="never">
        <div class="card-body">
          <div class="row">
            <div class="col">
              <h5 class="card-title text-uppercase text-muted mb-0">用户数量</h5>
              <span class="h2 font-weight-bold mb-0">{{ stats.user_count }}</span>
            </div>
            <div class="col-auto">
              <div class="icon icon-shape bg-primary text-white rounded-circle shadow">
                <i class="fas fa-users"></i>
              </div>
            </div>
          </div>
          <p class="mt-3 mb-0 text-muted text-sm">
            <span class="text-nowrap">当前系统注册用户总数</span>
          </p>
        </div>
      </el-card>
    </div>
    <div class="col-xl-3 col-lg-6">
      <el-card class="card card-stats mb-4 mb-xl-0" shadow="never">
        <div class="card-body">
          <div class="row">
            <div class="col">
              <h5 class="card-title text-uppercase text-muted mb-0">数据量</h5>
              <span class="h2 font-weight-bold mb-0">{{ stats.data_count }}</span>
            </div>
            <div class="col-auto">
              <div class="icon icon-shape bg-warning text-white rounded-circle shadow">
                <i class="fas fa-database"></i>
              </div>
            </div>
          </div>
          <p class="mt-3 mb-0 text-muted text-sm">
            <span class="text-nowrap">已入库的淘宝商品记录数</span>
          </p>
        </div>
      </el-card>
    </div>
    <div class="col-xl-3 col-lg-6">
      <el-card class="card card-stats mb-4 mb-xl-0" shadow="never">
        <div class="card-body">
          <div class="row">
            <div class="col">
              <h5 class="card-title text-uppercase text-muted mb-0">城市数量</h5>
              <span class="h2 font-weight-bold mb-0">{{ stats.city_count }}</span>
            </div>
            <div class="col-auto">
              <div class="icon icon-shape bg-yellow text-white rounded-circle shadow">
                <i class="fas fa-city"></i>
              </div>
            </div>
          </div>
          <p class="mt-3 mb-0 text-muted text-sm">
            <span class="text-nowrap">城市数量</span>
          </p>
        </div>
      </el-card>
    </div>
    <div class="col-xl-3 col-lg-6">
      <el-card class="card card-stats mb-4 mb-xl-0" shadow="never">
        <div class="card-body">
          <div class="row">
            <div class="col">
              <h5 class="card-title text-uppercase text-muted mb-0">商品种类</h5>
              <span class="h2 font-weight-bold mb-0">{{ stats.product_count }}</span>
            </div>
            <div class="col-auto">
              <div class="icon icon-shape bg-info text-white rounded-circle shadow">
                <i class="fas fa-boxes"></i>
              </div>
            </div>
          </div>
          <p class="mt-3 mb-0 text-muted text-sm">
            <span class="text-nowrap">爬取的商品种类数量</span>
          </p>
        </div>
      </el-card>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  stats: {
    type: Object,
    default: () => ({
      user_count: 0,
      data_count: 0,
      city_count: 0,
      product_count: 0
    })
  }
})
</script>

<style scoped>
.icon-shape {
  width: 3rem;
  height: 3rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.bg-danger {
  background-color: #f5365c !important;
}

.bg-warning {
  background-color: #fb6340 !important;
}

.bg-yellow {
  background-color: #ffd600 !important;
}

.bg-info {
  background-color: #11cdef !important;
}
</style>

