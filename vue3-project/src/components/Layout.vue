<template>
  <div>
    <!-- Sidebar -->
    <nav class="navbar navbar-vertical fixed-left navbar-expand-md navbar-light bg-white" id="sidenav-main">
      <div class="container-fluid">
        <button class="navbar-toggler" type="button" @click="toggleSidebar">
          <span class="navbar-toggler-icon"></span>
        </button>
        <router-link class="navbar-brand pt-0 brand-text" to="/dashboard">
          <h4>淘宝商品数据分析与可视化系统</h4>
        </router-link>
        <ul class="nav align-items-center d-md-none">
          <li class="nav-item">
            <el-dropdown trigger="click">
              <span class="nav-link nav-link-icon">
                <i class="ni ni-bell-55"></i>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item>Action</el-dropdown-item>
                  <el-dropdown-item>Another action</el-dropdown-item>
                  <el-dropdown-item divided>Something else here</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </li>
          <li class="nav-item">
            <el-dropdown trigger="click">
              <span class="nav-link">
                <div class="media align-items-center">
                  <span class="avatar avatar-sm rounded-circle">
                    <img alt="Image placeholder" src="/assets/img/theme/team-1-800x800.jpg">
                  </span>
                </div>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <div class="dropdown-header noti-title">
                    <h6 class="text-overflow m-0">Welcome!</h6>
                  </div>
                  <el-dropdown-item>
                    <i class="ni ni-single-02"></i>
                    <span>My profile</span>
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <i class="ni ni-settings-gear-65"></i>
                    <span>Settings</span>
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <i class="ni ni-calendar-grid-58"></i>
                    <span>Activity</span>
                  </el-dropdown-item>
                  <el-dropdown-item>
                    <i class="ni ni-support-16"></i>
                    <span>Support</span>
                  </el-dropdown-item>
                  <el-dropdown-item divided>
                    <i class="ni ni-user-run"></i>
                    <span>Logout</span>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </li>
        </ul>
        <div class="collapse navbar-collapse" :class="{ show: sidebarOpen }" id="sidenav-collapse-main">
          <!-- 分组：功能菜单 -->
          <h6 class="navbar-heading text-muted">功能菜单</h6>
          <ul class="navbar-nav mb-3">
            <li class="nav-item" :class="{ active: $route.path === '/dashboard' }">
              <router-link class="nav-link" to="/dashboard">
                <i class="ni ni-tv-2 text-primary"></i> 首页
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: $route.path === '/tables' }">
              <router-link class="nav-link" to="/tables">
                <i class="ni ni-bullet-list-67 text-red"></i> 商品数据
              </router-link>
            </li>
          </ul>

          <!-- 分组：数据分析 -->
          <h6 class="navbar-heading text-muted">数据分析</h6>
          <ul class="navbar-nav mb-3">
            <li class="nav-item" :class="{ active: $route.path === '/icons' }">
              <router-link class="nav-link" to="/icons">
                <i class="ni ni-planet text-blue"></i> 商品销量分析
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: $route.path === '/maps' }">
              <router-link class="nav-link" to="/maps">
                <i class="ni ni-pin-3 text-orange"></i> 城市销量分析
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: $route.path === '/part3' }">
              <router-link class="nav-link" to="/part3">
                <i class="ni ni-shop text-info"></i> 店铺销量分析
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: $route.path === '/part4' }">
              <router-link class="nav-link" to="/part4">
                <i class="ni ni-money-coins text-success"></i> 价格区间分析
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: $route.path === '/part7' }">
              <router-link class="nav-link" to="/part7">
                <i class="ni ni-chart-bar-32 text-warning"></i> 商品平均价格分析
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: $route.path === '/part5' }">
              <router-link class="nav-link" to="/part5">
                <i class="ni ni-app text-purple"></i> 商品特点分布
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: $route.path === '/part6' }">
              <router-link class="nav-link" to="/part6">
                <i class="ni ni-cloud-upload-96 text-cyan"></i> 标题词云分析
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: $route.path === '/dashboard-screen' }">
              <router-link class="nav-link" to="/dashboard-screen">
                <i class="ni ni-tv-2 text-danger"></i> 数据可视化大屏
              </router-link>
            </li>
          </ul>

          <!-- 分组：智慧算法 -->
          <h6 class="navbar-heading text-muted">智慧算法</h6>
          <ul class="navbar-nav mb-3">
            <li class="nav-item" :class="{ active: $route.path === '/predict' }">
              <router-link class="nav-link" to="/predict">
                <i class="ni ni-bulb-61 text-primary"></i>销量预测
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: $route.path === '/clustering' }">
              <router-link class="nav-link" to="/clustering">
                <i class="ni ni-chart-pie-35 text-success"></i> 市场聚类分析
              </router-link>
            </li>
          </ul>

          <!-- 分组：系统功能 -->
          <h6 class="navbar-heading text-muted">系统功能</h6>
          <ul class="navbar-nav mb-3">
            <li class="nav-item" :class="{ active: $route.path === '/profile' }">
              <router-link class="nav-link" to="/profile">
                <i class="ni ni-single-02 text-yellow"></i> 个人中心
              </router-link>
            </li>
            <li class="nav-item" :class="{ active: $route.path === '/chat' }">
              <router-link class="nav-link" to="/chat">
                <i class="ni ni-support-16 text-primary"></i> 在线客服
              </router-link>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="http://localhost:8000/admin/" target="_blank" rel="noopener noreferrer">
                <i class="ni ni-settings-gear-65 text-success"></i> 后台管理
              </a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="javascript:void(0)" @click="handleLogout">
                <i class="ni ni-button-power text-danger"></i> 退出
              </a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
    <div class="main-content">
      <!-- Top Navbar -->
      <nav class="navbar navbar-top navbar-expand-md navbar-dark" id="navbar-main">
        <div class="container-fluid">
          <a class="h4 mb-0 text-white text-uppercase d-none d-lg-inline-block" href="#">{{ pageTitle }}</a>
      
        </div>
      </nav>
      <!-- Page Content -->
      <slot></slot>
      <!-- Footer -->

    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

defineProps({
  pageTitle: {
    type: String,
    default: 'Dashboard'
  }
})

const sidebarOpen = ref(false)
const searchText = ref('')
const topSearchText = ref('')

const toggleSidebar = () => {
  sidebarOpen.value = !sidebarOpen.value
}

const handleLogout = async () => {
  try {
    await fetch(`${API_BASE_URL}/app/logout/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include'
    })
  } catch (e) {
    // 忽略错误，前端仍然执行退出
  } finally {
    ElMessage.success('已退出登录')
    router.push('/login')
  }
}
</script>

<style scoped>
.input-group-alternative :deep(.el-input__wrapper) {
  background-color: rgba(255, 255, 255, 0.1);
  border: none;
  box-shadow: none;
}

.input-group-alternative :deep(.el-input__inner) {
  color: white;
}

.input-group-alternative :deep(.el-input__prefix) {
  color: rgba(255, 255, 255, 0.6);
}
</style>

