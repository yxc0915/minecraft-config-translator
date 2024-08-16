import streamlit as st
from core.config_loader import load_config
from core.comment_extractor import extract_comments
from core.translator import translate_comments
from core.file_handler import save_json, merge_translations

def main():
    st.title("我的世界插件配置文件翻译器")

    config = load_config()

    # 步骤 1: 上传文件
    uploaded_file = st.file_uploader("选择一个配置文件", type=['yml', 'yaml', 'txt'])
    
    if uploaded_file is not None:
        file_content = uploaded_file.getvalue().decode('utf-8')
        
        # 步骤 2: 提取注释并转换为 JSON
        comments = extract_comments(file_content)
        
        # 显示提取的注释数量
        st.write(f"已获取到 {len(comments)} 条注释")
        
        # 为注释添加 id 并保存为 JSON
        comments_with_id = [{"id": i+1, **comment} for i, comment in enumerate(comments)]
        save_json(comments_with_id, 'extracted_comments.json')
        
        st.write("提取的注释（前5条）：")
        st.json(comments_with_id[:5])
        
        # 步骤 3: 选择 API 和模型
        api_name = st.selectbox("选择 API", list(config['apis'].keys()))
        model_name = st.selectbox("选择模型", config['apis'][api_name]['models'])
        
        # 新增：选择是否只保留中文
        chinese_only = st.checkbox("只保留中文翻译")
        st.info("注意：如果 AI 输出多行翻译，它们将被合并为单行，使用 ' | ' 作为分隔符。")
        
        # 新增：选择批量处理大小
        batch_size = st.slider("选择批量处理大小", min_value=1, max_value=50, value=10, step=1)
        
        # 新增：选择最大重试次数
        max_retries = st.slider("选择最大重试次数", min_value=1, max_value=10, value=3, step=1)
        
        # 步骤 4: 翻译文本
        if st.button("开始翻译"):
            target_lang = config['target_language']
            
            # 创建进度条和状态文本
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # 开始翻译
            translated_comments = translate_comments(
                comments_with_id, 
                api_name, 
                model_name, 
                target_lang, 
                progress_bar, 
                status_text, 
                batch_size, 
                max_retries
            )
            
            # 保存翻译结果
            save_json(translated_comments, 'translated_comments.json')
            
            st.write("翻译完成。结果已保存到 'translated_comments.json'")
            
            # 步骤 5: 合并翻译结果
            merged_content = merge_translations(file_content, translated_comments, chinese_only)
            
            # 显示合并后的内容
            st.write("合并后的内容（前10行）：")
            st.text('\n'.join(merged_content.split('\n')[:10]))
            
            # 提供下载链接
            st.download_button(
                label="下载翻译后的文件",
                data=merged_content,
                file_name=f"{uploaded_file.name}_translated.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    main()
