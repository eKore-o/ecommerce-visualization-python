<template>
  <Layout page-title="个人中心">
    <!-- Page content -->
    <div class="container-fluid mt-5">
      <el-card class="profile-card" shadow="hover">
        <template #header>
          <div class="card-header">
            <div class="d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center">
                <el-icon class="me-3" size="24" color="#409EFF">
                  <User />
                </el-icon>
                <h3 class="mb-0">个人信息设置</h3>
              </div>
              <div>
                <el-button type="primary" @click="handleSave" :loading="saving">
                  <template #icon>
                    <Check />
                  </template>
                  保存修改
                </el-button>
              </div>
            </div>
          </div>
        </template>

        <div class="card-body">
          <!-- 用户基本信息 -->
          <div class="section-header mb-4">
            <el-icon class="me-2" color="#67C23A">
              <UserFilled />
            </el-icon>
            <h4 class="section-title">基本信息</h4>
            <el-divider style="width: 87%" />
          </div>

          <el-form :model="form" ref="formRef" label-width="120px" label-position="left">
            <div class="row g-4">
              <!-- 用户名和邮箱 -->
              <div class="col-12">
                <div class="row g-4">
                  <div class="col-md-6">
                    <el-form-item 
                      label="用户名" 
                      prop="username"
                      :rules="[{ required: true, message: '请输入用户名', trigger: 'blur' }]"
                    >
                      <el-input
                        v-model="form.username"
                        placeholder="请输入用户名"
                        clearable
                        :prefix-icon="User"
                      >
                        <template #prepend>
                          <span class="input-label">
                            <el-icon><User /></el-icon>
                            用户名
                          </span>
                        </template>
                      </el-input>
                    </el-form-item>
                  </div>
                  <div class="col-md-6">
                    <el-form-item 
                      label="邮箱" 
                      prop="email"
                      :rules="[
                        { required: true, message: '请输入邮箱', trigger: 'blur' },
                        { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
                      ]"
                    >
                      <el-input
                        v-model="form.email"
                        type="email"
                        placeholder="请输入邮箱地址"
                        clearable
                        :prefix-icon="Message"
                      >
                        <template #prepend>
                          <span class="input-label">
                            <el-icon><Message /></el-icon>
                            邮箱
                          </span>
                        </template>
                      </el-input>
                    </el-form-item>
                  </div>
                </div>
              </div>

              <!-- 密码修改 -->
              <div class="col-12">
                <div class="row g-4">
                  <div class="col-md-6">
                    <el-form-item 
                      label="新密码" 
                      prop="password"
                      :rules="[
                        { min: 6, message: '密码长度至少6位', trigger: 'blur' }
                      ]"
                    >
                      <el-input
                        v-model="form.password"
                        type="password"
                        placeholder="如需修改密码请填写"
                        show-password
                        :prefix-icon="Lock"
                      >
                        <template #prepend>
                          <span class="input-label">
                            <el-icon><Lock /></el-icon>
                            新密码
                          </span>
                        </template>
                      </el-input>
                      <div class="form-hint">留空表示不修改密码</div>
                    </el-form-item>
                  </div>
                  <div class="col-md-6">
                    <el-form-item 
                      label="确认密码" 
                      prop="confirmPassword"
                      :rules="[
                        { validator: validateConfirmPassword, trigger: 'blur' }
                      ]"
                    >
                      <el-input
                        v-model="form.confirmPassword"
                        type="password"
                        placeholder="请再次输入新密码"
                        show-password
                        :prefix-icon="Lock"
                      >
                        <template #prepend>
                          <span class="input-label">
                            <el-icon><Lock /></el-icon>
                            确认密码
                          </span>
                        </template>
                      </el-input>
                    </el-form-item>
                  </div>
                </div>
              </div>

              <!-- 个人简介 -->
              <div class="col-12">
                <div class="section-header mb-4 mt-2">
                  <el-icon class="me-2" color="#E6A23C">
                    <EditPen />
                  </el-icon>
                  <h4 class="section-title">个人简介</h4>
                  <el-divider style="width: 87%" />
                </div>
                
                <el-form-item label="个人介绍" prop="user_text">
                  <el-input
                    v-model="form.user_text"
                    type="textarea"
                    :rows="5"
                    placeholder="介绍一下自己，让更多人了解你..."
                    maxlength="500"
                    show-word-limit
                    resize="none"
                  />
                  <div class="form-hint">最多可输入500个字符</div>
                </el-form-item>
              </div>
            </div>
          </el-form>
        </div>

        <!-- 底部操作按钮 -->
        <template #footer>
          <div class="card-footer d-flex justify-content-between">
            <el-button type="info" @click="handleReset">
              <template #icon>
                <RefreshRight />
              </template>
              重置
            </el-button>
            <div>
              <el-button @click="$router.back()">
                <template #icon>
                  <Back />
                </template>
                返回
              </el-button>
              <el-button type="primary" @click="handleSave" :loading="saving">
                <template #icon>
                  <Check />
                </template>
                保存修改
              </el-button>
            </div>
          </div>
        </template>
      </el-card>
    </div>
  </Layout>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User,
  UserFilled,
  Message,
  Lock,
  EditPen,
  InfoFilled,
  Calendar,
  Timer,
  Check,
  RefreshRight,
  Back
} from '@element-plus/icons-vue'
import Layout from '../components/Layout.vue'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const form = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: '',
  user_text: ''
})

const formRef = ref(null)
const saving = ref(false)
const profileInfo = ref(null)

// 验证确认密码
const validateConfirmPassword = (rule, value, callback) => {
  if (form.password && value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

// 加载用户信息
const loadProfile = async () => {
  try {
    const res = await fetch(`${API_BASE_URL}/app/profile/`, {
      credentials: 'include'
    })
    const data = await res.json()
    
    if (!res.ok) {
      throw new Error(data.message || '获取用户信息失败')
    }
    
    form.username = data.data.username || ''
    form.email = data.data.email || ''
    form.user_text = data.data.user_text || ''
    form.password = ''
    form.confirmPassword = ''
    
    // 保存其他信息用于展示
    profileInfo.value = {
      created_at: data.data.created_at,
      last_login: data.data.last_login
    }
    
  } catch (e) {
    ElMessage.error(e.message || '获取用户信息失败')
  }
}

// 保存修改
const handleSave = async () => {
  if (!formRef.value) return
  
  try {
    // 验证表单
    await formRef.value.validate()
    
    saving.value = true
    
    // 准备提交的数据
    const submitData = {
      username: form.username,
      email: form.email,
      user_text: form.user_text
    }
    
    // 如果有密码则添加
    if (form.password) {
      submitData.password = form.password
    }
    
    const res = await fetch(`${API_BASE_URL}/app/profile/update/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify(submitData)
    })
    
    const data = await res.json()
    
    if (!res.ok) {
      throw new Error(data.message || '保存失败')
    }
    
    ElMessage.success({
      message: data.message || '保存成功',
      duration: 2000
    })
    
    // 清空密码字段
    form.password = ''
    form.confirmPassword = ''
    
  } catch (error) {
    if (error.name !== 'Error') {
      ElMessage.error(error.message || '保存失败')
    }
  } finally {
    saving.value = false
  }
}

// 重置表单
const handleReset = () => {
  ElMessageBox.confirm('确定要重置所有修改吗？', '提示', {
    type: 'warning',
    confirmButtonText: '确定',
    cancelButtonText: '取消'
  }).then(() => {
    loadProfile()
    ElMessage.info('已重置所有修改')
  })
}

onMounted(() => {
  loadProfile()
})
</script>

<style scoped>
.profile-card {
  border-radius: 12px;
  border: 1px solid #e4e7ed;
}

.card-header {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  border-bottom: 1px solid #e4e7ed;
  padding: 1.5rem 1.5rem 0.5rem;
  border-radius: 12px 12px 0 0;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 1.5rem;
}

.section-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #303133;
  margin: 0;
}

:deep(.el-divider) {
  margin: 0.5rem 0 0 1rem;
  flex-grow: 1;
}

:deep(.el-form-item) {
  margin-bottom: 1.5rem;
}

:deep(.el-form-item__label) {
  font-weight: 500;
  color: #606266;
}

:deep(.el-input-group__prepend) {
  background-color: #f5f7fa;
  border-right: none;
  padding: 0 15px;
}

.input-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #606266;
  font-weight: 500;
}

.form-hint {
  font-size: 0.85rem;
  color: #909399;
  margin-top: 5px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
  padding: 1rem;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #ebeef5;
}

.info-item {
  display: flex;
  align-items: center;
  padding: 0.75rem;
  background: white;
  border-radius: 6px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}

.info-label {
  flex: 1;
  display: flex;
  align-items: center;
  color: #606266;
  font-weight: 500;
}

.info-value {
  flex: 1;
  text-align: right;
  color: #303133;
  font-weight: 600;
}

.card-footer {
  background-color: #fafbfc;
  border-top: 1px solid #e4e7ed;
  padding: 1.25rem 1.5rem;
  border-radius: 0 0 12px 12px;
}

:deep(.el-button) {
  border-radius: 6px;
  padding: 8px 20px;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #409EFF 0%, #337ecc 100%);
  border: none;
}

:deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, #66b1ff 0%, #409EFF 100%);
}

:deep(.el-textarea__inner) {
  font-family: 'Microsoft YaHei', 'Segoe UI', sans-serif;
  line-height: 1.6;
}

:deep(.el-icon) {
  vertical-align: middle;
}
</style>