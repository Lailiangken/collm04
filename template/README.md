# Agent Configuration Templates

このディレクトリには各種エージェントの設定テンプレートが含まれています。

## AssistantAgent.json

AssistantAgentの設定パラメータの説明:

| パラメータ | 説明 | 型 |
|------------|------|-----|
| name | エージェントの一意の識別名 | string |
| system_message | エージェントの基本的な振る舞いを定義するシステムメッセージ | string |
| description | エージェントの役割と専門性の説明 | string |
| model_client_stream | モデルの応答をストリーミングで受け取るかどうか | boolean |
| reflect_on_tool_use | ツール使用後に結果を分析して新しい推論を生成するかどうか | boolean |
| tool_call_summary_format | ツール実行結果の出力フォーマット。利用可能な変数: {tool_name}, {arguments}, {result} | string |
| tools | エージェントが使用可能なツールのリスト | array |
| handoffs | 他のエージェントへの引き継ぎ設定のリスト | array |
| model_context | モデルのコンテキスト管理設定 | object |
| model_client | 使用するLLMモデルの設定 | object |

### model_client設定

| パラメータ | 説明 | 型 |
|------------|------|-----|
| type | モデルクライアントの種類（例: OpenAIChatCompletionClient） | string |
| model | 使用するモデル名 | string |
| temperature | 生成時の温度パラメータ（0-1） | number |
| parallel_tool_calls | ツール呼び出しを並列実行するかどうか | boolean |

## 使用方法

1. 必要に応じてテンプレートをコピーして新しい設定ファイルを作成
2. パラメータを目的に合わせて調整
3. load_agents.pyを使用して設定を読み込み

## 設定例


{
    "name": "developer",
    "system_message": "プログラマーとして、技術的な実装の詳細を提案してください。When you done with generating the program, reply with TERMINATE.",
    "description": "A technical developer who specializes in implementation details and coding solutions",
    "model_client_stream": true,
    "reflect_on_tool_use": true,
    "tool_call_summary_format": "{tool_name}: {result}",
    "tools": [],
    "handoffs": [],
    "model_context": {
        "type": "UnboundedChatCompletionContext",
        "messages": []
    },
    "model_client": {
        "type": "OpenAIChatCompletionClient",
        "model": "gpt-4",
        "temperature": 0.7,
        "parallel_tool_calls": true
    }
}

