# 真実｜日々をアップデート
- 既存の Netlify URL と4つの note、X、TikTok、Instagram のURLを維持する。
- 新しい有料サービス・従量課金機能・Functions・カード登録を追加しない。
- note表示名は `config/site.json` に固定しない。`scripts/update_notes.py` が公開RSSから取得し `data/notes.json` に保存する。
- 取得失敗時は最後の正常な表示名・記事・取得日時を維持する。
- テーマの変更・追加は `config/site.json`、ページ構造は `templates/index.html`、見た目と操作は `public/style.css` と `public/script.js` を編集する。
- 実行：`python3 scripts/update_notes.py` → `python3 scripts/build.py` → `python3 -m unittest discover -s tests -v`。
- 公開更新前にNetlify上の現行デプロイを確認し、復元可能なデプロイIDと成果物を保存する。通常はユーザー指定の既存プロジェクトで更新する。
- バックアップには元のFunctionsソースや秘密情報は含まれない。`README.md` の復元範囲を守る。
