<template>
  <div class="bg-default register-page">
    <div class="main-content full-width">
      <!-- Navbar -->
      <nav class="navbar navbar-top navbar-horizontal navbar-expand-md navbar-dark">
        <div class="container px-4">
          <router-link class="navbar-brand brand-text" to="/">
            <h4 class="mb-0 text-white">淘宝商品数据分析与可视化系统</h4>
          </router-link>
          <button class="navbar-toggler" type="button" @click="toggleNavbar">
            <span class="navbar-toggler-icon"></span>
          </button>
          <div class="collapse navbar-collapse" :class="{ show: navbarOpen }" id="navbar-collapse-main">
            <div class="navbar-collapse-header d-md-none">
              <div class="row">
                <div class="col-6 collapse-brand">
                  <router-link to="/">
                    <h5 class="mb-0 text-primary">淘宝商品数据分析与可视化系统</h5>
                  </router-link>
                </div>
                <div class="col-6 collapse-close">
                  <button type="button" class="navbar-toggler" @click="toggleNavbar">
                    <span></span>
                    <span></span>
                  </button>
                </div>
              </div>
            </div>
            <ul class="navbar-nav ml-auto">
              <li class="nav-item">
                <router-link class="nav-link nav-link-icon active" to="/register">
                  <i class="ni ni-circle-08"></i>
                  <span class="nav-link-inner--text">注册</span>
                </router-link>
              </li>
              <li class="nav-item">
                <router-link class="nav-link nav-link-icon" to="/login">
                  <i class="ni ni-key-25"></i>
                  <span class="nav-link-inner--text">登录</span>
                </router-link>
              </li>
            </ul>
          </div>
        </div>
      </nav>
      <!-- Header -->
      <div class="header bg-gradient-primary py-7 py-lg-8">
        <div class="container">
              <div class="header-body text-center mb-7">
            <div class="row justify-content-center">
              <div class="col-lg-5 col-md-6">
                <h1 class="text-white">欢迎注册</h1>
                <p class="text-lead text-light">请填写以下信息创建您的账号。</p>
              </div>
            </div>
          </div>
        </div>
        <div class="separator separator-bottom separator-skew zindex-100">
          <svg x="0" y="0" viewBox="0 0 2560 100" preserveAspectRatio="none" version="1.1" xmlns="http://www.w3.org/2000/svg">
            <polygon class="fill-default" points="2560 0 2560 100 0 100"></polygon>
          </svg>
        </div>
      </div>
      <!-- Page content -->
      <div class="container mt--8 pb-5">
        <div class="row justify-content-center">
          <div class="col-lg-6 col-md-8">
            <el-card class="card bg-secondary shadow border-0" shadow="never">
             
              <div class="card-body px-lg-5 py-lg-5">
                
                <el-form :model="form" label-width="0">
                  <el-form-item>
                    <el-input
                      v-model="form.username"
                      placeholder="用户名"
                      size="large"
                      class="input-group-alternative"
                    >
                      <template #prefix>
                        <i class="ni ni-circle-08"></i>
                      </template>
                    </el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-input
                      v-model="form.email"
                      placeholder="邮箱"
                      size="large"
                      class="input-group-alternative"
                    >
                      <template #prefix>
                        <i class="ni ni-email-83"></i>
                      </template>
                    </el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-input
                      v-model="form.password"
                      placeholder="密码"
                      type="password"
                      size="large"
                      class="input-group-alternative"
                      show-password
                    >
                      <template #prefix>
                        <i class="ni ni-lock-circle-open"></i>
                      </template>
                    </el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-input
                      v-model="form.confirmPassword"
                      placeholder="确认密码"
                      type="password"
                      size="large"
                      class="input-group-alternative"
                      show-password
                    >
                      <template #prefix>
                        <i class="ni ni-lock-circle-open"></i>
                      </template>
                    </el-input>
                  </el-form-item>
                  <div class="row my-4">
                    <div class="col-12">
                      <el-checkbox v-model="form.agree">
                        <span class="text-muted">我已阅读并同意<a href="#!">用户协议</a></span>
                      </el-checkbox>
                    </div>
                  </div>
                  <div class="text-center">
                    <el-button
                      type="primary"
                      size="large"
                      class="mt-4"
                      :loading="submitting"
                      @click="handleRegister"
                    >
                      立即注册
                    </el-button>
                  </div>
                </el-form>
              </div>
            </el-card>
          </div>
        </div>
      </div>
     
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const navbarOpen = ref(false)
const submitting = ref(false)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  agree: false
})

const toggleNavbar = () => {
  navbarOpen.value = !navbarOpen.value
}

const handleRegister = async () => {
  if (!form.value.username || !form.value.email || !form.value.password || !form.value.confirmPassword) {
    ElMessage.error('请完整填写注册信息')
    return
  }

  if (form.value.password !== form.value.confirmPassword) {
    ElMessage.error('两次输入的密码不一致')
    return
  }

  if (!form.value.agree) {
    ElMessage.error('请勾选用户协议')
    return
  }

  submitting.value = true
  try {
    const response = await fetch(`${API_BASE_URL}/app/register/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(form.value)
    })
    const result = await response.json()
    if (!response.ok) {
      throw new Error(result.message || '注册失败')
    }
    ElMessage.success(result.message || '注册成功')
    router.push('/login')
  } catch (error) {
    ElMessage.error(error.message || '注册失败')
  } finally {
    submitting.value = false
  }
}
</script>

<style scoped>
.register-page {
  min-height: 100vh;
  display: flex;
}

.main-content.full-width {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.btn-wrapper {
  display: flex;
  gap: 10px;
  justify-content: center;
}

.btn-neutral {
  background: white;
  color: #525f7f;
  border: 1px solid #e9ecef;
}

.btn-inner--text {
  margin-left: 8px;
}

.input-group-alternative {
  border: 1px solid #cad1d7;
  border-radius: 0.375rem;
}

.input-group-alternative :deep(.el-input__wrapper) {
  box-shadow: none;
  border: none;
}

.input-group-alternative :deep(.el-input__inner) {
  padding-left: 40px;
}

.input-group-alternative :deep(.el-input__prefix) {
  left: 12px;
  color: #8898aa;
}
</style>

