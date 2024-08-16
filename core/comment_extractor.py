def extract_comments(file_content):
    comments = []
    for i, line in enumerate(file_content.split('\n'), 1):
        if '#' in line:
            before_comment, comment = line.split('#', 1)
            comment = comment.strip()
            if comment:
                comments.append({
                    "original_text": comment,
                    "location": {"line": i, "before_comment": before_comment}
                })
    return comments
