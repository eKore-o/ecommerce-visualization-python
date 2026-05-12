<template>
    <Layout page-title="">
      <div class="container-fluid mt-4">
        <el-card shadow="hover" class="chat-card">
          <template #header>
            <div class="chat-header">
              <div class="header-left">
                <div class="agent-avatar">
                  <svg class="avatar-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                  </svg>
                </div>
                <div class="header-info">
                  <h4 class="mb-1">
                    <span class="service-name">淘宝商品客服</span>
                    <span class="status-indicator active"></span>
                  </h4>
                  <small class="text-muted">
                    <svg class="icon-small" viewBox="0 0 24 24" fill="currentColor">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                    </svg>
                    在线 · 快速响应
                  </small>
                </div>
              </div>
            
            </div>
          </template>
  
          <div class="chat-body">
            <div class="chat-history">
              <div class="date-divider">
                <span>今天</span>
              </div>
              <div class="messages" ref="listRef">
                <div
                  v-for="(item, idx) in messages"
                  :key="idx"
                  :class="['msg-row', item.role === 'assistant' ? 'left' : 'right']"
                >
                  <div class="avatar" :class="item.role === 'assistant' ? 'agent' : 'user'">
                    <template v-if="item.role === 'assistant'">
                      <svg class="avatar-svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                      </svg>
                    </template>
                    <template v-else>
                      <svg class="avatar-svg" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                      </svg>
                    </template>
                  </div>
                  <div class="message-container">
                    <div class="bubble" :class="item.role === 'assistant' ? 'agent-bubble' : 'user-bubble'">
                      <div class="content">{{ item.content }}</div>
                      <div class="message-time">
                        {{ getCurrentTime() }}
                      </div>
                    </div>
                    <div class="message-status" v-if="item.role === 'user'">
                      <svg class="status-icon" viewBox="0 0 24 24" fill="#4CAF50">
                        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
  
          <div class="chat-footer">
            <div class="input-wrapper">
             
              <el-input
                v-model="input"
                type="textarea"
                :rows="3"
                placeholder="请输入您要咨询的内容..."
                class="chat-textarea"
                @keyup.enter.native.prevent="handleSend"
              />
              <div class="input-hint">
                <svg class="hint-icon" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M11 7h2v2h-2zm0 4h2v6h-2zm1-9C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
                </svg>
                按 Enter 发送，Shift + Enter 换行
              </div>
            </div>
            <div class="send-wrapper">
              <el-button 
                type="primary" 
                :loading="loading" 
                @click="handleSend"
                class="send-btn"
              >
                <template #default>
                  <span class="send-text">发送</span>
                  <svg class="send-icon" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                  </svg>
                </template>
              </el-button>
            </div>
          </div>
        </el-card>
      </div>
    </Layout>
  </template>
  
  <script setup>
  import { ref, nextTick } from 'vue'
  import { ElMessage } from 'element-plus'
  import Layout from '../components/Layout.vue'
  
  const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  
  const messages = ref([
    { role: 'assistant', content: '您好，我是淘宝商品在线客服，有什么可以帮助您的吗？' }
  ])
  const input = ref('')
  const loading = ref(false)
  const listRef = ref(null)
  
  const getCurrentTime = () => {
    const now = new Date()
    return `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`
  }
  
  const scrollToBottom = () => {
    nextTick(() => {
      if (listRef.value) {
        listRef.value.scrollTop = listRef.value.scrollHeight
      }
    })
  }
  
  const handleSend = async () => {
    const text = input.value.trim()
    if (!text) {
      ElMessage.warning('请输入内容')
      return
    }
    messages.value.push({ role: 'user', content: text })
    input.value = ''
    scrollToBottom()
  
    loading.value = true
    try {
      const res = await fetch(`${API_BASE_URL}/app/chat/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ message: text })
      })
      const data = await res.json()
      if (!res.ok) {
        throw new Error(data.message || '请求失败')
      }
      messages.value.push({ role: 'assistant', content: data.reply || '抱歉，我暂时无法回答。' })
      scrollToBottom()
    } catch (e) {
      ElMessage.error(e.message || '请求失败')
    } finally {
      loading.value = false
    }
  }
  </script>
  
  <style scoped>
  .chat-card {
    border: none;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
    overflow: hidden;
  }
  
  .chat-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 16px 24px;
    border-bottom: 1px solid #f0f0f0;
  }
  
  .header-left {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  
  .agent-avatar {
    width: 48px;
    height: 48px;
    border-radius: 50%;
    background: #f0f7ff;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px solid #e6f7ff;
  }
  
  .avatar-icon {
    width: 24px;
    height: 24px;
    color: #1890ff;
  }
  
  .header-info {
    display: flex;
    flex-direction: column;
  }
  
  .service-name {
    font-size: 18px;
    font-weight: 600;
    color: #1a1a1a;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  
  .status-indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #52c41a;
  }
  
  .status-indicator.active {
    background: #52c41a;
  }
  
  .status-indicator.active::after {
    content: '';
    position: absolute;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    border: 2px solid rgba(82, 196, 26, 0.3);
    animation: pulse 2s infinite;
  }
  
  @keyframes pulse {
    0% { transform: scale(1); opacity: 1; }
    100% { transform: scale(1.5); opacity: 0; }
  }
  
  .icon-small {
    width: 14px;
    height: 14px;
    margin-right: 6px;
    color: #52c41a;
    vertical-align: -2px;
  }
  
  .header-actions {
    display: flex;
    gap: 8px;
  }
  
  .action-btn {
    border: none;
    background: #f5f5f5;
    transition: all 0.3s;
  }
  
  .action-btn:hover {
    background: #e6f7ff;
    color: #1890ff;
  }
  
  .action-icon {
    width: 18px;
    height: 18px;
  }
  
  .chat-body {
    height: 60vh;
    background: #fafafa;
    padding: 0;
  }
  
  .chat-history {
    height: 100%;
    padding: 20px 24px;
  }
  
  .date-divider {
    text-align: center;
    margin: 20px 0;
    position: relative;
  }
  
  .date-divider span {
    display: inline-block;
    padding: 4px 16px;
    background: #f0f0f0;
    border-radius: 12px;
    font-size: 12px;
    color: #666;
    position: relative;
    z-index: 1;
  }
  
  .date-divider::before {
    content: '';
    position: absolute;
    top: 50%;
    left: 0;
    right: 0;
    height: 1px;
    background: #e8e8e8;
  }
  
  .messages {
    height: calc(100% - 60px);
    overflow-y: auto;
    padding-right: 8px;
  }
  
  .messages::-webkit-scrollbar {
    width: 6px;
  }
  
  .messages::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 3px;
  }
  
  .messages::-webkit-scrollbar-thumb {
    background: #c1c1c1;
    border-radius: 3px;
  }
  
  .messages::-webkit-scrollbar-thumb:hover {
    background: #a8a8a8;
  }
  
  .msg-row {
    display: flex;
    margin-bottom: 20px;
    position: relative;
  }
  
  .msg-row.left {
    flex-direction: row;
  }
  
  .msg-row.right {
    flex-direction: row-reverse;
  }
  
  .avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    flex-shrink: 0;
    margin-top: 4px;
  }
  
  .avatar.agent {
    background: #f0f7ff;
    border: 1px solid #e6f7ff;
  }
  
  .avatar.user {
    background: #f6ffed;
    border: 1px solid #f6ffed;
  }
  
  .avatar-svg {
    width: 18px;
    height: 18px;
  }
  
  .avatar.agent .avatar-svg {
    color: #1890ff;
  }
  
  .avatar.user .avatar-svg {
    color: #52c41a;
  }
  
  .message-container {
    max-width: 70%;
    display: flex;
    align-items: flex-end;
    margin: 0 12px;
  }
  
  .bubble {
    max-width: 100%;
    border-radius: 12px;
    padding: 12px 16px;
    position: relative;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
    line-height: 1.5;
  }
  
  .agent-bubble {
    background: white;
    border: 1px solid #f0f0f0;
    border-top-left-radius: 4px;
  }
  
  .user-bubble {
    background: #1890ff;
    color: white;
    border-top-right-radius: 4px;
  }
  
  .user-bubble .content {
    color: white;
  }
  
  .agent-bubble::before {
    content: '';
    position: absolute;
    left: -8px;
    top: 12px;
    width: 0;
    height: 0;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
    border-right: 8px solid white;
  }
  
  .user-bubble::before {
    content: '';
    position: absolute;
    right: -8px;
    top: 12px;
    width: 0;
    height: 0;
    border-top: 8px solid transparent;
    border-bottom: 8px solid transparent;
    border-left: 8px solid #1890ff;
  }
  
  .content {
    white-space: pre-wrap;
    word-break: break-word;
    font-size: 14px;
    color: #1a1a1a;
  }
  
  .message-time {
    font-size: 11px;
    color: #999;
    margin-top: 4px;
    text-align: right;
  }
  
  .user-bubble .message-time {
    color: rgba(255, 255, 255, 0.8);
  }
  
  .message-status {
    margin-left: 8px;
    margin-bottom: 4px;
  }
  
  .status-icon {
    width: 16px;
    height: 16px;
  }
  
  .chat-footer {
    padding: 20px 24px;
    border-top: 1px solid #f0f0f0;
  }
  
  .input-wrapper {
    position: relative;
    margin-bottom: 12px;
  }
  
  .input-actions {
    position: absolute;
    left: 12px;
    top: 12px;
    display: flex;
    gap: 8px;
    z-index: 1;
  }
  
  .input-action-btn {
    background: none;
    border: none;
    padding: 4px;
    cursor: pointer;
    color: #666;
    transition: color 0.3s;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .input-action-btn:hover {
    color: #1890ff;
  }
  
  .action-icon-sm {
    width: 18px;
    height: 18px;
  }
  
  .chat-textarea :deep(.el-textarea__inner) {
    padding-left: 48px;
    padding-right: 48px;
    border-radius: 8px;
    border: 1px solid #e8e8e8;
    font-size: 14px;
    line-height: 1.5;
    resize: none;
    transition: border-color 0.3s;
  }
  
  .chat-textarea :deep(.el-textarea__inner:hover) {
    border-color: #c0c4cc;
  }
  
  .chat-textarea :deep(.el-textarea__inner:focus) {
    border-color: #1890ff;
    box-shadow: 0 0 0 2px rgba(24, 144, 255, 0.1);
  }
  
  .input-hint {
    display: flex;
    align-items: center;
    gap: 6px;
    font-size: 12px;
    color: #999;
    margin-top: 8px;
    padding-left: 4px;
  }
  
  .hint-icon {
    width: 14px;
    height: 14px;
  }
  
  .send-wrapper {
    display: flex;
    justify-content: flex-end;
  }
  
  .send-btn {
    padding: 10px 24px;
    border-radius: 6px;
    background: #1890ff;
    border: none;
    transition: all 0.3s;
  }
  
  .send-btn:hover {
    background: #40a9ff;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(24, 144, 255, 0.3);
  }
  
  .send-text {
    font-weight: 500;
    margin-right: 6px;
  }
  
  .send-icon {
    width: 16px;
    height: 16px;
  }
  </style>