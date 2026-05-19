# テーブル定義

## study_records

|カラム名|型|NULL|PK|説明|
|---|---|---|---|---|
|id|BIGINT|NO|YES|学習記録ID|
|title|VARCHAR(255)|NO|NO|学習タイトル|
|content|TEXT|NO|NO|学習内容|
|study_minutes|INT|NO|NO|学習時間（分）|
|study_date|DATE|NO|NO|学習日|
|memo|TEXT|YES|NO|メモ|
|created_at|DATETIME|NO|NO|作成日時|
|updated_at|DATETIME|NO|NO|更新日時|


## study_goals

|カラム名|型|NULL|PK|説明|
|---|---|---|---|---|
|id|BIGINT|NO|YES|目標ID|
|goal_type|VARCHAR(20)|NO|NO|目標種別（日次/月次）|
|target_minutes|INT|NO|NO|目標学習時間|
|start_date|DATE|NO|NO|開始日|
|end_date|DATE|NO|NO|終了日|
|created_at|DATETIME|NO|NO|作成日時|
|updated_at|DATETIME|NO|NO|更新日時|