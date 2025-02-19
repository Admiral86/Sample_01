```mermaid
graph LR
    %% アクター
    User((ユーザー))

    %% メインユースケース
    UC1[タスクを追加]
    UC2[タスク一覧を表示]
    UC3[タスクを完了]
    UC4[タスクを削除]

    %% サブユースケース
    SUB1[タスク入力を検証]
    SUB2[タスクの選択を確認]
    SUB3[削除の確認]
    SUB4[データベースに保存]

    %% アクターとユースケースの関連
    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4

    %% includeの関連
    UC1 -.-> SUB1
    UC1 -.-> SUB4
    UC3 -.-> SUB2
    UC3 -.-> SUB4
    UC4 -.-> SUB2
    UC4 -.-> SUB3
    UC4 -.-> SUB4

    %% スタイル設定
    classDef actor fill:#f9f,stroke:#333,stroke-width:2px
    classDef usecase fill:#bbf,stroke:#333,stroke-width:2px
    classDef subcase fill:#ddf,stroke:#333,stroke-width:1px

    class User actor
    class UC1,UC2,UC3,UC4 usecase
    class SUB1,SUB2,SUB3,SUB4 subcase

    %% 注釈
    subgraph 注釈
        note1[タスク名を入力して「追加」ボタンをクリック]
        note2[タスクを選択して「完了」ボタンをクリック]
        note3[タスクを選択して「削除」ボタンをクリック]
        note4[SQLiteデータベースにタスク情報を永続化]
    end

    UC1 --- note1
    UC3 --- note2
    UC4 --- note3
    SUB4 --- note4
```

## ユースケース図の説明

### アクター
- ユーザー：システムを利用する人

### メインユースケース
1. タスクを追加
   - タスク名を入力して新しいタスクを作成
2. タスク一覧を表示
   - 登録されているタスクの一覧を表示
3. タスクを完了
   - 選択したタスクを完了状態に変更
4. タスクを削除
   - 選択したタスクをシステムから削除

### サブユースケース（<<include>>）
1. タスク入力を検証
   - 入力値の妥当性をチェック
2. タスクの選択を確認
   - タスクが選択されているか確認
3. 削除の確認
   - 削除前に確認ダイアログを表示
4. データベースに保存
   - タスク情報をSQLiteに永続化 