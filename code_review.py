import os
from pathlib import Path
from autogen_functions.code_review.llm_function import CodeReviewFunction

def review_code(file_path: str) -> str:
    """
    指定されたPythonファイルのコードレビューを実行します
    
    Args:
        file_path: レビュー対象のPythonファイルパス
    """
    # ファイルの存在確認
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
        
    # コードの読み込み
    with open(file_path, 'r', encoding='utf-8') as f:
        code = f.read()
        
    # レビュー実行
    reviewer = CodeReviewFunction()
    result = reviewer(code)
    
    return result

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python code_review.py <path_to_python_file>")
        sys.exit(1)
        
    file_path = sys.argv[1]
    result = review_code(file_path)
    print(result)
