from .code_generator.generator import CodeGeneratorFunction
from .code_review.reviewer import CodeReviewFunction

def create_llm_function(function_type: str):
    """
    機能タイプに応じたLLM機能クラスを返す
    
    Args:
        function_type: 機能の種類（'コードレビュー' or 'コード生成'）
    Returns:
        対応するクラス
    """
    functions = {
        'コードレビュー': CodeReviewFunction,
        'コード生成': CodeGeneratorFunction
    }
    return functions.get(function_type)   