# Model Configuration

`model_config.json`の設定パラメータについて説明します。

## 基本設定

| パラメータ | 説明 | 型 | デフォルト値 |
|------------|------|-----|-------------|
| model | 使用するモデルの名称 (例: gpt-4, gpt-3.5-turbo など) | string | 必須 |
| api_key | OpenAI APIキー | string | 環境変数から取得 |

## モデル機能設定

| パラメータ | 説明 | 型 | デフォルト値 |
|------------|------|-----|-------------|
| vision | 画像処理機能の有効/無効 | boolean | false |
| function_calling | 関数呼び出し機能の有効/無効 | boolean | true |
| json_output | JSON形式出力の有効/無効 | boolean | true |
| family | モデルファミリー (GPT_4, GPT_35, O1 など) | string | "GPT_4" |

## 生成パラメータ

| パラメータ | 説明 | 型 | デフォルト値 |
|------------|------|-----|-------------|
| temperature | 生成テキストの多様性 (0.0-1.0) | float | 0.7 |
| max_tokens | 生成する最大トークン数 | integer | 2000 |

## 設定例

```json
{
    "model": "gpt-4",
    "vision": false,
    "function_calling": true,
    "json_output": true,
    "family": "GPT_4",
    "api_key": "your-api-key",
    "temperature": 0.7,
    "max_tokens": 2000
}
