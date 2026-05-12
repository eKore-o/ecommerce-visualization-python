@echo off
chcp 65001 >nul
title 淘宝商品数据分析与可视化系统



:: ── 路径配置 ──────────────────────────────────
set ROOT=%~dp0
set DJANGO_DIR=%ROOT%djangoProject
set VUE_DIR=%ROOT%vue3-project
set PYTHON=D:\ProgramData\anaconda3\python.exe
set NODE_CMD=npm

:: ── 启动 Django 后端 ──────────────────────────
echo [1/2] 启动 Django 后端 (http://localhost:8000) ...
start "Django 后端" cmd /k "cd /d %DJANGO_DIR% && %PYTHON% manage.py runserver"

:: 等待 Django 启动
timeout /t 2 /nobreak >nul

:: ── 启动 Vue 前端 ─────────────────────────────
echo [2/2] 启动 Vue 前端 (http://localhost:3000) ...
start "Vue 前端" cmd /k "cd /d %VUE_DIR% && %NODE_CMD% run dev"

echo   两个服务已在独立窗口中启动
echo   后端: http://localhost:8000
echo   前端: http://localhost:3000
echo   后台: http://localhost:8000/admin/

pause
