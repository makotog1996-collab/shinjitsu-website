# 真実｜日々をアップデート

> 制作実績・LINE/メールの相談機能を本番へ公開済みです。最新の公開・復元情報は `DEPLOYMENT_STATUS.md` を参照してください。

知ることから、毎日はもっと良くなる。

AI・心理学・自分磨き・暮らしの4つのnoteとSNSを統合する個人ブランドサイトです。承認済みのアイボリー・淡いグリーンのデザインを使用し、既存のNetlify URLで正式公開しました。

- **サイト**：https://neon-empanada-519607.netlify.app/
- **ソース**：https://github.com/makotog1996-collab/shinjitsu-website
- **自動更新・手動更新**：https://github.com/makotog1996-collab/shinjitsu-website/actions/workflows/update-notes.yml
- **公開・復元の記録**：[DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)

## 日常の使い方

通常のnote投稿や表示名変更について、このリポジトリやNetlifyを手作業で変更する必要はありません。毎日03:17（日本時間）を目安に公開RSSを取得します。GitHub側の実行遅延や配信キャッシュにより数分以上ずれる場合があります。サイトを再読み込みすると、取得済みの最新JSONを表示します。

更新が止まった場合は、次の操作で手動更新できます。

1. 上の「自動更新・手動更新」を開く。
2. **Run workflow** を押す。
3. ブランチmainを選び、もう一度 **Run workflow** を押す。
4. 実行結果の緑のチェックを確認し、数分後にサイトを再読み込みする。

`data/notes.json` の `checkedAt` は実行時刻、各アカウントの `fetchedAt` は最後に正常取得できた時刻です。`status: cached` は取得失敗時に前回の正常データを保持していることを示します。GitHubで定期実行が無効化された場合はActions画面で再有効化します。GitHubには長期無活動時のスケジュール停止等の制限があるため、停止したときは上の方法で確認してください。

## 自動更新の仕組み

```
note公開RSS
  → GitHub Actions（毎日03:17 JST）
  → data/notes.jsonを保存
  → サイトがGitHubの公開JSONを取得
  → 表示名・最新記事を画面へ反映
```

取得・生成・表示は分離しています。表示名は設定ファイルに固定せず、各RSSのchannel/titleから取得します。記事はタイトル、URL、公開日時、公開RSSのdescriptionから整形した180文字までの概要、取得可能なサムネイルを保存します。本文全文は転載しません。noteアカウント側の名前を変更する処理はありません。

公開JSONのURL：
https://raw.githubusercontent.com/makotog1996-collab/shinjitsu-website/main/data/notes.json

実際のmainブランチを指定し、HTTP 200・CORS・5分の配信キャッシュを確認しています。画面側にも5分単位のキャッシュキーを設けています。データ更新のコミットには `[skip ci] [skip netlify]` を付けるため、毎日Netlifyをデプロイする方式ではありません。

RSSの取得失敗時はアカウントごとに前回の表示名・記事・最終成功日時を保持します。初回失敗時はジャンル名＋「のnote」を表示します。ブラウザーからJSONを取得できない場合も、ブラウザーの正常キャッシュや同梱の静的HTMLが残り、各noteへ移動できます。JavaScriptが無効でもテーマ・SNS・保存済み記事を利用できます。

## 内容を追加・修正する場所

| ファイル | 用途 |
| --- | --- |
| config/site.json | noteのURL・ジャンル・紹介文、SNS、おすすめ記事、将来の商品 |
| templates/index.html | ページ構造・文章 |
| public/style.css | 配色・余白・スマホ表示 |
| public/script.js | JSONの画面反映と共有機能 |
| scripts/update_notes.py | 公開RSSの取得・キャッシュ |
| scripts/build.py | 設定とキャッシュから公開HTMLを生成 |
| .github/workflows/update-notes.yml | 毎日の更新と手動実行 |
| public/ | Netlifyへ公開するファイル一式 |
| AGENTS.md | 次回Codexへ引き継ぐ作業方針 |

5つ目のnoteはnotes配列にURLとcategoryを追加すると対応できます。description、symbol、colorは省略可能です。SNSはsocials配列に追加でき、Pinterest等も同じ構造で扱えます。offersは現在空です。紹介する実在の商品が決まってから、title・description・httpsのurl・広告表記用disclosureを追加します。

**カード構造やデザインを変更した場合は、一度ビルドしてNetlifyへ公開する必要があります。** noteの名前や新着記事だけの変更には再公開は不要です。Netlifyへの毎日の自動再デプロイや、有料機能を追加していません。

## ローカルでの作業

Python 3.10以上の標準ライブラリだけで取得・生成・単体テストが動きます。実行場所はリポジトリのルートです。

```sh
python3 scripts/update_notes.py
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 -m http.server 8000 --directory public
```

ブラウザーで http://localhost:8000 を開きます。プライバシーページはローカルでは /privacy.html を使います。ブラウザーテストのtests/browser_check.pyは、PlaywrightとChromiumが利用できる開発環境向けです。通常の閲覧や毎日の更新に追加パッケージは不要です。

## 公開・復元と秘密情報

現在の公開デプロイIDと復元対象はDEPLOYMENT_STATUS.mdに記録しています。Netlifyへログインして既存プロジェクトのDeploysから旧デプロイを再公開できます。旧デプロイは削除していません。バックアップ・OAuth認証・アカウント情報は公開リポジトリに入れていません。パスワード・APIトークンをコミットしないでください。

## 費用と検証

Netlify Free・自動チャージ無効・超過課金無効をAPIで確認して公開しました。追加の有料契約、プラン変更、従量課金の有効化、有料APIはありません。サイトは静的ファイルで、追加Functions・Blobs・データベース・課金される定期実行サービスを使いません。Actionsは公開リポジトリの標準Ubuntuランナーのみを利用し、privateリポジトリになった場合はジョブを実行しない条件を設けています。

Netlify Freeは無制限ではなく、公式料金表では月300クレジット、本番デプロイ15クレジット/回です。無料枠の上限では停止する場合があるため、有料化やauto rechargeの有効化をせずに運用します。

単体テスト24件、実際の公開サイトのPC・スマホ幅、4つのnote・3つのSNS・記事リンク、画像、JSON取得と画面反映を確認しました。詳細と実施方法はDEPLOYMENT_STATUS.mdおよびdocs/live-verification.jsonに記録しています。

初回制作時の記録はdocs/initial-delivery-report.md、初期設定の参考手順はdocs/setup-reference.mdに保全しています。

参照：
- https://www.netlify.com/pricing/
- https://docs.github.com/en/billing/concepts/product-billing/github-actions
- https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule
- https://note.com/robots.txt

## 制作実績・仕事の相談を更新する

`config/work.json` に連絡先、自己紹介、相談メニュー、制作実績、相談の流れ、FAQを保存しています。LINEは `lineUrl`、メールは `email` を編集し、`python3 scripts/build.py` でリンク・プライバシーポリシーも生成します。メールのリンクはメールアプリを開くmailtoであり、サイトからの自動送信や受信確認はありません。

制作実績を追加するときは、portfolio配列へid・name・subtitle・url・description・purpose・technologiesを追加します。imageは任意で、実際に取得した画像をpublic/imagesに置いた場合のみ設定します。技術・顧客実績・成果・料金を推測で増やさないでください。

既存のGA4（G-76H2G7LD3T）を維持しています。`contact_click` はcontact_method（line/email）とplacement、`portfolio_click` はcontent_idとplacementを送信します。元のSNS・記事・商品向けhub_link_clickも維持しています。画面上のクリックとパラメータをテストしましたが、GA4管理画面での受信、LINEのメッセージ到達、メールの配信、成約は未検証です。独自イベントに相談内容や返信先を含めません。新しい解析サービスは追加していません。

問い合わせフォーム・決済・新規課金設定はありません。料金と対応範囲は事前確認のうえ個別案内し、双方の合意後に作業を開始する案内です。法定事業者表示の必要性は具体的な契約・販売条件をもとに確認します。フォームがないことだけを理由に表示義務が不要とは断定しません。
