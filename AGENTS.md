# 真実｜日々をアップデート
- 既存の Netlify URL と4つの note、X、TikTok、Instagram のURLを維持する。
- 新しい有料サービス・従量課金機能・Functions・カード登録を追加しない。
- note表示名は `config/site.json` に固定しない。`scripts/update_notes.py` が公開RSSから取得し `data/notes.json` に保存する。
- 取得失敗時は最後の正常な表示名・記事・取得日時を維持する。
- テーマの変更・追加は `config/site.json`、ページ構造は `templates/index.html`、見た目と操作は `public/style.css` と `public/script.js` を編集する。
- 実行：`python3 scripts/update_notes.py` → `python3 scripts/build.py` → `python3 -m unittest discover -s tests -v`。
- 公開更新前にNetlify上の現行デプロイを確認し、復元可能なデプロイIDと成果物を保存する。通常はユーザー指定の既存プロジェクトで更新する。
- バックアップには元のFunctionsソースや秘密情報は含まれない。`README.md` の復元範囲を守る。

## 制作・相談機能
- `config/work.json` に連絡先・8相談メニュー・制作実績・手順・FAQをまとめる。
- 仕事用の追加UIは `templates/work-contact.html`、`templates/work-content.html`、`public/work.css`、`public/contact.js`。
- プライバシーポリシーは `templates/privacy.html` を編集し、build.pyで生成する。
- GA4は既存IDを維持する。contact_click/portfolio_clickには識別子だけを送り、相談本文・メールアドレス・URLクエリを送らない。
- 追加テストは `python3 tests/business_browser.py`（Playwright環境のみ）。実メール送信やLINEメッセージ送信は行わない。
- 現時点でフォーム・料金表・商品販売は追加していない。法定表示の適用を未確認のまま不要と断定しない。
