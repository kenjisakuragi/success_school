# 🌐 LP公開セットアップガイド

> **このディレクトリ(`docs/`)はGitHub Pagesの公開元として使用します。**
> **公開URL:** `https://kenjisakuragi.github.io/success_school/`(設定後)

---

## ① GitHub Pagesを有効化する(5分)

1. GitHubリポジトリ `kenjisakuragi/success_school` を開く
2. 上部メニュー **Settings** をクリック
3. 左サイドバーの **Pages** をクリック
4. 「**Source**」セクションで以下を設定:
   - **Branch:** `claude/personal-management-dashboard-LKkCF` を選択
   - **Folder:** `/docs` を選択
5. **Save** をクリック
6. 1-2分待つと、ページ上部に「Your site is live at https://kenjisakuragi.github.io/success_school/」と表示される

---

## ② メルマガ収集フォームの設定(10分)

現在、`docs/index.html` のフォームは `action="#"` のプレースホルダー状態です。
実際にメール収集するには、以下のいずれかのサービスと連携が必要です。

### 🥇 推奨:Brevo(旧Sendinblue) ─ 無料プランで月300通配信可能

1. [Brevo](https://www.brevo.com/ja/) で無料アカウント登録
2. **Contacts** → **Forms** → **Create a form** で新規フォーム作成
3. フォーム作成後、表示される **HTML形式** をコピー
4. 表示された `action="..."` 属性のURLをコピー
5. `docs/index.html` の以下行を編集:

```html
<!-- 変更前 -->
<form action="#" method="POST">

<!-- 変更後 -->
<form action="https://YOUR-BREVO-FORM-URL" method="POST">
```

### 🥈 簡易代替:Formspree ─ 無料プランで月50通

1. [Formspree](https://formspree.io/) で無料アカウント登録
2. 新規フォーム作成 → 表示される `Form Endpoint URL` をコピー
3. `docs/index.html` を以下のように編集:

```html
<form action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
```

### 🥉 最も簡単:Googleフォーム ─ 完全無料

1. Googleフォームでフォームを作成
2. フォーム送信先URLを取得
3. `docs/index.html` の `<form>` セクションをGoogleフォーム埋め込み用iframeに置き換える

---

## ③ メール自動応答(7日間ステップメール)の設定

メルマガ登録者にPDFと7日間メール講座を自動配信する設定:

### Brevoの場合
1. **Marketing** → **Automation** → **Create new automation**
2. トリガー:「フォーム登録」
3. ステップを追加:
   - Step 1: 即時 → PDF配布メール(添付ファイルでPDF送付 or ダウンロードリンク)
   - Step 2: 1日後 → メール1「マーフィー博士との出会い」
   - Step 3: 2日後 → メール2「3つのルール ① 肯定形」
   - Step 4: 3日後 → メール3「3つのルール ② 現在形」
   - Step 5: 4日後 → メール4「3つのルール ③ 五感」
   - Step 6: 5日後 → メール5「就寝前の黄金時間」
   - Step 7: 6日後 → メール6「学長の体験談」
   - Step 8: 7日後 → メール7「次のステップへ(¥1,000セミナーの案内)」

---

## ④ 配布するPDFの準備

以下の3つの素材が必要です:

1. **マーフィー博士の「叶える言葉」100選 PDF**(全42ページ)
   - Canvaまたはココナラで¥10,000〜¥20,000で作成可能
   - 学長監修・推奨フレーズ100本

2. **「叶う私」ワークシート PDF**(印刷可)
   - 既存の本科ワークシートを流用可能

3. **YouTube限定動画リンク**
   - YouTube動画を「限定公開」設定でアップロード
   - そのURLをメール内で配布

---

## ⑤ 動作確認チェックリスト

GitHub Pages公開後、以下を確認してください:

- [ ] LPがhttps://kenjisakuragi.github.io/success_school/で表示される
- [ ] スマホ表示が崩れていない(Chromeデベロッパーツールで確認)
- [ ] 各セクションのCTAボタンがフォームへスクロールする
- [ ] フォームに自分のメールアドレスを入力して送信できる
- [ ] メルマガサービスに登録が記録される
- [ ] 自動応答メールがすぐ届く
- [ ] PDFがダウンロードできる

---

## ⑥ アクセス解析の設定(任意・推奨)

Google Analyticsを設定すると、LP訪問者数・コンバージョン率を計測できます:

1. [Google Analytics](https://analytics.google.com/) でGA4プロパティを作成
2. 測定IDを取得(`G-XXXXXXXXXX`)
3. `docs/index.html` の `</head>` 直前に以下を追加:

```html
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

---

## ⑦ カスタムドメイン設定(任意・推奨)

`yume-navi.com` のような独自ドメインを使うと信頼性UP:

1. お名前.com等でドメインを取得(年¥1,000-3,000)
2. ドメインのDNS設定で以下のCNAMEレコードを追加:
   - `www` → `kenjisakuragi.github.io`
3. GitHub Repository → Settings → Pages の「Custom domain」に `yume-navi.com` を入力
4. 「Enforce HTTPS」をチェック

---

## ⑧ A/Bテスト・継続改善

LPは公開後、継続的に改善することで コンバージョン率が向上します:

- **タイトル**:「願えば叶うはウソだった」vs 別パターンの比較
- **CTAボタン文言**:「無料でPDFを受け取る」vs「いますぐ手に入れる」
- **ヒーロー画像**:文字のみ vs 神秘的画像背景
- **学長プロフィール位置**:中盤 vs 最終CTA直前

月1回、Google Analyticsのコンバージョン率を確認して、改善ポイントを特定してください。

---

## 🔥 トラブルシューティング

### LPが表示されない
- GitHub Pagesの「ビルド完了」を確認(緑色チェックマーク)
- ブラウザのキャッシュをクリア
- `docs/index.html` のパスを確認

### フォーム送信ができない
- フォームの `action` 属性が正しいか確認
- メルマガサービス側の設定を確認
- ブラウザのデベロッパーツールでネットワークエラーを確認

### スマホ表示が崩れる
- `<meta name="viewport">` タグがあるか確認(現状ありますので問題なし)
- Chromeデベロッパーツールの「Toggle device toolbar」で確認

---

## 📞 サポート

設定で困ったら、本ファイル(`docs/SETUP.md`)を見ながら、必要に応じてClaude(私)にご相談ください。
メルマガサービスの選定・配信文章の作成・LPの改善案、いずれもお手伝いできます。
