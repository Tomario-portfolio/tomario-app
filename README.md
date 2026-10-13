# tomario-app

複数のホテルを横断予約できる予約システム「Tomario」のバックエンド（Flask REST API）とフロントエンド（静的 HTML）のリポジトリです。

インフラ（ECS Fargate / ALB / RDS / CloudFront / S3）は [tomario-infra](https://github.com/Tomario-portfolio/tomario-infra) で管理しています。

## 技術スタック

| レイヤー | 技術 |
|---|---|
| バックエンド | Python / Flask（REST API）、gunicorn、ECS Fargate（Graviton/ARM64）上のコンテナ |
| フロントエンド | HTML / CSS / JavaScript（静的ファイル） |
| データベース | MySQL 8.4（AWS RDS） |
| 認証 | Flask-Login（セッション Cookie） |

---

## アーキテクチャ

```
ユーザー
  ↓ HTTPS
CloudFront
  ├── /*     → S3（静的ファイル: HTML/CSS/JS）
  └── /api/* → ALB → ECS Fargate（Flask API）→ RDS（MySQL）
```

フロントエンドと API は CloudFront で同一オリジンとして配信するため、クロスオリジン問題なしにセッション Cookie が機能します。

---

## ディレクトリ構成

```
tomario-app/
├── app.py              # Flask REST API（ルーティング・DBモデル・ビジネスロジック）
├── seed_data.py        # ホテル・部屋の初期データ（47都道府県）と地方→都道府県の対応表
├── schema.sql          # DB テーブル定義（参考。テーブル作成と初期データの投入はアプリ起動時に行う）
├── requirements.txt    # Python 依存パッケージ
├── Dockerfile          # コンテナイメージ（gunicorn で起動）
├── .github/workflows/
│   └── deploy.yml      # イメージのビルド・脆弱性スキャン（Trivy）・dev/stagingへのデプロイ・productionへの昇格・フロントエンドの配信
└── frontend/           # S3 にアップロードする静的ファイル
    ├── index.html          # トップページ（地方→都道府県・日付でホテル検索）
    ├── hotels.html         # ホテル一覧
    ├── rooms.html          # 客室一覧（部屋の種類ごと・空き室数）
    ├── room_detail.html    # 客室詳細
    ├── booking.html        # 予約フォーム
    ├── my_bookings.html    # 予約確認・キャンセル
    ├── login.html          # ログイン
    ├── register.html       # ユーザー登録
    ├── css/
    │   └── style.css
    └── js/
        ├── api.js      # API 通信・認証・検索プルダウンの共通処理
        └── main.js     # 日付入力の制御
```

---

## API エンドポイント

| メソッド | パス | 説明 |
|---|---|---|
| GET | `/health` | ヘルスチェック（ALB 用） |
| POST | `/api/auth/register` | ユーザー登録（パスワードは8文字以上） |
| POST | `/api/auth/login` | ログイン |
| POST | `/api/auth/logout` | ログアウト |
| GET | `/api/auth/me` | ログイン中ユーザー情報取得 |
| GET | `/api/regions` | 地方と都道府県の一覧 |
| GET | `/api/hotels` | ホテル一覧（`?region=&area=` で地方・都道府県、`?check_in=&check_out=` で空き室数・最安値） |
| GET | `/api/hotels/<id>` | ホテル詳細 |
| GET | `/api/hotels/<id>/room-types` | 部屋の種類ごとの料金・定員・空き室数（`?check_in=&check_out=`） |
| GET | `/api/rooms` | 客室一覧（`?hotel_id=`、`?check_in=&check_out=` で空き部屋） |
| GET | `/api/rooms/<id>` | 客室詳細 |
| POST | `/api/bookings` | 予約作成（`hotel_id`＋`room_type` で空いている部屋を自動で割り当て。`room_id` 指定も可） |
| GET | `/api/bookings` | 自分の予約一覧 |
| POST | `/api/bookings/<id>/cancel` | 予約キャンセル（チェックインまでの日数に応じてキャンセル料を算出） |

---

## 機能

- ユーザー登録 / ログイン / ログアウト（ログイン・会員登録後は元の画面へ戻る）
- 地方→都道府県・日付によるホテル検索（47都道府県・59ホテル）
- 部屋の種類（シングル・ダブル・スイート）ごとの表示と空き室数
- 予約作成（空いている部屋を自動で割り当て、宿泊日数に応じた合計金額を自動計算）
- 予約確認・キャンセル（キャンセル料：3日前まで無料、2日前30%、前日以降50%）

---

## 環境変数

AWS 上では ECS のタスク定義から渡します（認証情報・署名鍵は Secrets Manager から取得）。ローカル実行時は `.env` を作成してください。

| 変数名 | 説明 |
|---|---|
| `SECRET_KEY` | Flask セッション署名用キー |
| `SECRET_KEY_PREVIOUS` | 1つ前の署名用キー（鍵の更新後も、更新前に発行した Cookie を受け付けるため。任意） |
| `DB_HOST` | RDS エンドポイント |
| `DB_PORT` | DB ポート（デフォルト: 3306） |
| `DB_NAME` | データベース名（`tomario`） |
| `DB_USER` | DB ユーザー名 |
| `DB_PASSWORD` | DB パスワード |

---

## ローカル起動

MySQL を用意し、上記の環境変数を `.env` に設定してから起動します。起動時にテーブル作成と初期データの投入を行います。

```bash
pip install -r requirements.txt
python app.py
# → http://localhost:8080
```

フロントエンドは API を同一オリジンの `/api` で呼び出すため、画面まで確認する場合は API と同じオリジンで `frontend/` を配信してください。

---

## デプロイ

`main` へのマージで `deploy.yml` が実行され、イメージのビルド・Trivy による脆弱性スキャン・dev/staging へのデプロイ・フロントエンドの S3 配信までを自動で行います。production へは、staging で検証したイメージを digest 指定で昇格させます（GitHub Environment「prod」の承認が必要）。
