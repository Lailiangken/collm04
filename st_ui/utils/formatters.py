def format_task_result(task_result):
    md_output = "# 会話履歴\n\n"
    last_message = "# 結果\n\n"
    
    for message in task_result.messages:
        md_output += f"## {message.source.capitalize()}\n"
        md_output += f"{message.content}\n\n"
        last_message_content = f"{message.content}"
    last_message = last_message + last_message_content
    return md_output, last_message
