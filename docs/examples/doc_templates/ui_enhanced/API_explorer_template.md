# 交互式 API 文档模板 (Enhanced with Magic MCP)

## 生成的文档
1. ✅ docs/api/endpoints.md (标准 Markdown)
2. ✅ docs/api/explorer.html (交互式 API 浏览器)

## 交互式组件特性
- **API 浏览器**: Swagger/OpenAPI UI 风格的界面
  - 可以直接在浏览器中测试 API
  - 自动生成请求示例
  - 显示响应状态和数据
  - 支持认证 token 配置

- **代码示例沙盒**: 可运行的代码片段
  - 支持多种编程语言
  - 可修改和立即执行
  - 实时显示输出结果

- **参数配置器**: 表单式的请求构建
  - 自动验证输入
  - 提供默认值建议
  - 生成 cURL 命令

## 使用方式
```bash
# 启动本地文档服务器
cd docs/api
python -m http.server 8000

# 浏览器访问
open http://localhost:8000/explorer.html
```
