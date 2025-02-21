import json
import os
from datetime import datetime

def save_chat_settings(settings: dict):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    save_dir = 'saved_settings'
    os.makedirs(save_dir, exist_ok=True)
    
    filename = f'chat_settings_{timestamp}.json'
    filepath = os.path.join(save_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)
    
    return filepath
