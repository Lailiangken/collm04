
def goal_setting_info(query: str) -> str:
    """目標設定に関する情報を検索する関数
    
    Args:
        query (str): 検索クエリ
        
    Returns:
        str: 検索結果
    """
    result = "営業Level3の目標は、売上1000円を達成することです。"
    return result


def speciality_guide_info(query: str) -> str:
    """専門性ガイドに関する情報を検索する関数
    
    Args:
        query (str): 検索クエリ
        
    Returns:
        str: 検索結果
    """
    result = "営業Level3の目標は、売上1000円を達成することです。"
    return result

if __name__ == "__main__":
    query = "目標設定に関する情報を取得してください。"
    result = goal_setting_info(query)
    print(result)
