import aiohttp
from aiohttp_socks import ProxyConnector, ProxyType
import asyncio
from yarl import URL
from core.config_loader import load_config

def get_proxy_connector(proxy_url):
    if not proxy_url:
        return None
    
    url = URL(proxy_url)
    if url.scheme in ['http', 'https']:
        return ProxyConnector.from_url(proxy_url)
    elif url.scheme == 'socks5':
        return ProxyConnector(
            proxy_type=ProxyType.SOCKS5,
            host=url.host,
            port=url.port
        )
    else:
        raise ValueError(f"Unsupported proxy scheme: {url.scheme}")

async def call_ai_api_async(api_name, model_name, prompt, max_retries=3, retry_delay=5):
    config = load_config()
    api_config = config['apis'][api_name]
    proxy_url = config.get('proxy', {}).get('url')
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_config['api_key']}"
    }
    
    data = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": "你是一位专业的我的世界插件配置文件翻译专家，你正在翻译配置文件中带#的注释部分内容，你只需要输出翻译后的内容，不要附上自己的猜想。如果遇到带有#的RGB颜色代码，请不要翻译，直接返回原内容。注意纯大写的文本如 LOWEST, LOW, NORMAL, HIGH, HIGHEST，请不要翻译，它们可能是供参考的配置选项。"},
            {"role": "user", "content": prompt}
        ]
    }
    
    connector = get_proxy_connector(proxy_url)

    async with aiohttp.ClientSession(connector=connector) as session:
        for attempt in range(max_retries):
            try:
                async with session.post(api_config['base_url'], headers=headers, json=data, timeout=30) as response:
                    response.raise_for_status()
                    result = await response.json()
                    return result['choices'][0]['message']['content'].strip()
            except aiohttp.ClientError as e:
                if attempt < max_retries - 1:
                    print(f"API 调用失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}. 正在重试...")
                    await asyncio.sleep(retry_delay)
                else:
                    print(f"API 调用失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}. 已达到最大重试次数。")
                    return None
