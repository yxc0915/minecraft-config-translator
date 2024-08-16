import asyncio
from core.api_caller import call_ai_api_async
from core.config_loader import load_config
import logging
import sys

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=sys.stdout)
logger = logging.getLogger(__name__)

def format_ai_output(output):
    """
    将 AI 输出的多行内容合并为单行，使用 ' | ' 作为分隔符。
    """
    return ' | '.join(line.strip() for line in output.split('\n') if line.strip())

async def translate_comment_async(comment, api_name, model_name, target_lang):
    prompt = f"请将以下我的世界插件配置文件注释翻译成{target_lang}：{comment['original_text']}"
    translation = await call_ai_api_async(api_name, model_name, prompt)
    formatted_translation = format_ai_output(translation) if translation else "翻译失败"
    return {
        "id": comment.get("id"),
        "original_text": comment["original_text"],
        "translated_text": formatted_translation,
        "location": comment["location"]
    }

async def translate_batch_async(comments, api_name, model_name, target_lang, batch_size):
    tasks = []
    for comment in comments:
        task = asyncio.create_task(translate_comment_async(comment, api_name, model_name, target_lang))
        tasks.append(task)
        
        if len(tasks) >= batch_size:
            batch_results = await asyncio.gather(*tasks, return_exceptions=True)
            for result in batch_results:
                if isinstance(result, Exception):
                    logger.error(f"Translation failed: {str(result)}")
                    yield None
                else:
                    yield result
            tasks = []
    
    if tasks:
        batch_results = await asyncio.gather(*tasks, return_exceptions=True)
        for result in batch_results:
            if isinstance(result, Exception):
                logger.error(f"Translation failed: {str(result)}")
                yield None
            else:
                yield result

async def process_translations(comments, api_name, model_name, target_lang, batch_size, progress_bar, status_text):
    translated_comments = []
    retry_comments = []
    total_comments = len(comments)
    
    async for translated_comment in translate_batch_async(comments, api_name, model_name, target_lang, batch_size):
        if translated_comment is None:
            retry_comments.append(comments[len(translated_comments)])
        else:
            translated_comments.append(translated_comment)
        
        progress = len(translated_comments) / total_comments
        if progress_bar:
            progress_bar.progress(progress)
        if status_text:
            status_text.text(f"已翻译 {len(translated_comments)}/{total_comments} 条注释 (进度: {progress:.2%})")
        logger.info(f"Translated {len(translated_comments)}/{total_comments} comments (Progress: {progress:.2%})")
    
    return translated_comments, retry_comments

def translate_comments(comments, api_name, model_name, target_lang, progress_bar=None, status_text=None, batch_size=10, max_retries=3):
    config = load_config()
    all_translated_comments = []
    remaining_comments = comments
    total_comments = len(comments)
    
    for attempt in range(max_retries):
        if not remaining_comments:
            break
        
        logger.info(f"Translation attempt {attempt + 1}/{max_retries}")
        if status_text:
            status_text.text(f"翻译尝试 {attempt + 1}/{max_retries}")
        
        async def run_translation():
            nonlocal all_translated_comments, remaining_comments
            translated, to_retry = await process_translations(remaining_comments, api_name, model_name, target_lang, batch_size, progress_bar, status_text)
            all_translated_comments.extend(translated)
            remaining_comments = to_retry
        
        asyncio.run(run_translation())
        
        if remaining_comments:
            logger.info(f"{len(remaining_comments)} comments failed to translate. Retrying...")
            if status_text:
                status_text.text(f"重新连接中... 剩余 {len(remaining_comments)} 条注释待翻译")
            asyncio.run(asyncio.sleep(5))  # 等待5秒后重试
    
    if remaining_comments:
        logger.warning(f"Failed to translate {len(remaining_comments)} comments after {max_retries} attempts")
        if status_text:
            status_text.text(f"警告：{len(remaining_comments)} 条注释翻译失败")
    
    # 确保进度条显示100%完成
    if progress_bar:
        progress_bar.progress(1.0)
    if status_text:
        status_text.text(f"翻译完成: {len(all_translated_comments)}/{total_comments} 条注释已翻译")
    
    logger.info(f"Translation completed. {len(all_translated_comments)}/{total_comments} comments translated.")
    
    return all_translated_comments
