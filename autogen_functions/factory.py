from .code_generator.generator import CodeGeneratorFunction
from .code_review.reviewer import CodeReviewFunction
from .code_generator_group.generator_group import GroupChatGenerator
from .group_common.generator_group import CommonGroupChatGenerator

AVAILABLE_FUNCTIONS = {
    'コードレビュー': CodeReviewFunction,
    'コード生成': CodeGeneratorFunction,
    'グループコード生成': GroupChatGenerator,
    'グループチャット': CommonGroupChatGenerator
}

def get_available_functions():
    """
    利用可能な機能の一覧を返す
    
    Returns:
        dict: 機能名とクラスの対応辞書
    """
    return AVAILABLE_FUNCTIONS

def create_llm_function(function_type: str):
    """
    機能タイプに応じたLLM機能クラスを返す
    
    Args:
        function_type: 機能の種類
    Returns:
        対応するクラス
    """
    return AVAILABLE_FUNCTIONS.get(function_type) 