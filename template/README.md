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
| tool_call_summary_format | ツール実行結果の出力フォーマット。利用可能な変数: {tool_name}, {result} | string |

## 使用方法

1. 必要に応じてテンプレートをコピーして新しい設定ファイルを作成
2. パラメータを目的に合わせて調整
3. load_agents.pyを使用して設定を読み込み

## 設定例

```json
{
    "name": "developer",
    "system_message": "プログラマーとして、技術的な実装の詳細を提案してください。",
    "description": "A technical developer who specializes in implementation details",
    "model_client_stream": true,
    "reflect_on_tool_use": true,
    "tool_call_summary_format": "{tool_name}: {result}"
}
