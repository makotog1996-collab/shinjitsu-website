# 無料ツールを中心にしたリニューアル

基準commit: 06c13fb2c9bb40ad8c29e17063438bf828ddceba
作業ブランチ: renewal/free-tools-20261115
本番URL: https://neon-empanada-519607.netlify.app/

## 変更

無料ツール→4つのnote→おすすめ・新着→6つのガイド→実績・運営者・制作相談→商品枠→LINE/メール→SNSという流れに変更。アイボリーと深緑、オリーブ、控えめなゴールド。スマホメニュー、フォーカス、軽いスクロール演出（動きの軽減設定対応）。

前回ZIP内の投稿リパーパス設計室を再利用し、編集・端末保存・復元・コピー・MD/CSV/JSON・UTMを維持。ローカル保存キーとスキーマはv1のまま。AI APIや自動投稿はない。入力本文はブラウザー内で処理。

`config/tools.json`で利用可能/検討中を管理。検討中2案はまだ使えないことを明示。`config/site.json`で4テーマ、SNS、実在のおすすめ記事、正式な商品リンク（確認済みの場合だけ）を管理。正規広告リンク・実商品がないため、広告/販売/決済を新設していない。

既存の全note/SNS、LINE/メール、8相談メニュー、2公開実績、5FAQ、既存画像、RSS取得・失敗時のキャッシュ、GA4 IDを保持。既存のGA4起動ファイルは変更なし。カスタムイベントはツールID・媒体・形式等の固定識別子のみ。実到達・契約・投稿成功は計測しない。

## 実行

```bash
python3 scripts/update_notes.py
python3 scripts/build.py
python3 -m unittest discover -s tests -v
# PlaywrightとChromiumが既に使える環境:
node tests/renewal_browser.js
```

テストはローカルの自作ファイルをPlaywrightの通信ルートへ渡す方式。独自HTTPサーバーは起動しない。実Netlifyの配信検査とは異なる。iPhone検証はChromiumのiPhone13記述子によるエミュレーション。実iOS/SafariとWebKitは実行ファイルがないため未確認。

ページ別title/description、canonical、OGP、適切な構造化データ、11ページのサイトマップ、robotsを生成。NetlifyのCONTEXTがdeploy-previewまたはbranch-deployなら全HTMLをnoindexにし、robotsをDisallowへ切り替える。本番では通常のindex用出力になる。

## 公開の境界

GitHubは専用ブランチのみ。本番ブランチへのmerge、ドメイン・プラン・課金設定の変更は禁止。PRのNetlifyプレビューは確認用。ユーザー承認まではmergeしない。

公開前に本人がプレビューを確認し、Netlify管理画面の現行デプロイID、無料枠/契約条件、復元手段を確認する。前回のGitと公開静的ファイルは作業環境にバックアップ済みだが、管理画面限定設定やFunctions/秘密情報を含む完全なアカウントバックアップではない。無料枠を超える場合は有料切替せず停止・縮小する。

承認後にのみmainへ反映し、実Netlifyの11ページ・スマホ・ファイル出力・LINE/メール遷移・GA4受信を確認する。実メッセージは自動送信しない。
