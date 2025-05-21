# 経済指標ボラティリティ分析ツール

このプロジェクトは、経済指標データとZigZagデータを紐付けて分析し、経済指標のボラティリティ特性を調査するためのツールです。

## プロジェクト概要

このプロジェクトは以下のステップで経済指標の価格変動特性を分析します：

1. **データ収集**：
   - MT5からMQL5スクリプトで経済指標データを取得
   - MT5からZigZagデータを取得

2. **データ前処理**：
   - 時間帯別ボラティリティの計算
   - 経済指標データとボラティリティデータの紐付け

3. **データ分析**：
   - 経済指標別のボラティリティ統計量の計算
   - ボラティリティに基づく経済指標の「大・中・小」カテゴリ分類

4. **データ可視化**：
   - Streamlitを使用したインタラクティブな分析ツール
   - ソート・フィルタリング機能付きデータ表示

## 主要コンポーネント

このプロジェクトは以下の主要コンポーネントから構成されています：

### 1. データ収集 (MQL5スクリプト)

- `mql5/EconomicIndicatorsExport.mq5`：経済指標データをCSV形式でエクスポート
- `mql5/ZigZagExport.mq5`：ZigZagデータをCSV形式でエクスポート

### 2. データ処理 (Pythonスクリプト)

- `Python/calculate_intraday_volatility.py`：時間帯別ボラティリティの計算
- `Python/merge_indicators_with_volatility.py`：経済指標データとボラティリティデータの紐付け
- `Python/calculate_indicator_statistics.py`：指標別ボラティリティ統計量の計算

### 3. データ可視化 (Streamlitアプリ)

- `Python/indicator_statistics_app.py`：経済指標ボラティリティ分析用Streamlitアプリ

## データファイル

このプロジェクトでは以下のディレクトリ構造でデータを管理しています：

- `csv/EconomicIndicators/`：経済指標データ (UTC時刻)
- `csv/Zigzag-data/`：ZigZagデータ
- `csv/CalculatedVolatility/`：時間帯別ボラティリティデータ
- `csv/MergedData/`：経済指標とボラティリティを紐付けたデータ
- `csv/Statistics/`：経済指標別ボラティリティ統計量
- `plots/`：生成した可視化図表

## 進捗状況

このプロジェクトは以下のタスクを完了しています：

- ✅ 時間帯別ボラティリティの計算
- ✅ 経済指標データとボラティリティデータの紐付け
- ✅ 指標別ボラティリティ統計量の計算
- ✅ 「大・中・小」カテゴリへの機械的分類
- ✅ Streamlitベースの分析アプリケーション開発

現在進行中：
- ⬜ Streamlitアプリケーションのデプロイ
- ⬜ ユーザーによるデータ探索と指標カテゴライズ基準の策定

## 使用方法

### 1. 必要条件

- Python 3.8以上
- 必要なPythonパッケージ：pandas, numpy, matplotlib, seaborn, streamlit, pillow, pytz

必要なパッケージのインストール：
```bash
pip install -r Python/requirements.txt
```

### 2. データ処理

各スクリプトを以下の順序で実行します：

```bash
# 1. ZigZagデータから時間帯別ボラティリティを計算
python Python/calculate_intraday_volatility.py

# 2. 経済指標データとボラティリティデータを紐付け
python Python/merge_indicators_with_volatility.py

# 3. 経済指標別ボラティリティ統計量を計算
python Python/calculate_indicator_statistics.py
```

### 3. Streamlitアプリの起動

```bash
streamlit run Python/indicator_statistics_app.py
```

ブラウザで`http://localhost:8501`にアクセスして分析ツールを使用できます。

## 分析結果

現在の分析では以下のような結果が得られています：

- **データ量**：89,019件の経済指標データのうち86,853件（97.57%）に有効なボラティリティデータが紐付けられました
- **通貨別分布**：USD（22,835件）とEUR（19,562件）が最も多く存在
- **ボラティリティ**：HKDが最も高いボラティリティ平均値（16.941）を示しています
- **カテゴリ分類**：ボラティリティに基づき指標を「大・中・小」に三分位数を使用して分類

## ライセンス

このプロジェクトは[MIT License](LICENSE)のもとで配布されています。

## 謝辞

このプロジェクトは、MQL5およびMetaTrader 5プラットフォームを利用して開発されました。 