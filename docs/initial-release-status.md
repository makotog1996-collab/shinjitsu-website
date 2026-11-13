# 正式公開・自動運用の実行結果

正式公開：2026年11月14日 02:03 JST

| 項目 | 実行結果 |
| --- | --- |
| 公開URL | https://neon-empanada-519607.netlify.app/ |
| GitHub | https://github.com/makotog1996-collab/shinjitsu-website |
| 新デプロイ | `6af742107781419c0e73b29f` / ready / 元のプロジェクト・URLを維持 |
| 元のデプロイ | `6af507ab948c7cdf7280e96f` / ready / 削除せず保全 |
| note取得 | 4アカウントの現在名、記事、URL、公開日時、180文字までの概要を取得 |
| 毎日の更新 | GitHub Actions `17 18 * * *` UTC（03:17 JST）、有効 |
| 手動実行テスト | 2回成功。最終テスト https://github.com/makotog1996-collab/shinjitsu-website/actions/runs/43467759651 |
| 公開JSON | HTTP 200 / CORS `*` / `max-age=300` / 実ブランチmainを使用 |
| 公開後のブラウザー確認 | 実際のHTML/CSS/JS・画像・GitHub JSONを取得してChromiumで確認。DOMとlocalStorageへの反映成功 |
| レイアウト | PC 1440px、スマホ幅390px・320px、横はみ出しなし |
| 外部リンク | 公開HTMLから抽出した16リンクすべてHTTP 200 |
| Pythonテスト | 17件成功。名前変更、失敗時の保持、概要整形、URL検証など |
| 料金設定 | Netlify Free、自動チャージ無効、超過課金無効。プラン・契約は変更していない |
| サーバー機能 | 新デプロイは静的ファイルのみ。Functionsの追加なし |

## バックアップ・復元

現行デプロイのメタデータとファイル一覧を取得し、公開ファイル13件を作業環境に保存した。Netlifyの設定ファイルnetlify.tomlはHTTPで取得できないため、ローカルの公開ファイルコピーだけでは完全な復元にならない。完全な復元には保全した元のreadyデプロイを再公開する。旧デプロイ・旧Functionsのソースはリポジトリには混ぜていない。

Netlifyへログインし、既存のneon-empanada-519607プロジェクト → Deploys → 元のデプロイ `6af507ab948c7cdf7280e96f` を開き、「Publish deploy」等の再公開操作を行う。管理画面の文言が変わる場合も、対象IDで確認できる。APIによる復元エンドポイントは `POST /api/v1/sites/8abd4543-f97b-4794-8d46-9faa542ad269/deploys/6af507ab948c7cdf7280e96f/restore`。認証情報は必要であり、公開資料にトークンを入れない。

復元経路と旧デプロイのready状態をAPIで確認した。正常な本番を切り替えるロールバック実行自体は不要なので行っていない。

## 確認の方法と範囲

Netlifyの確認用デプロイはログイン保護により401となるため、保護を変更せず、ready状態とアップロード完了を確認して本番へ公開した。公開後、本番URLのHTTP 200と新ブランドを確認した。

環境の独立したChromiumの証明書ストアにセッション用CAが入っていないため、ブラウザーテストの通信は環境指定CAでTLS検証するPython HTTPクライアントを経由した。取得した実際の公開HTML・CSS・JavaScript・画像・JSONをChromiumへ転送し、JavaScript・CORS・DOM・localStorageの挙動を確認した。TLS検証を無効にするフラグは使っていない。iPhone実機・Safariでの直接試験は未実施。

GitHubに保存した公開用ファイルをNetlifyへアップロードした。Netlifyのアカウント情報、OAuth認証情報、秘密鍵、個人の請求情報はソースやこの記録へ保存していない。
