# Tomario Hotel - アプリケーション

ホテル予約システム「Tomario Hotel」のバックエンド・フロントエンドアプリケーションです。  
インフラ（EC2 / ALB / RDS）は [tomario-infra](https://github.com/Tomario-portfolio/tomario-infra) リポジトリで管理しています。

---

## 技術スタック

| レイヤー | 技術 |
|---|---|
| バックエンド | Python / Flask |
| フロントエンド | HTML / CSS / JavaScript（Jinja2 テンプレート） |
| データベース | MySQL 8.0（AWS RDS） |
| 認証 | Flask-Login（セッション管理） |

---

## 機能一覧

- ユーザー登録 / ログイン / ログアウト
- 客室一覧・詳細表示
- チェックイン・アウト日による空き部屋検索
- 予約登録（宿泊日数に応じた合計金額自動計算）
- 予約確認・キャンセル

---

## ディレクトリ構成

```
tomario-app/
├── app.py                  # Flask アプリ本体（ルーティング・DB モデル・ビジネスロジック）
├── requirements.txt        # Python 依存パッケージ
├── schema.sql              # DB テーブル定義・初期データ投入
├── .env.example            # 環境変数テンプレート（実際の .env は Git 管理外）
├── .gitignore
├── templates/              # Jinja2 HTML テンプレート
│   ├── base.html           # 共通レイアウト（ヘッダー・フッター・フラッシュメッセージ）
│   ├── index.html          # トップページ（空き部屋検索フォーム）
│   ├── login.html          # ログインフォーム
│   ├── register.html       # ユーザー登録フォーム
│   ├── rooms.html          # 客室一覧・空き部屋検索結果
│   ├── room_detail.html    # 客室詳細
│   ├── booking.html        # 予約フォーム（合計金額リアルタイム計算）
│   └── my_bookings.html    # 予約確認・キャンセル
└── static/
    ├── css/
    │   └── style.css       # 全ページ共通スタイル
    └── js/
        └── main.js         # 日付入力バリデーション（過去日・逆順の防止）
```

---

## 環境変数

`.env.example` をコピーして `.env` を作成し、各値を設定してください。

```bash
cp .env.example .env
```

| 変数名 | 説明 |
|---|---|
| `SECRET_KEY` | Flask セッション署名用キー（ランダムな文字列を設定） |
| `DB_HOST` | RDS エンドポイント |
| `DB_PORT` | DB ポート（デフォルト: 3306） |
| `DB_NAME` | データベース名（`tomario`） |
| `DB_USER` | DB ユーザー名 |
| `DB_PASSWORD` | DB パスワード |

---

## DB セットアップ

RDS に接続して `schema.sql` を流します。

```bash
mysql -h <RDSエンドポイント> -u admin -p < schema.sql
```

`schema.sql` の内容：
- `users` テーブル（ユーザー情報）
- `rooms` テーブル（客室情報）
- `bookings` テーブル（予約情報）
- 客室サンプルデータ 5 件（シングル×2 / ダブル×2 / スイート×1）

---

## ローカル起動

```bash
# 依存パッケージインストール
pip install -r requirements.txt

# 起動（ポート 8080）
python app.py
```

ブラウザで `http://localhost:8080` にアクセス。

---

## EC2 デプロイ

```bash
# EC2 にログイン
ssh -i <キーペア> ec2-user@<EC2のIP>

# リポジトリをクローン
git clone https://github.com/Tomario-portfolio/tomario-app.git
cd tomario-app

# パッケージインストール
pip install -r requirements.txt

# 環境変数設定
cp .env.example .env
vi .env  # 各値を入力

# 起動
python app.py
```

ALB のターゲットグループがポート 8080 を向いているため、ALB の DNS 名でアクセスできます。

---

## インフラ構成

インフラは別リポジトリ [tomario-infra](https://github.com/Tomario-portfolio/tomario-infra) で Terraform 管理しています。

```
Internet → ALB（ポート 80）→ EC2（ポート 8080）→ RDS MySQL
```
