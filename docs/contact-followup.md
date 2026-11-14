# 相談導線の追加点検（2026-11-14）

## 現在の公開内容とソース

本番 https://neon-empanada-519607.netlify.app/ と、接続GitHubのmain（開始時31cd767）を調査した。今回依頼されたLINE/mailto、自己紹介、相談8メニュー、実績2件、3ステップ、FAQ5件、個人情報の説明、モバイル固定バーはすでに公開済み。重複セクションを追加していない。

Python標準ライブラリでconfig/site.json、config/work.json、templatesからpublicを生成する静的構成。Netlifyの設定はnetlify.toml、公開先public。GitHub Actionsが公開RSSを定期取得する。現在のNetlify管理画面、Git連携の有効状態、請求・残クレジット、現行deploy IDはこのセッションでは未確認。過去の公開記録はDEPLOYMENT_STATUS.mdに残した。

作業ディレクトリに元プロジェクトがなかったため接続済みのGitHubから新規cloneした。未コミット変更なしを確認後、変更前にバックアップ用コミット1a3c138を作成した。既存作業は破棄していない。

## 今回のコード修正

public/work.cssに.mobile-contact-bar[hidden]{display:none}を追加。IntersectionObserverがhiddenを設定した際、モバイル用display:flexのCSSがブラウザー標準の非表示を上書きしないようにした。既存ブラウザーテストはhiddenプロパティに加えて実際の表示状態を検査するよう補強。相談本文・配色・SNS・広告URL・アニメーションは変更していない。

## 今回実行した確認

- python3 scripts/update_notes.py: 4件ともRSS取得成功。確認で生じた取得日時の差分のみ元に戻し、定期更新機能は維持。
- python3 scripts/build.py: 成功。
- python3 -m unittest discover -s tests -v: 24件成功。
- 公開HTMLの外部リンク19件: HTTP 200（docs/contact-followup-links.json）。HTTP応答は各SNSアプリ内の全動作の保証ではない。
- LINEはhttps://line.me/R/ti/p/@hoi1576mへ転送。
- 全mailtoの宛先はmakotog1996@gmail.com。送信や受信はしていない。
- 内部アセットとアンカー、privacyの相談個人情報へのリンクを確認。
- git diff --check: 成功。

今回の環境では管理ブラウザー用cua_repl.jsが見つからず、PC/スマホの新しい目視・ブラウザー回帰テストは未実施。tests/business_browser.pyの補強は実行済みとは扱わない。Sitesスキルの管理環境手順に「If cua_repl.js is unavailable, skip browser QA: do not start a preview server, install a browser, or improvise another browser-control path.」とあるため、別経路でブラウザーを起動しなかった。
参照: skill://plugin_connector_1p_689987207de08191979cf68eca2941c6/sites/SKILL.md

## 維持・未確認事項

GA4 G-76H2G7LD3Tのコードとcontact_click、portfolio_click、hub_link_clickを維持。管理画面での受信、訪問数、クリック数は未確認。GA4の管理画面にアクセスできないため実測値は報告しない。

4つのnote、新着記事、X/TikTok/Instagram、商品追加用offers配列は維持。現在offersは空、YouTubeのURLも設定されていないため、新しい商品・広告・SNS URLを推測して増やさなかった。

新規サービス、フォーム、決済、有料API、課金設定は追加していない。追加の実費なし。Netlify Freeの現在の残量と復元用デプロイを管理APIで再確認できていないため、今回の修正は本番にデプロイしていない。PRを用意して公開前レビュー可能な状態にした。マージ・公開前に管理者が現在の無料枠、請求設定、復元可能な現行デプロイを確認し、管理ブラウザーが使える環境でモバイル表示を再確認する。

正式氏名・住所・電話番号等は捏造しない。事業者表示の適用は具体的な販売・契約形態で確認が必要。フォームがないことだけで不要とは判断しない。ユーザー依頼末尾「法令上の表示が必要か判断できない場合は」の続きは受け取れていない。
