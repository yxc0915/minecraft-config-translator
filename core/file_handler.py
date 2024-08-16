import json

def save_json(data, filename):
    """
    将数据保存为 JSON 文件
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def merge_translations(file_content, translated_comments, chinese_only=False):
    """
    将翻译后的注释合并回原始文件内容
    
    :param file_content: 原始文件内容
    :param translated_comments: 翻译后的注释列表
    :param chinese_only: 是否只保留中文翻译
    :return: 合并后的文件内容
    """
    lines = file_content.split('\n')
    for comment in translated_comments:
        line_num = comment["location"]["line"] - 1
        before_comment = comment["location"]["before_comment"]
        original = comment["original_text"]
        translation = comment["translated_text"]
        
        if chinese_only:
            lines[line_num] = f"{before_comment}# {translation}"
        else:
            lines[line_num] = f"{before_comment}# {original} | {translation}"
    
    return '\n'.join(lines)

def load_json(filename):
    """
    从 JSON 文件加载数据
    """
    with open(filename, 'r', encoding='utf-8') as f:
        return json.load(f)
