# 真実｜日々をアップデート

既存公開サイト `https://neon-empanada-519607.netlify.app/` の承認済みデザインを引き継ぐ静的サイトです。最新の公開・接続状況は `DEPLOYMENT_STATUS.md` を確認してください。初回納品時の記録は `docs/initial-delivery-report.md` に保全しています。

元のGitHubリポジトリ、Netlify内部設定、Functionsのソースは提供されていません。公開されているHTML・CSS・JS・画像・プライバシーページ等を別途保存し、その範囲で既存機能を引き継ぎました。これは元リポジトリを編集したものではありません。

## 最初に使うファイル

- `public/`：そのままNetlifyにアップロードできる完成済みファイル。サイトのルートに `index.html` が置かれるよう、publicフォルダーの中身を公開します。
- `config/site.json`：ブランド、noteのURL・ジャンル、SNS、おすすめ記事、将来の商品設定。
- `templates/index.html`：HTMLテンプレート。
- `public/style.css`：明るい配色・レスポンシブデザイン。
- `public/script.js`：保存済みJSONの読み込み、自動更新データの反映、共有機能。
- `scripts/update_notes.py`：4つの公開RSSを取得し、表示名・記事をキャッシュ。
- `scripts/build.py`：キャッシュと設定からHTMLを生成。ネットワーク通信なし。
- `data/notes.json`：前回の正常な取得内容を含むキャッシュ。手で表示名を書き換える運用は不要です。
- `.github/workflows/update-notes.yml`：毎日03:17（日本時間）の無料更新経路。
- `tests/test_notes.py`：取得失敗、名前変更、URL検証などの17テスト。
- `AGENTS.md`：次回Codexで修正する際の作業方針。
- `netlify.toml`：既存Netlifyサイト用の公開ディレクトリ・ビルド設定。

## 実装したこと

ブランド・タブ名・SEO・OGP・ヘッダー・フッター・プライバシーページを新名称へ変更。アイボリー、セージ、くすみブルーを採用し、4テーマのカード全体をリンク化しました。日本語の見出し、スキップリンク、キーボードフォーカス、動きの軽減設定、44px以上の主要タップ領域に対応しています。

4つのnote、X、TikTokに加えて元のInstagram、おすすめ記事3件、共有機能、既存GA4の計測ID・クリックイベント識別子を維持しています。GA4は元の本番ホストでだけ作動し、ローカル検証のアクセスは送信しません。`note_migaku` は過去の集計と連続性を保つ内部イベント識別子であり、サイトのブランド名ではありません。

記事は実際にRSSで取得した公開日時の新しい順に6件を表示します。全体で新しい順のため、各ジャンルが均等に並ぶとは限りません。以前のおすすめ記事は「はじめての方に、おすすめの記事」を開くと読めます。商品・実績は作成していません。

## 表示名と記事の自動更新

```
note.com/<アカウント>/rss
  → Python（毎日または手動、1アカウントにつき1回取得）
  → data/notes.json（GitHubの公開リポジトリに保存）
  → ブラウザーがGitHubの公開JSONを取得
  → カードの表示名と最新記事だけ更新
```

表示名はRSSの `channel/title`、記事は `item/title/link/pubDate` を利用します。`description` からHTMLを除去した180文字までの概要もJSONの `summary` に保存します。各RSSの `channel/link` が設定URLと同じことを検証します。記事本文・非公開API・ログイン情報は利用しません。RSS取得処理とHTML生成・表示処理を分離しています。noteの実際の名前を変更する処理はありません。

現時点の名称は `data/notes.json` に取得結果として記録しています。`MIGAKU｜自分磨きの記録` はnote側の現在名なので自分磨きカードにのみ表示し、サイト全体の名称には使いません。

- 更新予定：**毎日03:17 JST**。GitHub側の混雑・障害により遅延する場合があります。
- 毎日の更新を開始するには、下記のGitHub公開リポジトリ設定が必要です。**納品時点では未接続・定期実行未開始です。**
- GitHub Actionsは公開リポジトリだけ実行されます。非公開リポジトリの有料実行枠を誤使用しない条件を設けています。
- 通常のActionsでは公開リポジトリで60日間活動がないと定期実行が無効になることがあります。Actions画面で状態を確認し、必要なら再有効化してください。完全な無保守・指定時刻の厳密保証ではありません。
- RSS取得失敗時：アカウントごとに前回の名前、記事、最終成功日時を保持します。
- 初回取得失敗時：ジャンル名＋「のnote」を予備表示します。記事を作りません。
- ブラウザーでGitHub JSONの取得に失敗：ブラウザーに保存済みの正常データ、または同梱のHTML・JSONを表示します。localStorageが使えなくてもHTMLが残ります。
- ブラウザーは各アカウントの成功日時を比較し、古い同梱データで新しいキャッシュを上書きしません。
- データだけのコミットには `[skip ci] [skip netlify]` を付け、Netlify側にも差分によるビルドスキップ条件を入れています。毎日Netlifyへデプロイする仕組みにはしていません。
- GitHubの公開JSONにもキャッシュ・通信遅延があるため、名前変更は次の成功した定期更新後、ブラウザーで再読み込みした際に反映されます。

## ローカルの更新と表示

Python 3.10以上を使います。本体とデータ取得・単体テストは標準ライブラリだけで動き、pipやnpmによる依存追加は不要です。

```sh
python3 scripts/update_notes.py
python3 scripts/build.py
python3 -m unittest discover -s tests -v
python3 -m http.server 8000 --directory public
```

最後のコマンドの実行中に `http://localhost:8000` を開きます。終了はCtrl+C。ローカルの標準HTTPサーバーでは `/privacy.html` を開いてください。Netlifyでは `/privacy` にも対応します。HTMLのダブルクリックではなくHTTPで表示してください。

5つ目のnoteは `config/site.json` の `notes` 配列に次の2項目を追加し、上の取得・ビルドを実行すると追加できます。アイコン・色・説明は省略可能です。

```json
{"url":"https://note.com/追加するアカウント","category":"新しいジャンル"}
```

※実際にはnoteの正しい英数字のアカウントURLを使います。定期更新データだけで新しいカードの構造は増えないため、設定変更時には一度ビルドしてNetlifyへ公開します。既存アカウントの表示名変更だけなら再デプロイは不要です。

SNSの追加は `socials` 配列へ追加します。商品は実在する紹介先が決まってから `offers` に `title`、`description`、`url`、`disclosure`（「広告」「PR」など）を入れます。現時点の配列は空です。

## 現在のNetlifyサイトを安全に更新する手順

### 1. 現行デプロイを保全

1. Netlifyへ普段の方法でログインし、**既存の `neon-empanada-519607` プロジェクト**を開きます。新規プロジェクトは作りません。
2. Deploysで現在のPublishedデプロイを開き、デプロイID、固有URL、日時を控えます。ダウンロード機能が利用可能ならデプロイファイルも保存します。
3. そのデプロイを再公開できる権限があることを確認します。公開済みデプロイは削除しません。
4. 同梱の公開ファイルバックアップも保管します。ただし、これはFunctionsのソース、Netlify設定、秘密情報を含みません。**元の最新記事APIまで含めた完全な復元は、Netlify上の元デプロイへのロールバックを使います。**

### 2. 無料で使う条件を確認

NetlifyのUsage & billingでFreeプランを確認し、有料プランへの変更、追加購入、auto rechargeの有効化をしません。2026年11月14日確認の公式価格表ではFreeは月300クレジット、本番デプロイ1回は15クレジットです。帯域・リクエストにも枠があるため、無制限配信ではありません。Freeは上限で停止し、超過課金しない説明になっています。現在のアカウント内部の契約・残量はこの作業環境から確認できていません。旧料金プランでは表示が異なります。無料枠内で更新し、追加購入しないでください。

### 3. GitHubでソースを管理して定期更新を有効化

1. GitHubで**無料の公開リポジトリ**を1つ作ります。これはソース管理用で、新しいWebサイトは作りません。秘密情報・バックアップ・個人ファイルを含めず、このプロジェクトの内容だけを入れます。
2. `config/site.json` の `remoteDataUrl` を次の形式に設定します。`OWNER/REPO` は実際のものへ置き換えます。

   ```
   https://raw.githubusercontent.com/OWNER/REPO/HEAD/data/notes.json
   ```

3. `python3 scripts/build.py` を実行し、生成された `public/data/site.json` にこのURLが入ったことを確認します。これによりNetlifyへ手動アップロードする場合もGitHubから更新を受け取れます。
4. `.github/workflows/update-notes.yml` を含めてGitHubのデフォルトブランチに保存します。ZIP展開時に隠しフォルダー `.github` が落ちないよう注意してください。

   ```sh
   git init
   git add .
   git commit -m "Rebuild Shinjitsu personal brand site"
   git branch -M main
   git remote add origin https://github.com/OWNER/REPO.git
   git push -u origin main
   ```

   認証はGitHubの通常のログイン手順を利用します。トークン・パスワードをチャットへ貼らないでください。
5. GitHubのSettings → Actions → GeneralでActionsを利用可能にし、Workflow permissionsをRead and write permissionsに設定します（リポジトリポリシーで許可される場合）。組織ルールやブランチ保護でbotのpushが禁止されていると自動保存できません。
6. Actions → Update public note RSS cache → Run workflowを1回実行し、成功とJSONの更新を確認します。公開Raw JSONのURLを開き、4つの最新名があることを確認してください。
7. 以後、デフォルトブランチ上のスケジュールが毎日03:17 JSTに実行されます。私有リポジトリでは安全のため実行しません。

GitHub連携を後回しにした場合でもサイトは正常表示できますが、**名前・記事の無人定期更新は始まりません**。その間はローカルで取得・ビルドして手動公開してください。

### 4. 既存サイトへ公開

最小の変更で済むのは手動アップロードです。上のGitHub URL設定・ビルドと表示確認を済ませてから、Netlifyの**既存プロジェクト**のDeploysに、完成版の `public` フォルダーをドロップします。`index.html` が公開ルートになることを確認してください。GitHubのRaw URLを設定した版のpublicを使います。納品ZIPの初期publicは、まだGitHub未接続です。

既存プロジェクトをGitHub連携へ移行する場合は、Project configuration → Build & deployで先ほどのリポジトリを接続し、Build commandを `python3 scripts/build.py`、Publish directoryを `public` にします。Base directoryはプロジェクトルートです。Netlifyには標準のPythonランタイムが必要です。`netlify.toml` にも同じ設定を用意しています。元の環境変数・ドメイン・Analytics等の設定を削除する必要はありません。

GitHub連携での初回ビルドは `REPOSITORY_URL` またはgit originからRaw URLを自動推定できますが、手順3で明示設定しておく方法が確実です。既存のFunctionsによる新着記事APIは今回の静的データ方式に置き換わります。

### 5. 公開直後の確認と復元

- 元のURLを開き、新名称・明るいデザイン・4つの表示名を確認します。
- スマホで4つのnote、X、TikTok、Instagram、記事、共有、`/privacy` を確認します。
- 開発者ツールで `/data/site.json`、GitHub Raw JSONが成功し、コンソールエラーがないことを確認します。
- 次回Actions成功後にJSONの `fetchedAt` が進むことと、ブラウザー再読み込みで反映されることを確認します。noteの名前をテスト目的で変更する必要はありません。
- 不具合があればDeploysから**手順1で控えた元のPublishedデプロイ**を選び、「Publish deploy」等の再公開操作を行います。これにより元のFunctionsも含むデプロイへ戻せます。画面の文言はNetlifyのUI更新で変わることがあります。

## 検証の範囲

納品レポートに実測結果をまとめています。Chromiumで320・375・390・430・768・1440pxを確認しました。iPhone実機/Safari、Netlify本番デプロイ後の権限・GitHubスケジュール実行はこの環境では確認していません。

公開ソースのHTML・CSS・JS、設定とキャッシュを保存していますが、元のプロジェクトの完全なソースを回収したものではありません。元のAPIと異なる方式へ変更した点、定期更新の有効化が残っている点を前提に引き継いでください。

## 費用・取得方式の参照

- Netlify公式料金表：https://www.netlify.com/pricing/ （確認：2026-11-14 JST）
- GitHub Actions料金：https://docs.github.com/en/billing/concepts/product-billing/github-actions
- Actionsスケジュール：https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule
- Netlifyのビルドスキップ：https://docs.netlify.com/build/configure-builds/ignore-builds/
- note robots.txt：https://note.com/robots.txt （一般User-agentで今回のRSSパスに禁止指定なし。robots.txtだけで利用規約の全面的な適合を保証するものではありません。公開RSSを少頻度で取得し本文は転載しません。）

有料API、Netlify Functions/Blobs/データベース、外部有料プラグイン、クレジットカード登録、従量課金の有効化は行っていません。表示用イラストはSVG、フォントは端末の日本語システムフォントを利用します。

## 日常の管理（パソコンでコマンド入力せずに更新）

GitHub保存とActionsの有効化が完了した後は、リポジトリの **Actions → Update public note RSS cache → Run workflow → Run workflow** で手動更新できます。緑のチェックが出た後、サイトを再読み込みしてください。通常は毎日03:17 JSTに同じ処理が自動実行され、Netlifyを操作する必要はありません。

動作確認には `data/notes.json` の `checkedAt` と各アカウントの `fetchedAt` を見ます。`checkedAt` だけが更新され `status: cached` のままの場合、RSS取得に失敗して以前の情報を保持しています。原因を解消して手動実行してください。成功してもRaw JSONの配信キャッシュにより数分かかる場合があります。

Actionsを手動で無効にした場合や長期無活動で停止した場合は、同じワークフローの画面で再有効化してRun workflowを実行します。

`config/site.json` のURL・ジャンルや `socials` を変更した場合、カード構造を変えるため一度だけビルド・公開が必要です。表示名・新着記事の更新には再公開不要です。アフィリエイトや商品は実在する掲載先が確定してから `offers` に追加し、広告表記を付けます。
