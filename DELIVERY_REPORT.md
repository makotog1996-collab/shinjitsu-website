# 納品レポート：真実｜日々をアップデート

作業完了：2026年11月14日 01:18 JST

## 公開状態

新規プロジェクトとしての再構築・実装・ローカル動作確認を完了しました。現在のNetlifyサイトは更新していません。Netlifyの認証権限と元のGitHubリポジトリが未提供のため、本番デプロイと定期更新の有効化は未実施です。新しいサイトの乱立、API契約、課金設定はありません。

## 納品物

- project/：GitHubに保存できるプロジェクト一式（隠しフォルダー.githubを含む）。
- project/public/：公開用ファイル。index.htmlが公開ルートになります。
- project/README.md：更新・公開・復元・無料運用の詳細手順。
- backup-public/：旧サイトから取得した公開ファイルとSHA-256一覧。サーバーソースやNetlify設定のバックアップではありません。
- screenshots/：Chromiumで取得したPC・スマホ表示。
- evidence/：リンク確認とブラウザーテスト結果。

## 作成・変更した主なファイル

config/site.json、templates/index.html、scripts/update_notes.py、scripts/build.py、data/notes.json、public/index.html、public/style.css、public/script.js、public/privacy.html、public/favicon.svg、public/og-image.png、public/data/site.json、public/data/notes.json、public/analytics.js、public/engagement.js、public/_headers、public/_redirects、netlify.toml、.github/workflows/update-notes.yml、tests/test_notes.py、tests/browser_check.py、AGENTS.md、README.md。

新名称、SEO、OGP、ヘッダー・フッター、明るい配色、4テーマカード、新着記事、SNS、将来の紹介枠を実装しました。既存note・SNS・おすすめ記事・共有・GA4を引き継いでいます。既存のInstagramも維持しました。商品や実績は作成していません。

## 取得できたnoteの現在名

- 真実｜AIを使い倒す人 — https://note.com/crisp_auk8183
- 真実｜日常の気づきと心理学 — https://note.com/rosy_snake7477
- MIGAKU｜自分磨きの記録 — https://note.com/brave_violet386
- 真実｜暮らしの困りごとと時短 — https://note.com/shinjitsu_saigen

表示名は上記の文字列を固定設定したものではなく、RSSからのキャッシュです。取得日時はJSONのfetchedAtに記録しています。

## 自動更新

公開RSS → GitHub Actions → 保存済みJSON → ブラウザー表示の経路を実装。毎日03:17 JSTの予定です。公開リポジトリへの保存、remoteDataUrlの設定、Actionsの有効化が完了した後に稼働します。現時点では未有効化です。GitHubのスケジュールには遅延・休止の可能性があります。

RSS失敗時はアカウントごとに最後の正常なデータを維持し、初回失敗時はジャンル名を予備表示します。ブラウザーでは新しいキャッシュを古い同梱データで戻さず、通信失敗時も静的HTMLが残ります。名前変更だけではNetlifyを再デプロイしません。note側の表示名は変更していません。

## テスト結果

Python単体テスト：14件成功。実際の4RSSから表示名・公開記事を取得成功。JavaScript構文検証、Python構文検証、Netlify TOMLの読み込みも成功。

- Desktop title, 4 live names, 3 original SNS URLs, 6 articles, light background, no JS exceptions: PASS
- 320, 375, 390, 430, 768, 1440 px: no horizontal overflow; theme tap areas >=44px: PASS
- Privacy route and renewed brand: PASS
- JavaScript disabled: static names, themes and articles remain: PASS
- JSON network failure: snapshot remains usable: PASS
- Remote name change automatically reflected as text, without HTML execution: PASS
- Remote outage after successful update: latest cached name preserved: PASS
- Malicious external article URL rejected: PASS
- Share button copies canonical URL: PASS

リンク確認：
- https://note.com/crisp_auk8183 → 200
- https://note.com/rosy_snake7477 → 200
- https://note.com/brave_violet386 → 200
- https://note.com/shinjitsu_saigen → 200
- https://x.com/abp12f → 200
- https://www.tiktok.com/@otokomigaki.lab2 → 200
- https://www.instagram.com/shinjitsu_aiai/ → 200
- https://note.com/crisp_auk8183/n/nc7b339d78647 → 200
- https://note.com/brave_violet386/n/nf6f0cf8bc6fd → 200
- https://note.com/rosy_snake7477/n/n9746ca8d3901 → 200

テストの名前変更は取得データの差し替えで再現しました。実際のnoteアカウントに変更はしていません。iPhone実機・Safariでの確認は未実施です。公開後のNetlify・GitHubの実行確認も残っています。

## 費用

追加契約・課金有効化・カード登録・依存パッケージの新規購入は0件です。Python標準ライブラリと静的ファイルを使います。Netlify公式料金表はFreeの月300クレジット、本番公開15クレジット/回、無料枠超過時の停止を案内しています（2026-11-14確認）。既存アカウントの実際のプラン・残量は未確認です。公開前にFreeであることを確認し、有料化・追加購入・自動チャージをしないでください。Actionsは公開リポジトリの標準ランナーに限定しています。

## 安全な公開の最後の操作

1. 既存Netlifyプロジェクトの現在のPublishedデプロイIDを控え、再公開できる状態を保つ。
2. GitHubに無料の公開リポジトリを作り、project/の内容を保存する。backup-public/はソースに混ぜない。
3. config/site.jsonのremoteDataUrlを https://raw.githubusercontent.com/OWNER/REPO/HEAD/data/notes.json に設定し、python3 scripts/build.pyで公開用を生成し直す。
4. GitHub ActionsのRead and write権限を設定し、Update public note RSS cacheを手動実行して成功を確認する。
5. 既存NetlifyプロジェクトのDeploysへ、生成し直したpublic/をアップロードする。別プロジェクトは作らない。Git連携を選ぶ場合はBuild command=python3 scripts/build.py、Publish directory=public。
6. 同じ本番URLでリンク・表示名・共有・privacyを確認。不具合時は手順1の元デプロイを再公開する。

詳細はproject/README.mdに記載しています。
