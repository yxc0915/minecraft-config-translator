# Minecraft 插件配置文件翻译器

这是一个用于翻译 Minecraft 插件配置文件的工具。它可以自动提取配置文件中的注释，使用 AI 进行翻译，并将翻译结果合并回原始文件。

## 功能特点

- 支持 YAML 和 TXT 格式的配置文件
- 使用 AI 进行高质量翻译
- 支持多种 AI API（如 OpenAI, OhMyGPT 等）
- 翻译工作难度不大，选择合适的模型几乎不要钱
- 批量异步翻译，提高效率
- 实时显示翻译进度
- 支持自动重试失败的翻译
- 可选择只保留中文翻译或保留原文和翻译
- 自动处理多行 AI 输出，确保配置文件结构完整性

## 安装

1. 克隆此仓库：
   
   ```
   git clone https://github.com/your-username/minecraft-config-translator.git
   cd minecraft-config-translator
   ```
2. 安装依赖：
   
   ```
   pip install -r requirements.txt
   ```
3. 配置 `config.yml` 文件，添加您的 API 密钥和其他设置。

## 使用方法

1. 运行应用：
   
   ```
   streamlit run app.py
   ```
2. 在浏览器中打开显示的 URL（通常是 http://localhost:8501 ）。
3. 上传您想要翻译的 Minecraft 插件配置文件。
4. 选择 AI API 和模型。
5. 设置翻译选项（批量大小、最大重试次数等）。
6. 点击"开始翻译"按钮。
7. 等待翻译完成，然后下载翻译后的文件。

## 配置

在 `config.yml` 文件中设置您的 API 密钥和其他选项：

```yaml
proxy:
  url: socks5://your-proxy-server:port  # 如果需要代理

apis:
  openai:
    api_key: "your-openai-api-key"
    base_url: "https://api.openai.com/v1/chat/completions"
    models:
      - "gpt-3.5-turbo"
      - "gpt-4"
  # 添加其他 API 配置...

target_language: "简体中文"
```

## 注意事项

- 推荐OhMyGPT的command-r-plus模型，价格便宜
- [点击前往OhMyGPT注册（请务必使用这个链接qwq）](https://www.ohmygpt.com?aff=2eaHPMNH)
- 请确保您有足够的 API 使用额度。
- 翻译大量文本可能需要一些时间，请耐心等待。
- 始终检查翻译结果，以确保其准确性和适用性。

## 贡献

欢迎提交 Pull Requests 或创建 Issues 来帮助改进这个项目！

## 许可证

[MIT License](LICENSE)
[[](https://)](https://)
