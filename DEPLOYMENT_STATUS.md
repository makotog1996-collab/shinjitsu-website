# 正式公開・自動運用の実行結果

最終公開：2026年11月14日 02:46 JST（制作・相談機能の追加版）

- 公開サイト：https://neon-empanada-519607.netlify.app/
- 全ソース：https://github.com/makotog1996-collab/shinjitsu-website （main）
- 公開デプロイ：`6af74a54bef029deeeb08d35` / ready
- 直前の復元用デプロイ：`6af742107781419c0e73b29f` / ready、削除していない
- 作業前Gitタグ：`backup-before-contact-extension-20261114`（590e930）
- 追加版PR：https://github.com/makotog1996-collab/shinjitsu-website/pull/1 （マージ済み）

## 公開内容

LINE公式URLとmailtoの相談導線、スマホの相談バー、個人としての自己紹介、8つの相談メニュー、実際の作品2件・実際の公開画面の画像、3ステップ、FAQ5件を公開した。4つのnote・新着記事・既存SNS・共有・商品紹介の設定構造・日次更新を維持した。

個人情報の扱いと外部サービスの説明、ブラウザーキャッシュ、計測の範囲をプライバシーポリシーへ追記した。フォーム・決済・架空の価格や顧客実績は追加していない。

## 検証結果

- 追加版を含む単体テスト24件成功。
- main上のActions手動実行成功：https://github.com/makotog1996-collab/shinjitsu-website/actions/runs/43476396680
- 4つのnoteの現在名・記事・日時・概要を公開RSSから取得しJSONを更新。毎日03:17 JSTの設定は有効。
- 公開JSONはmainブランチを利用し、HTTP 200、CORS *、5分単位のキャッシュ更新に対応。
- 公開後、本番のHTML/CSS/JS・記事画像・GitHub JSONを実際に取得し、ChromiumでDOM・localStorageへの反映を確認。
- PC1440px・スマホ幅390px/320pxで横はみ出しなし。公開前には320/375/390/430/768/1024/1440pxと相談バーの非遮蔽も確認。
- 公開HTMLの外部リンク18件すべてHTTP 200。LINEの転送先、mailtoの宛先・件名、作品ページ、FAQ操作、プライバシーページ、OGP画像を確認。
- contact_click、portfolio_clickの公開コードを確認。公開前のブラウザーでイベント発火・識別子だけのパラメータ・既存イベント維持を検証。

ブラウザー通信は、環境指定CAを用いてTLS検証したPython HTTPクライアントから実レスポンスをChromiumへ転送して確認した。証明書検証を無効にしていない。iPhone/Safari実機、GA4管理画面での実受信、LINEメッセージ・メールの配信は未検証。クリックは実送信や成約を意味しない。

## 復元

Netlifyへログインし、既存のneon-empanada-519607プロジェクト → Deploys → `6af742107781419c0e73b29f` を選び、「Publish deploy」等の再公開操作を行う。APIは `POST /api/v1/sites/8abd4543-f97b-4794-8d46-9faa542ad269/deploys/6af742107781419c0e73b29f/restore`。

対象デプロイのready状態とOwner権限を確認済み。正常な本番を切り替えるロールバック実行自体は不要なので行っていない。さらに前のデプロイ6af507ab948c7cdf7280e96fも保全している。

## 費用と管理

Netlify Free、自動チャージ無効、超過課金無効、公開前の無料枠内残量を確認した。GitHub Actionsは公開リポジトリの標準ランナーのみ。追加契約・プラン変更・有料API・新しいFunctionsやフォームはなし。日々のnote投稿や表示名変更でNetlifyの再公開は不要。

法定事業者表示の適用は具体的な取引条件によるため、不要とは断定していない。未確定の正式氏名・住所・電話番号・料金を作って掲載することはしていない。将来の商品販売や申込方法の追加時には必要事項を確認する。

初回公開の記録はdocs/initial-release-status.md、今回の実装記録はdocs/official-site-extension.md、検証結果はdocs/official-extension-verification.jsonを参照。
