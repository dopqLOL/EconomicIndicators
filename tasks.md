# GoldEventAnalyzer 開発タスクリスト

## 優先度 高

-   [x] **基本的なプロジェクト構造の定義 (MVVM)**
    -   [x] `ui` パッケージ作成 (画面関連)
    -   [x] `data` パッケージ作成 (データアクセス、リポジトリ)
    -   [x] `domain` パッケージ作成 (ビジネスロジック、ユースケース)
    -   [x] `di` パッケージ作成 (依存性注入: Hilt/Koin導入時)
-   [x] **依存ライブラリの追加 (`build.gradle(:app)`)**
    -   [x] ViewModel (`androidx.lifecycle:lifecycle-viewmodel-ktx`)
    -   [x] Coroutines (`org.jetbrains.kotlinx:kotlinx-coroutines-android`)
    -   [x] Compose 基本 (`androidx.compose.ui:ui`, `androidx.compose.material3:material3`, `androidx.compose.ui:ui-tooling-preview`)
    -   [x] Compose ViewModel (`androidx.lifecycle:lifecycle-viewmodel-compose`)
    -   [x] Compose Activity (`androidx.activity:activity-compose`)
    -   [x] Webアクセス: Ktor Client (`io.ktor:ktor-client-android`, `io.ktor:ktor-client-content-negotiation`, `io.ktor:ktor-serialization-kotlinx-json`)
    -   [ ] (検討) データ永続化: DataStore (`androidx.datastore:datastore-preferences`) または Room
    -   [x] JUnit (`junit:junit`)
-   [x] **UI骨格の実装 (Compose) - メイン画面**
    -   [x] `ui/eventlist` パッケージ作成
    -   [x] `EventListScreen.kt` 作成 (`@Composable EventListScreen`)
    -   [x] `LazyColumn` でダミーデータを表示する仮実装
-   [x] **データ取得機能の実装 - kissfx.com**
    -   [x] Webアクセスライブラリ決定・導入 (Ktor or Retrofit) - Ktor決定済、導入はbuild.gradle編集済
    -   [x] `data` レイヤー: `EconomicEventRepository` (Interface) とその実装クラス作成
    -   [x] `data` レイヤー: `KissFxDataSource` (Webスクレイピング/APIアクセス) 作成 (Jsoup or Ktor/Retrofit)
    -   [x] `ui/eventlist` パッケージ: `EventListViewModel.kt` 作成
    -   [x] ViewModel で Coroutine を使用し Repository 経由でデータ取得
    -   [x] `StateFlow` でUI向けの状態 (読み込み中、成功、エラー) とイベントリストを管理
-   [x] **UIとViewModelの連携 - メイン画面**
    -   [x] `EventListScreen` で `EventListViewModel` の `StateFlow` を収集 (`collectAsState` を使用)
    -   [x] 状態に応じてローディング表示、エラー表示、イベントリスト表示を切り替え
    -   [x] 取得データを `LazyColumn` に表示 (初期は単純なテキスト表示)

## 経済指標の価格変動特性分析とカテゴライズ支援ツールの開発

-   [ ] **データ準備と時間帯別ボラティリティ計算 (データ1作成)**
    -   [ ] 経済指標データ (`economic_indicators_*.csv`) から時刻・国・指標名を読み込み、前処理を行う。
    -   [x] 3つのZigZagデータ (`mt5_zigzag_legs_*.csv`) を読み込み、結合・前処理を行う。 (`Python/calculate_intraday_volatility.py` で対応済)
    -   [x] 定義済み時間帯（例: 07-09時, 09-12時等）ごとにZigZagデータからボラティリティ（高値-安値）を計算する。 (`Python/calculate_intraday_volatility.py` で対応済)
    -   [ ] 各経済指標が発表された時間帯を特定し、対応するボラティリティを指標データに紐付ける。
-   [ ] **指標別ボラティリティ統計量の集計 (データ2作成の主要部分)**
    -   [ ] 上記でボラティリティが紐付けられた経済指標データを「国名」と「指標名」でグループ化する。
    -   [ ] 各グループのボラティリティについて、平均値、中央値、標準偏差、最小値、最大値、データ件数等の統計量を計算する。
-   [ ] **仮3分類カテゴリ別平均ボラティリティの集計 (データ2の補足部分)**
    -   [ ] 上記で計算した「指標ごとの平均ボラティリティ」を基準に、全指標を機械的に「仮・大」「仮・中」「仮・小」の3カテゴリに分類する（例: 三分位数を使用）。
    -   [ ] 各仮分類カテゴリに属する指標のボラティリティの平均値を計算する。
-   [ ] **集計結果表示Webアプリケーションの開発とデプロイ (データ2表示)**
    -   [ ] 「指標別ボラティリティ統計量」および「仮3分類カテゴリ別平均ボラティリティ」を表示・ソート・フィルタリングできるWebアプリケーションを開発する (Streamlit推奨)。
    -   [ ] 開発したWebアプリケーションをデプロイする。
-   [ ] **ユーザーによるデータ探索と指標カテゴライズ基準の策定**
    -   [ ] デプロイされたWebアプリケーション（指標別ボラティリティ統計量）を使用し、ユーザーがデータを探索・分析する。
    -   [ ] ユーザーが経済指標の「大・中・小」のカテゴライズ基準を定義する。

## 優先度 中

-   [ ] **UI骨格の実装 (Compose) - 設定画面**
    -   [ ] `ui/settings` パッケージ作成
    -   [ ] `SettingsScreen.kt` 作成 (`@Composable SettingsScreen`)
    -   [ ] 市場ボラティリティ選択UI (`RadioButton` 等) の仮実装
-   [ ] **設定機能の実装**
    -   [ ] データ永続化ライブラリ決定・導入 (DataStore or Room)
    -   [ ] `data` レイヤー: `SettingsRepository` (Interface) とその実装クラス作成 (DataStore/Room使用)
    -   [ ] `ui/settings` パッケージ: `SettingsViewModel.kt` 作成
    -   [ ] ViewModel で設定値の読み込み・保存処理を実装
    -   [ ] `SettingsScreen` と `SettingsViewModel` を連携
-   [ ] **過去データ読み込み機能の実装**
    -   [ ] 過去データ形式決定 (例: アプリ内アセットに配置するCSV)
    -   [ ] `data` レイヤー: `PastPriceDataRepository` (Interface) とその実装クラス作成 (アセット読み込み等)
    -   [ ] 関連する ViewModel で読み込み処理を呼び出し
-   [ ] **分析ロジックの実装**
    -   [ ] `domain` レイヤー: `CalculateVolatilityUseCase` など、分析ロジックを持つクラスを作成
    -   [ ] イベントデータと過去データを基に変動幅・方向性などを計算
    -   [ ] ユーザー設定（市場ボラティリティ）を考慮したボラティリティ分類ロジック
    -   [ ] ViewModel から UseCase を呼び出し、分析結果を `StateFlow` で管理
-   [ ] **UIとViewModelの連携 - 分析結果表示**
    -   [ ] `EventListScreen` の各リストアイテム用 `@Composable` 関数 (`EventListItem`) を作成・詳細化
    -   [ ] `EventListItem` で分析結果（変動幅、ボラティリティ分類、傾向）を表示
    -   [ ] 時間帯別変動幅も表示

## 優先度 低

-   [ ] **UI改善**
    -   [ ] `EventListItem` で重要度に応じた視覚的区別（アイコン、色等）
    -   [ ] メイン画面に手動更新機能 (`SwipeRefreshLayout` の Compose 版等) を追加
    -   [ ] (任意) Compose Navigation を導入し、イベントタップで詳細画面へ遷移
    -   [ ] 詳細画面 (`EventDetailScreen`) の実装
-   [ ] **テスト**
    -   [ ] ViewModel の単体テスト (JUnit + Turbine/Coroutines Test)
    -   [ ] Repository/DataSource の単体テスト (JUnit + MockK/Mockito)
    -   [ ] UseCase の単体テスト (JUnit)
    -   [ ] Compose UI テスト (基本的な画面表示・インタラクション)
-   [ ] **README.md の詳細化**
    -   [ ] ビルド手順、実行方法を追記
    -   [ ] ライブラリ、アーキテクチャについての説明を追加
-   [ ] **エラーハンドリング改善**
    -   [ ] より具体的なエラーメッセージ表示
    -   [ ] オフライン時の挙動定義と実装
-   [ ] **コードリファクタリングと最適化**
    -   [ ] 再コンポジションの最適化
    -   [ ] 可読性・保守性の向上

## その他・メモ

- Pythonスクレイパー関連の管理:
    - 2024/XX/XX: 過去に誤って作成されたリモートブランチ `origin/feature/add-date-arg-to-scraper` を削除。
    - 2024/XX/XX: Pythonスクレイパー関連の作業ブランチとして `feature/python-scraper` をローカルで作成・作業し、シークレットファイル (`firebasePython/goldeventanalyzer-firebase-adminsdk-fbsvc-bad0029e0d.json`) を `.gitignore` で管理対象外とした上でリモート (`origin/feature/python-scraper`) へプッシュ完了。 