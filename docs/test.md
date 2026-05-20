## テスト設計書

## 1. 目的
本テスト設計書は、学習記録・目標設定アプリの品質を担保するために、単体テストおよび結合テストの観点・範囲・方法を定義する。
API・DB・ビジネスロジックの整合性を確認し、機能追加時のリグレッション防止を目的とする。

---

## 2. 対象範囲

### 2.1 API機能（結合テスト対象）
- 学習記録一覧取得・新規作成（GET/POST `/api/study-records`）
- 学習記録詳細取得・更新・削除（GET/PUT/DELETE `/api/study-records/{id}`）
- 学習記録日付検索（GET `/api/study-records/date/{study_date}`）
- 目標設定一覧取得・新規作成（GET/POST `/api/study-goals`）
- 目標設定詳細取得・更新・削除（GET/PUT/DELETE `/api/study-goals/{id}`）
- 進捗状況集計（GET `/api/study-records/progress`）

### 2.2 ビジネスロジック（単体テスト対象）
- 総学習時間の集計処理（SUM）
- 目標設定に基づく達成率計算ロジック（0除算・目標未設定時のハンドリング含む）

### 2.3 DB操作
- SQLAlchemyを用いたSQLite（in-memory）へのCRUD処理
- テーブル制約（NOT NULL / 型バリデーション）の検証

---

## 3. テスト種別

### 3.1 単体テスト（Unit Test）
#### 目的
FastAPIや外部接続から切り離し、純粋な集計・計算ロジックの正しさを関数単位で検証する。
#### 例
- 目標設定が存在しない場合、達成率が `0.0` として安全に返ること。
- 目標時間が `0` の場合、0除算エラーを起こさずに `0.0` が返ること。

### 3.2 結合テスト（Integration Test）
#### 目的
FastAPIエンドポイント、Pydanticスキーマ、SQLAlchemyセッションが連携し、HTTPリクエストに対してDBが正しく不整合なく操作されるかを確認する。
#### 例
- POST実行後、自動採番された `id` を含むレスポンスが201で返ること。
- データを削除した後、同じIDでGETリクエストを送ると正しく404エラーになること。

---

## 4. テスト観点

### 4.1 正常系
- 各リソース（記録・目標）の作成・取得・更新・削除が期待通りのステータスコード（200/201）で成功すること。

### 4.2 異常系
- 存在しないIDに対する更新・削除・取得リクエストが適切に `404 Not Found` になること。
- Pydanticのバリデーション制約（空文字、文字数超過、負の学習時間など）に違反した際、適切に `422 Unprocessable Entity` になること。

---

## 5. テストデータ設計
- **データの独立性:** 各テストケースは独立したトランザクションで実行され、終了時に自動的にロールバック（リセット）される。
- **データ干渉の防止:** テスト間でのデータ干渉を一切排除し、常にクリーンな状態から検証を開始する。

---

## 6. テスト環境
- **Language:** Python 3.12
- **Framework:** pytest
- **HTTP Client:** FastAPI TestClient (starlette)
- **ORM:** SQLAlchemy
- **Test DB:** SQLite (in-memory)

---

## 7. モック方針
- **DB操作:** モック化せず、インメモリのSQLiteを用いて実際のクエリを発行して担保する。
- **FastAPI依存関係:** `Depends(get_db)` を、テスト用に用意した自動ロールバック機能付きのSQLiteセッションへと強制的に上書き（dependency_overrides）する。

---

## 8. テスト構成（実際のディレクトリ構造）

プロジェクトで実際に構築した完全なテスト配置は以下の通りである。

```text
study_records/
├── backend/
│   └── app/
│       ├── main.py                    # アプリ本体
│       ├── database/database.py       # Base, engine定義
│       ├── models/                    # ORMモデル定義
│       ├── routers/                   # APIエンドポイント
│       └── schemas/                   # Pydanticバリデーション
└── tests/
    ├── conftest.py                    # 【最重要】インメモリDB・Clientのセットアップ、モデル強制登録
    ├── unit/
    │   └── test_progress.py           # Progress集計ロジックの単体テスト（3ケース）
    └── integration/
        ├── test_api_study_record.py   # 学習記録APIの結合テスト（8ケース）
        └── test_api_study_goal.py     # 目標設定APIの結合テスト（6ケース）