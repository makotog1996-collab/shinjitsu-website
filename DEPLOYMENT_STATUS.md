# 正式公開の実行状況

このファイルは実際に確認できた結果だけを記録します。

- 完成済みソース：確認済み。承認済みのデザインを再利用。
- note：4アカウントとも公開RSSから表示名・記事・日時・概要を取得済み。
- 単体テスト：17件成功。
- 自動更新経路：毎日03:17 JSTのGitHub Actionsを有効化済み。手動実行 https://github.com/makotog1996-collab/shinjitsu-website/actions/runs/43467160524 が成功。4RSS取得・17テスト・JSON保存コミット7925162を確認。公開JSONのHTTP 200、CORS *、max-age=300を確認済み。Netlify画面での反映確認は公開後に行う。
- GitHub：公開リポジトリ https://github.com/makotog1996-collab/shinjitsu-website のmainへ全ソースを保存済み。秘密情報は含めていない。
- Netlify：公式OAuth認証のユーザー承認待ち。まだ新デザインを公開していない。
- バックアップ：現行サイトの公開ファイル13件を再取得し、SHA-256付きで作業環境に保存済み。Netlify上のpublished deploy IDは未認証のため未確認。完全な復元の確認は認証後。
- 料金：追加契約・課金設定なし。Netlifyアカウントの実際のプラン・無料枠残量は認証後に確認する。
