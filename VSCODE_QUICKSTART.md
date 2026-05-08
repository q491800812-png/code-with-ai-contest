# 🚀 VS Code 快速启动指南

## 📌 一键运行方式

### 方式 1：F5 运行 Streamlit（推荐）

1. **打开工作区**
   ```
   文件 → 打开文件夹 → 选择本项目目录
   或
   直接打开: code-with-ai-contest.code-workspace
   ```

2. **按 F5 启动应用**
   - VS Code 会自动启动 Streamlit 应用
   - 浏览器自动打开 `http://localhost:8501`
   - 开始使用 5G 信号可视化看板

### 方式 2：运行单元测试

1. **打开调试配置选择菜单**
   - 按 Ctrl+Shift+D 打开调试面板
   - 从下拉菜单选择 "🧪 Run Unit Tests"

2. **按 F5 启动测试**
   - 所有 17 个单元测试会运行
   - 结果显示在集成终端

### 方式 3：使用快捷键或菜单

- **Ctrl+Shift+B**：安装依赖 (Build Task)
- **Ctrl+Shift+D**：打开调试面板
- **F5**：开始调试/运行
- **Shift+F5**：停止调试

---

## ⚙️ 初次配置

### 1️⃣ 安装 Python 扩展
VS Code 会提示安装推荐扩展，点击"安装"：
- Python
- Pylance
- Black Formatter
- GitHub Copilot (可选)

### 2️⃣ 创建虚拟环境（可选）
```powershell
# 在 VS Code 终端中运行
python -m venv .venv
.\.venv\Scripts\Activate
```

### 3️⃣ 安装依赖
```powershell
# 方式 1：使用 Ctrl+Shift+B (Build Task)
# 方式 2：手动运行
pip install -r requirements.txt
```

---

## 📝 VS Code 工作区文件说明

### `.vscode/launch.json`
- **F5 启动配置**
- 定义了 3 个启动方案：
  1. 🚀 Run Streamlit Dashboard
  2. 🧪 Run Unit Tests
  3. 📊 Run with Coverage

### `.vscode/tasks.json`
- **快捷任务定义**
- Ctrl+Shift+B：安装依赖
- 其他任务：测试、代码格式化、Lint 检查

### `.vscode/settings.json`
- **工作区设置**
- Python 环境配置
- 代码格式化规则
- 文件排除规则

### `.vscode/extensions.json`
- **推荐扩展列表**
- 新成员打开项目时自动提示安装

### `code-with-ai-contest.code-workspace`
- **VS Code 工作区文件**
- 包含所有设置和启动配置
- 方便用户直接打开

---

## 🎯 常用快捷键

| 快捷键 | 功能 |
|--------|------|
| **F5** | 🚀 开始调试（运行 Streamlit） |
| **Shift+F5** | ⏹️ 停止调试 |
| **Ctrl+Shift+D** | 🐛 打开调试面板 |
| **Ctrl+Shift+B** | 📦 运行构建任务（安装依赖） |
| **Ctrl+Shift+`** | 📟 打开/关闭终端 |
| **Ctrl+K Ctrl+0** | 📂 打开文件浏览器 |
| **Ctrl+Shift+P** | 🔍 打开命令框 |

---

## 🐛 调试功能

### 设置断点
1. 点击代码行号左侧的空白处
2. 红色圆点表示已设置断点
3. 按 F5 运行，执行到断点时暂停

### 调试工具栏
- ▶️ 继续
- ⬇️ 单步进入
- ⬆️ 单步跳过
- ↩️ 单步退出
- 🔄 重启
- ⏹️ 停止

### 监视变量
- 在调试面板中定义监视表达式
- 实时查看变量值的变化

---

## 📊 运行不同的配置

### 1. 调试启动面板选择

点击调试配置下拉菜单（F5 旁边），选择：
- 🚀 **Run Streamlit Dashboard** - 运行 Web 应用
- 🧪 **Run Unit Tests** - 运行单元测试
- 📊 **Run with Coverage** - 运行测试并生成覆盖率报告

### 2. Python REPL

在调试模式下，可以在"调试控制台"输入 Python 代码：
```python
>>> df.head()
>>> len(filtered_df)
>>> get_color(-95)
```

---

## 🚨 常见问题

### Q: F5 按下后没有反应？

**A:** 检查以下几点：
1. 确保选择了正确的启动配置（下拉菜单）
2. Python 扩展已安装
3. 依赖已安装：`pip install -r requirements.txt`
4. 检查输出面板获取错误信息

### Q: 如何修改 F5 的启动行为？

**A:** 编辑 `.vscode/launch.json` 中的 `"module": "streamlit"` 配置

### Q: 调试时如何查看变量？

**A:** 
- 左侧"变量"面板自动显示本地变量
- 悬停鼠标到代码中的变量名上
- 在"监视"面板添加自定义表达式

### Q: 如何停止运行的 Streamlit 应用？

**A:** 按 Shift+F5 或点击调试工具栏的停止按钮

---

## 📚 相关文档

- [README_SOLUTION.md](README_SOLUTION.md) - 完整项目说明
- [app.py](app.py) - 主应用源代码
- [test_dashboard.py](test_dashboard.py) - 单元测试
- [PROJECT_COMPLETION.md](PROJECT_COMPLETION.md) - 完成总结

---

## ✨ 推荐工作流

1. **打开项目**
   ```
   code code-with-ai-contest.code-workspace
   ```

2. **一键安装依赖**
   - Ctrl+Shift+B (或从快速菜单选择任务)

3. **一键运行应用**
   - F5 (自动选择"Run Streamlit Dashboard")

4. **浏览器自动打开**
   - http://localhost:8501

5. **开始开发**
   - 修改代码后自动热重载
   - 按 F5 重新启动应用

---

## 🎓 扩展学习

### 调试技巧
- 使用条件断点：右键断点→编辑条件
- 使用日志点：右键代码行→添加日志点
- 使用远程调试（高级）

### 性能分析
- 使用 Python Profiler
- 监控执行时间和内存使用

### 代码质量
- Pylint 检查：Ctrl+Shift+P → "Lint"
- Black 格式化：右键→"Format Document"

---

**祝你使用愉快！🎉**

有任何问题，查看 [README_SOLUTION.md](README_SOLUTION.md) 获取更多帮助。
