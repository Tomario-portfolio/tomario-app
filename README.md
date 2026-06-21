# tomario-app

ホテル予約システム「Tomario Hotel」のバックエンド（Flask REST API）とフロントエンド（静的 HTML）のリポジトリです。

インフラ（EC2 / ALB / RDS / CloudFront / S3）は [tomario-infra](https://github.com/Tomario-portfolio/tomario-infra) で管理しています。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| バックエンド | Python / Flask（REST API） |
| フロントエンド | HTML / CSS / JavaScript（静的ファイル） |
| データベース | MySQL 8.0（AWS RDS） |
| 認証 | Flask-Login（セッション Cookie） |

---

## アーキテクチャ

```
ユーザー
  ↓ HTTPS
CloudFront
  ├── /*     → S3（静的ファイル: HTML/CSS/JS）
  └── /api/* → ALB → EC2（Flask API）→ RDS（MySQL）
```

フロントエンドと API は CloudFront で同一オリジンとして配信するため、クロスオリジン問題なしにセッション Cookie が機能します。

---

## ディレクトリ構成

```
tomario-app/
├── app.py              # Flask REST API（ルーティング・DBモデル・ビジネスロジック）
├── requirements.txt    # Python 依存パッケージ
├── schema.sql          # DB テーブル定義・初期データ
└── frontend/           # S3 にアップロードする静的ファイル
    ├── index.html          # トップページ
    ├── login.html          # ログイン
    ├── register.html       # ユーザー登録
    ├── rooms.html          # 客室一覧・空き部屋検索
    ├── room_detail.html    # 客室詳細
    ├── booking.html        # 予約フォーム
    ├── my_bookings.html    # 予約確認・キャンセル
    ├── css/
    │   └── style.css
    └── js/
        ├── api.js      # API 通信・認証ユーティリティ
        └── main.js     # 各ページの UI ロジック
```

---

## API エンドポイント

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/health` | ヘルスチェック（ALB 用） |
| POST | `/api/auth/login` | ログイン |
| POST | `/api/auth/logout` | ログアウト |
| POST | `/api/auth/register` | ユーザー登録 |
| GET | `/api/auth/me` | ログイン中ユーザー情報取得 |
| GET | `/api/rooms` | 客室一覧（`?check_in=&check_out=` で空き部屋検索） |
| GET | `/api/rooms/<id>` | 客室詳細 |
| POST | `/api/bookings` | 予約作成 |
| GET | `/api/bookings` | 自分の予約一覧 |
| DELETE | `/api/bookings/<id>` | 予約キャンセル |

---

## 機能

- ユーザー登録 / ログイン / ログアウト
- 客室一覧・詳細表示（客室画像付き）
- チェックイン・アウト日による空き部屋検索
- 予約作成（宿泊日数に応じた合計金額自動計算）
- 予約確認・キャンセル

---

## 環境変数

EC2 上では `user_data` が自動生成します。ローカル実行時は `.env` を手動作成してください。

| 変数名 | 説明 |
|---|---|
| `SECRET_KEY` | Flask セッション署名用キー |
| `DB_HOST` | RDS エンドポイント |
| `DB_PORT` | DB ポート（デフォルト: 3306） |
| `DB_NAME` | データベース名（`tomario`） |
| `DB_USER` | DB ユーザー名 |
| `DB_PASSWORD` | DB パスワード |

---

## ローカル起動

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:8080
```

フロントエンドは `frontend/` を任意の HTTP サーバーで配信してください。

```bash
cd frontend
python3 -m http.server 3000
# → http://localhost:3000
```

---

## フロントエンドのデプロイ（S3）

```bash
aws s3 sync frontend/ s3://<バケット名>/ --region ap-northeast-1
```
