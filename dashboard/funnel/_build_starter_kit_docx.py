"""
マニフェスティング・スターターキット PDF→Word(.docx)制作
20ページのリードマグネット PDF/Word を生成
"""
from pathlib import Path
from docx import Document
from docx.shared import Pt, RGBColor, Cm, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = Path(__file__).resolve().parent
OUT = HERE / "マニフェスティング・スターターキット.docx"

# ==== Color Palette (桜木ブランド) ====
PINK_MAIN = RGBColor(0xc9, 0x4f, 0x7c)
PINK_DARK = RGBColor(0xb8, 0x45, 0x6e)
PINK_BG = RGBColor(0xff, 0xf5, 0xf7)
GOLD = RGBColor(0xff, 0xc8, 0x57)
DARK_TEXT = RGBColor(0x2c, 0x2c, 0x2c)
MUTED = RGBColor(0x77, 0x77, 0x77)
WHITE = RGBColor(0xff, 0xff, 0xff)

JP_FONT = "Yu Mincho"
JP_BOLD = "Yu Gothic"


def set_font(run, name=JP_FONT, size=11, bold=False, color=None):
    """フォント設定(日本語対応)"""
    run.font.name = name
    run.font.size = Pt(size)
    run.bold = bold
    if color is not None:
        run.font.color.rgb = color
    # eastAsia フォント指定
    rPr = run._element.get_or_add_rPr()
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), name)


def add_pagebreak(doc):
    p = doc.add_paragraph()
    r = p.add_run()
    br = OxmlElement('w:br')
    br.set(qn('w:type'), 'page')
    r._element.append(br)


def add_heading(doc, text, size=22, color=PINK_MAIN, align=WD_ALIGN_PARAGRAPH.LEFT, space_after=12):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    r = p.add_run(text)
    set_font(r, name=JP_BOLD, size=size, bold=True, color=color)
    return p


def add_text(doc, text, size=11, bold=False, color=DARK_TEXT, align=WD_ALIGN_PARAGRAPH.LEFT, indent=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.line_spacing = 1.8
    if indent is not None:
        p.paragraph_format.left_indent = Cm(indent)
    r = p.add_run(text)
    set_font(r, name=JP_FONT, size=size, bold=bold, color=color)
    return p


def add_divider(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("─" * 30)
    set_font(r, name=JP_FONT, size=10, color=MUTED)


def add_blank_line(doc, count=1):
    for _ in range(count):
        doc.add_paragraph()


def add_quote_box(doc, text, italic=False):
    """引用調の段落(背景色付き)"""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.8)
    p.paragraph_format.right_indent = Cm(0.8)
    p.paragraph_format.line_spacing = 1.8
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(8)
    r = p.add_run(text)
    set_font(r, name=JP_FONT, size=11, bold=False, color=PINK_DARK)
    r.italic = italic
    return p


def add_blank_input_line(doc, lines=3, indent=0.5):
    """記入用の罫線"""
    for _ in range(lines):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Cm(indent)
        p.paragraph_format.line_spacing = 1.0
        r = p.add_run("_" * 50)
        set_font(r, name=JP_FONT, size=11, color=MUTED)


def setup_page(doc):
    """ページマージン設定"""
    section = doc.sections[0]
    section.top_margin = Cm(2.5)
    section.bottom_margin = Cm(2.5)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)


# ====================================================
#  ページごとの内容
# ====================================================

def page_cover(doc):
    """表紙"""
    add_blank_line(doc, 4)
    # 大きな絵文字
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run("🌸")
    set_font(r, size=72)

    add_blank_line(doc, 1)
    add_heading(doc, "マニフェスティング", size=32, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=4)
    add_heading(doc, "スターターキット", size=32, align=WD_ALIGN_PARAGRAPH.CENTER, space_after=20)

    add_text(doc, "― 「未来からの手紙」が、今夜、",
             size=13, align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED)
    add_text(doc, "  あなたの脳を動かしはじめます ―",
             size=13, align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED)
    add_blank_line(doc, 6)

    add_text(doc, "桜木 賢治", size=18, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=PINK_MAIN)
    add_text(doc, "日本マニフェスティング協会 代表",
             size=11, align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED)
    add_blank_line(doc, 2)
    add_text(doc, "2026年版", size=10, align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED)


def page_intro_1(doc):
    """P.1 はじめに前半"""
    add_heading(doc, "はじめに", size=20)
    add_divider(doc)

    add_text(doc, "このPDFをダウンロードしてくださって、ありがとうございます。", size=11)
    add_text(doc, "このページを開いてくださった、ということは ―", size=11)
    add_blank_line(doc, 1)
    add_text(doc, "あなたは今、人生のどこかで、", size=11)
    add_text(doc, "「もう一度、自分を変えたい」と、本気で願っているのだと思います。", size=11)
    add_blank_line(doc, 1)
    add_text(doc, "そして、過去に何冊も引き寄せの本を読んで、", size=11)
    add_text(doc, "それでも変わらなかった経験を、抱えているのかもしれません。", size=11)
    add_blank_line(doc, 2)
    add_text(doc, "大丈夫です。", size=14, bold=True, color=PINK_MAIN, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_text(doc, "あなたのせいでは、ありません。", size=14, bold=True, color=PINK_MAIN, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_blank_line(doc, 1)
    add_text(doc, "メソッドの設計が、不完全だったのです。", size=11, align=WD_ALIGN_PARAGRAPH.CENTER)


def page_intro_2(doc):
    """P.2 はじめに後半"""
    add_heading(doc, "なぜ「書くこと」が脳を変えるのか", size=16, color=PINK_DARK)
    add_divider(doc)

    add_text(doc, "カリフォルニアのドミニカン大学で、こんな研究があります。", size=11)
    add_blank_line(doc, 1)
    add_text(doc, "ゲイル・マシューズ博士は、149名の社会人を5つのグループに分け、", size=11)
    add_text(doc, "目標達成について比較しました。", size=11)
    add_blank_line(doc, 1)
    add_text(doc, "結果は、こうでした。", size=11)
    add_blank_line(doc, 1)
    add_text(doc, "・ただ「考える」だけ:達成率 約43%", size=11, indent=1.0)
    add_text(doc, "・「書く + 共有 + 進捗報告」:達成率 約76%", size=11, indent=1.0)
    add_blank_line(doc, 1)
    add_text(doc, "差は、約33ポイント。", size=14, bold=True, color=PINK_MAIN, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_blank_line(doc, 1)
    add_text(doc, "紙にペンを走らせる ― ただそれだけの行為が、", size=11)
    add_text(doc, "人生をこれほど大きく変える可能性があります。", size=11)
    add_blank_line(doc, 1)
    add_text(doc, "これが、本PDFの土台になる科学です。", size=11)


def page_how_to_use(doc):
    """P.3 本書の使い方"""
    add_heading(doc, "本書の使い方", size=20)
    add_text(doc, "今夜、5分でできる、最初の一歩", size=14, bold=True, color=PINK_DARK)
    add_divider(doc)

    add_text(doc, "このPDFは、以下の3つで構成されています。", size=11)
    add_blank_line(doc, 1)
    add_text(doc, "① ワーク1:過去形で書く ― 五感のチェックリスト(P.4-7)", size=11, indent=0.5)
    add_text(doc, "② ワーク2:3年後の朝・昼・夜を立体化する(P.8-15)", size=11, indent=0.5)
    add_text(doc, "③ WOOPフォーマット入門(P.16-17)", size=11, indent=0.5)
    add_blank_line(doc, 1)
    add_text(doc, "すべてを今夜やる必要はありません。", size=11)
    add_blank_line(doc, 2)

    add_heading(doc, "最も大切なお願い", size=14, color=PINK_MAIN)
    add_text(doc, "P.4 を開いて、最初の3行だけ、書いてみてください。", size=11)
    add_blank_line(doc, 1)
    add_quote_box(doc, "「2029年5月22日、私は ____ になっています」")
    add_blank_line(doc, 1)
    add_text(doc, "この空欄を、埋めるだけです。", size=11)
    add_text(doc, "完璧でなくて構いません。", size=11)
    add_blank_line(doc, 1)
    add_text(doc, "最初の3行が、3年後のあなたを作ります。", size=12, bold=True, color=PINK_DARK, align=WD_ALIGN_PARAGRAPH.CENTER)


def page_work1_a(doc):
    """P.4 ワーク1:過去形で書くとは"""
    add_heading(doc, "ワーク1 ― 過去形で書く", size=20)
    add_divider(doc)

    add_text(doc, "「過去形で書く」とは何か", size=14, bold=True, color=PINK_DARK)
    add_blank_line(doc, 1)
    add_text(doc, "引き寄せの本で、よく「過去形で書け」と言われますが、", size=11)
    add_text(doc, "具体的にどう違うのでしょうか。", size=11)
    add_blank_line(doc, 1)

    add_text(doc, "✗ 未来形:「2029年に、月収50万円になりますように」", size=11, color=MUTED, indent=0.3)
    add_text(doc, "✗ 現在形:「私は今、月収50万円です」(嘘っぽくて続かない)", size=11, color=MUTED, indent=0.3)
    add_text(doc, "✓ 過去形:「2029年5月、私は副業で月収52万円に到達していました」", size=11, bold=True, color=PINK_MAIN, indent=0.3)

    add_blank_line(doc, 2)
    add_text(doc, "過去形で書くと、脳は「すでに起きた出来事」として処理し始めます。", size=11)
    add_blank_line(doc, 1)
    add_text(doc, "これが、脳科学者の言う「予期的な記憶の刷り込み」です。", size=11)
    add_text(doc, "未来の自分を、過去の記憶として、脳に登録するのです。", size=11)


def page_work1_b(doc):
    """P.5 五感チェックリスト"""
    add_heading(doc, "五感のチェックリスト", size=18, color=PINK_DARK)
    add_divider(doc)

    add_text(doc, "「3年後の朝、何が見えますか?」と聞かれて、即答できる人はいません。", size=11)
    add_text(doc, "でも、こうやって順に質問されると、答えられます。", size=11)
    add_blank_line(doc, 1)

    items = [
        ("👁  視覚 ― 朝起きて最初に見えるものは何ですか?",
         "例:「窓のカーテン越しの朝陽が、ベランダの観葉植物に当たっている」"),
        ("👂  聴覚 ― 周囲から何が聞こえてきますか?",
         "例:「ドリップコーヒーの音、夫が朝の家事をしている気配」"),
        ("✋  触覚 ― 体に感じる感覚は?",
         "例:「肩こりがなく、軽く、深く息ができる感覚」"),
        ("👃  嗅覚 ― どんな匂いがしますか?",
         "例:「コーヒー豆の苦みのある香り、観葉植物の青い匂い」"),
        ("👅  味覚 ― 朝食には何を食べていますか?",
         "例:「自家製パンと、トマトの甘み」"),
    ]
    for q, ex in items:
        add_text(doc, q, size=11, bold=True, color=PINK_DARK)
        add_text(doc, ex, size=10, color=MUTED, indent=0.5)
        add_blank_line(doc, 1)

    add_text(doc, "5つの感覚を順に書き出すと、未来は「絵」になり、「映像」になります。", size=11, color=PINK_MAIN, bold=True)


def page_work1_c(doc):
    """P.6 例文5パターン"""
    add_heading(doc, "例文5パターン", size=18, color=PINK_DARK)
    add_text(doc, "コピペで書き始められる雛形", size=11, color=MUTED)
    add_divider(doc)

    patterns = [
        ("パターン1(キャリア)",
         "「2029年5月、私は副業でXXに到達していました。\n朝、自分のペースで仕事を始められる毎日が、定着していました」"),
        ("パターン2(人間関係)",
         "「2029年5月、私は夫と週末の朝、ベランダで一緒にコーヒーを飲んでいました。\nお互いに、感謝の言葉を、自然に交わしていました」"),
        ("パターン3(健康)",
         "「2029年5月、私は健康診断オールAでした。\n朝起きた瞬間から、エネルギーが満ちている感覚が、当たり前になっていました」"),
        ("パターン4(自己表現)",
         "「2029年5月、私はXXとして発信を始めて、6ヶ月が経っていました。\nファンが100人を超え、毎日のメッセージが、私の喜びでした」"),
        ("パターン5(精神的な豊かさ)",
         "「2029年5月、私は朝、自分の呼吸を整える時間が、習慣になっていました。\n焦らず、急がず、満たされた感覚が、ベースラインでした」"),
    ]
    for title, body in patterns:
        add_text(doc, title, size=12, bold=True, color=PINK_MAIN)
        for line in body.split("\n"):
            add_text(doc, line, size=10, indent=0.5)
        add_blank_line(doc, 1)

    add_text(doc, "どれか1つを選んで、自分のことばに書き換えてみてください。", size=11, bold=True)


def page_work1_d(doc):
    """P.7 ワーク1記入欄"""
    add_heading(doc, "ワーク1 ― 記入欄", size=18, color=PINK_DARK)
    add_divider(doc)

    add_text(doc, "今夜、ここに3行だけ書いてみてください。", size=11, bold=True)
    add_blank_line(doc, 1)
    add_quote_box(doc, "(印刷推奨:ペンで書くと、脳の記憶定着が違います)")
    add_blank_line(doc, 2)

    prompts = [
        "2029年5月22日、私は",
        "                    になっていました。",
        "",
        "朝起きると、",
        "                    が見えていました。",
        "",
        "そして心は、",
        "                    で満たされていました。",
    ]
    for line in prompts:
        if line:
            add_text(doc, line, size=12)
            add_blank_input_line(doc, lines=1)
        else:
            add_blank_line(doc, 1)

    add_blank_line(doc, 2)
    add_text(doc, "書けましたか?", size=12, bold=True, color=PINK_DARK)
    add_text(doc, "これが、あなたの3年後の地図の、最初の3行です。", size=11, color=PINK_MAIN)


def page_work2_morning_a(doc):
    """P.8 3年後の朝を書く - 質問"""
    add_heading(doc, "ワーク2 ― 3年後の「朝」", size=20)
    add_divider(doc)

    add_text(doc, "朝6:30。3年後のあなたが目を覚ました瞬間。", size=11, bold=True, color=PINK_MAIN)
    add_blank_line(doc, 1)

    questions = [
        "🌅 何時に起きていますか?",
        "🌅 起きたとき、最初に何を感じますか?",
        "🌅 朝、最初に何をしますか?",
        "🌅 朝食は何を、どこで食べていますか?",
        "🌅 朝、隣には誰がいますか?",
    ]
    for q in questions:
        add_text(doc, q, size=11, bold=True, color=PINK_DARK)
        add_blank_input_line(doc, lines=2)
        add_blank_line(doc, 1)


def page_work2_morning_b(doc):
    """P.9 3年後の朝 記述スペース"""
    add_heading(doc, "3年後の「朝」記述スペース", size=18, color=PINK_DARK)
    add_divider(doc)
    add_text(doc, "P.8 で書いたメモを使って、3年後の朝のシーンを、", size=11)
    add_text(doc, "短編小説のように書いてみてください。", size=11)
    add_text(doc, "(50-100字で構いません)", size=10, color=MUTED)
    add_blank_line(doc, 2)
    add_text(doc, "2029年5月22日、朝6:30 ―", size=12, bold=True, color=PINK_DARK)
    add_blank_line(doc, 1)
    add_blank_input_line(doc, lines=10)


def page_work2_noon_a(doc):
    """P.10 3年後の昼を書く"""
    add_heading(doc, "3年後の「昼」", size=20)
    add_divider(doc)

    add_text(doc, "13:00。3年後のあなたが昼食を食べている瞬間。", size=11, bold=True, color=PINK_MAIN)
    add_blank_line(doc, 1)

    questions = [
        "🌞 どこで食べていますか?",
        "🌞 何を食べていますか?",
        "🌞 一人ですか? 誰かと一緒ですか?",
        "🌞 午後、何を始めますか?",
        "🌞 「今日もここまで来られた」と感じる、その日の喜びは何ですか?",
    ]
    for q in questions:
        add_text(doc, q, size=11, bold=True, color=PINK_DARK)
        add_blank_input_line(doc, lines=2)
        add_blank_line(doc, 1)


def page_work2_noon_b(doc):
    """P.11 3年後の昼 記述スペース"""
    add_heading(doc, "3年後の「昼」記述スペース", size=18, color=PINK_DARK)
    add_divider(doc)
    add_text(doc, "2029年5月22日、昼13:00 ―", size=12, bold=True, color=PINK_DARK)
    add_blank_line(doc, 1)
    add_blank_input_line(doc, lines=12)


def page_work2_night_a(doc):
    """P.12 3年後の夜を書く"""
    add_heading(doc, "3年後の「夜」", size=20)
    add_divider(doc)

    add_text(doc, "22:00。3年後のあなたが一日を終える瞬間。", size=11, bold=True, color=PINK_MAIN)
    add_blank_line(doc, 1)

    questions = [
        "🌙 寝る前のルーティンは何ですか?",
        "🌙 今日一日を振り返って、どんな気持ちですか?",
        "🌙 ベッドに入る前に、最後に何をしますか?",
        "🌙 隣には誰がいますか?",
        "🌙 眠りに就く瞬間、最後に思う言葉は何ですか?",
    ]
    for q in questions:
        add_text(doc, q, size=11, bold=True, color=PINK_DARK)
        add_blank_input_line(doc, lines=2)
        add_blank_line(doc, 1)


def page_work2_night_b(doc):
    """P.13 3年後の夜 記述スペース"""
    add_heading(doc, "3年後の「夜」記述スペース", size=18, color=PINK_DARK)
    add_divider(doc)
    add_text(doc, "2029年5月22日、夜22:00 ―", size=12, bold=True, color=PINK_DARK)
    add_blank_line(doc, 1)
    add_blank_input_line(doc, lines=12)


def page_work2_integration(doc):
    """P.14 統合・読み返し"""
    add_heading(doc, "「未来からの手紙」を完成させる", size=18, color=PINK_DARK)
    add_divider(doc)

    add_text(doc, "P.9 / P.11 / P.13 で書いた3シーンを、", size=11)
    add_text(doc, "1通の手紙として、続けて読み返してみてください。", size=11)
    add_blank_line(doc, 2)
    add_quote_box(doc, "声に出して、3回、読んでみてください。")
    add_blank_line(doc, 1)
    add_text(doc, "それが、3年後のあなたが、今夜、あなたに送ってきた手紙です。", size=12, bold=True, color=PINK_MAIN, align=WD_ALIGN_PARAGRAPH.CENTER)
    add_blank_line(doc, 3)

    add_heading(doc, "声に出した感想を、書き留めてください", size=12, color=PINK_DARK)
    add_blank_input_line(doc, lines=5)


def page_work2_save(doc):
    """P.15 保管場所"""
    add_heading(doc, "「未来からの手紙」の保管場所", size=18, color=PINK_DARK)
    add_divider(doc)

    add_text(doc, "手紙が完成したら、以下のいずれかに保管してください。", size=11)
    add_blank_line(doc, 1)

    add_text(doc, "📁 紙のノートの、最後のページ", size=12, bold=True, color=PINK_MAIN)
    add_text(doc, "私(桜木)が高校1年の春に実際にやった方法です。", size=10, color=MUTED, indent=0.5)
    add_blank_line(doc, 1)

    add_text(doc, "📁 スマホのメモアプリ", size=12, bold=True, color=PINK_MAIN)
    add_text(doc, "毎朝、最初に開く位置に固定", size=10, color=MUTED, indent=0.5)
    add_blank_line(doc, 1)

    add_text(doc, "📁 PCのデスクトップ", size=12, bold=True, color=PINK_MAIN)
    add_text(doc, "毎日、目に入る場所", size=10, color=MUTED, indent=0.5)
    add_blank_line(doc, 2)

    add_divider(doc)
    add_text(doc, "そして、毎朝1回、声に出して読んでください。", size=11, bold=True)
    add_blank_line(doc, 1)
    add_text(doc, "・3週間続けると、脳が「これは現実だ」と認識し始めます。", size=11, indent=0.5)
    add_text(doc, "・6週間続けると、行動が変わり始めます。", size=11, indent=0.5)
    add_text(doc, "・12週間続けると、人生の景色が変わり始めます。", size=11, indent=0.5)
    add_blank_line(doc, 1)
    add_text(doc, "これが、ジェームズ・ペネベイカーの30年・200研究で実証された、", size=10, color=MUTED)
    add_text(doc, "「書くこと」の本当の力です。", size=10, color=MUTED)


def page_woop_intro(doc):
    """P.16 WOOP導入"""
    add_heading(doc, "WOOPフォーマット入門", size=20)
    add_divider(doc)

    add_text(doc, "「願うだけ」では叶わない、という不都合な真実", size=14, bold=True, color=PINK_DARK)
    add_blank_line(doc, 1)

    add_text(doc, "ニューヨーク大学のガブリエル・エッティンゲン博士は、", size=11)
    add_text(doc, "20年以上の研究で、こう結論づけました。", size=11)
    add_blank_line(doc, 1)

    add_quote_box(doc, "「叶った姿を、ポジティブにイメージするだけ」の人は、何もしなかった人よりも、達成率が「むしろ下がる」。", italic=True)
    add_blank_line(doc, 1)

    add_text(doc, "理由は、シンプルです。", size=11)
    add_text(doc, "願うだけだと、脳が「もう叶った」と達成感を前借りし、", size=11)
    add_text(doc, "行動エネルギーが、枯渇してしまうのです。", size=11)
    add_blank_line(doc, 2)

    add_text(doc, "その処方箋が、WOOP法 です。", size=14, bold=True, color=PINK_MAIN, align=WD_ALIGN_PARAGRAPH.CENTER)


def page_woop_practice(doc):
    """P.17 WOOPワーク"""
    add_heading(doc, "WOOP法 4ステップ", size=18, color=PINK_DARK)
    add_divider(doc)

    add_text(doc, "P.14 で書いた「未来からの手紙」を見ながら、以下を書いてみてください。", size=11)
    add_blank_line(doc, 1)

    add_text(doc, "W ― Wish(願望)", size=13, bold=True, color=PINK_MAIN)
    add_text(doc, "あなたの3年後の願望を、1行で。", size=10, color=MUTED)
    add_blank_input_line(doc, lines=1)
    add_blank_line(doc, 1)

    add_text(doc, "O ― Outcome(成果)", size=13, bold=True, color=PINK_MAIN)
    add_text(doc, "それが叶った状態の、五感での詳細を、3行で。", size=10, color=MUTED)
    add_blank_input_line(doc, lines=3)
    add_blank_line(doc, 1)

    add_text(doc, "O ― Obstacle(障害)", size=13, bold=True, color=PINK_MAIN)
    add_text(doc, "過去、この目標に向かおうとして、止まってしまった経験はありますか?", size=10, color=MUTED)
    add_text(doc, "そのとき、あなたの「内側」にあった、最大の障害は何でしたか?", size=10, color=MUTED)
    add_blank_input_line(doc, lines=2)
    add_blank_line(doc, 1)

    add_text(doc, "P ― Plan(計画)", size=13, bold=True, color=PINK_MAIN)
    add_text(doc, "「もし【その障害】が出てきたら、私は【何】をする」", size=10, color=MUTED)
    add_blank_input_line(doc, lines=2)
    add_blank_line(doc, 1)

    add_text(doc, "毎日のWOOPを習慣化すると、目標達成率が一貫して向上することが、", size=10, color=MUTED)
    add_text(doc, "心理学研究で繰り返し示されています。", size=10, color=MUTED)


def page_ai_prompts(doc):
    """P.18 AIプロンプト5本"""
    add_heading(doc, "Manifest AI™ と話してみてください", size=18, color=PINK_DARK)
    add_divider(doc)

    add_text(doc, "ChatGPT または Claude を開いて、以下のプロンプトをコピペしてください。", size=11)
    add_text(doc, "桜木式に最適化された対話が、今夜、あなたを待っています。", size=11)
    add_blank_line(doc, 1)

    prompts_titles = [
        "【プロンプト1】最初の対話",
        "【プロンプト2】障害の言語化",
        "【プロンプト3】WOOPの仕上げ",
        "【プロンプト4】3年後の自分から、今の自分への手紙",
        "【プロンプト5】毎朝の問いかけ",
    ]
    descriptions = [
        "あなたが書いた「未来からの手紙」の冒頭を貼り、五感のディテールを質問で引き出してもらう。",
        "ソクラテス対話で「内側の本当の障害」を引き出してもらう。",
        "WOOPを実装意図フォーマット「もしXが起きたら、Yをする」で整える。",
        "桜木式フォーマットで「未来からの手紙」のドラフトを生成してもらう。",
        "30日間、毎朝1つだけ質問を投げかけてもらう設定。",
    ]
    for t, d in zip(prompts_titles, descriptions):
        add_text(doc, t, size=12, bold=True, color=PINK_MAIN)
        add_text(doc, d, size=10, color=MUTED, indent=0.5)
        add_blank_line(doc, 1)

    add_divider(doc)
    add_text(doc, "全文プロンプトは、マニフェスティング・マスター講座(¥19,800)で、", size=10, color=MUTED)
    add_text(doc, "30本セットでお届けしています。", size=10, color=MUTED)


def page_letter_sample(doc):
    """P.19 桜木の手紙(一部)"""
    add_heading(doc, "桜木の高校1年の手紙(一部公開)", size=18, color=PINK_DARK)
    add_divider(doc)

    add_text(doc, "私自身、高校1年の春に、こんな手紙を書きました。", size=11)
    add_text(doc, "ノートの最後のページに挟んでいた、3年後の私から、当時の私への手紙です。", size=11)
    add_blank_line(doc, 2)

    letter_lines = [
        "1998年3月10日",
        "",
        "賢治(現在の名前)へ",
        "",
        "私は今、東京大学の合格発表の前に立っています。",
        "自分の受験番号を見つけた瞬間です。",
        "",
        "朝、本郷の銀杏並木は、3月の風で揺れていました。",
        "駅から発表会場へ歩く道で、母からのメールを思い出しました。",
        "「眠れた?」とだけ書いてあったメッセージです。",
        "",
        "掲示板の前で、わたしは自分の番号を、3回確認しました。",
        "確かに、あったのです。",
        "",
        "・・・(以下、全文はマスター講座の特典として収録)・・・",
        "",
        "1998年3月10日 3年後のあなたより",
    ]
    for line in letter_lines:
        add_text(doc, line, size=11, color=PINK_DARK, indent=1.0)

    add_blank_line(doc, 2)
    add_divider(doc)
    add_text(doc, "3年後、ほぼこの通りの情景が、現実になりました。", size=11, bold=True)
    add_text(doc, "未来からの手紙には、こういう力が、確かにあります。", size=11, bold=True, color=PINK_MAIN)


def page_next_step(doc):
    """P.20 次のステップ"""
    add_heading(doc, "次のステップ", size=20)
    add_text(doc, "今夜から、30日プロトコルを始めましょう", size=12, color=PINK_DARK)
    add_divider(doc)

    add_text(doc, "ここまでお読みくださって、本当にありがとうございました。", size=11)
    add_blank_line(doc, 1)
    add_text(doc, "このPDFの内容を、今夜から30日間、毎日5分だけ実践してみてください。", size=11)
    add_text(doc, "それだけで、何かが変わり始めます。", size=11)
    add_blank_line(doc, 2)

    add_heading(doc, "もう一段、深く実践したい方へ", size=14, color=PINK_DARK)

    add_text(doc, "📦 マニフェスティング・マスター講座(¥19,800)", size=12, bold=True, color=PINK_MAIN)
    add_text(doc, "  6コンテンツ+3ボーナス・自学自習の決定版", size=10, color=MUTED, indent=0.3)
    add_text(doc, "  オーディオ三部作180分・ワークブック60ページ・プロンプト集30本・他", size=10, color=MUTED, indent=0.3)
    add_blank_line(doc, 1)

    add_text(doc, "🌹 Manifest AI™ 3ヶ月伴走プログラム(¥98,000)", size=12, bold=True, color=PINK_MAIN)
    add_text(doc, "  24時間のAI伴走+月1グループQ&A+桜木の個別添削", size=10, color=MUTED, indent=0.3)
    add_text(doc, "  伴走付きグループでは95%が3ヶ月後に変化を実感", size=10, color=MUTED, indent=0.3)
    add_blank_line(doc, 2)

    add_divider(doc)
    add_text(doc, "桜木賢治", size=12, bold=True, align=WD_ALIGN_PARAGRAPH.CENTER, color=PINK_DARK)
    add_text(doc, "日本マニフェスティング協会 代表", size=10, align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED)
    add_blank_line(doc, 1)
    add_text(doc, "著書:『科学的に正しい引き寄せ ― マーフィーが届けたかった、本当の引き寄せ』",
             size=10, align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED)
    add_text(doc, "(2026年10月発売予定)", size=10, align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED)
    add_blank_line(doc, 1)
    add_text(doc, "公式X:@mindlab_jp", size=10, align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED)
    add_blank_line(doc, 2)
    add_text(doc, "(c) 2026 日本マニフェスティング協会 / 桜木賢治",
             size=9, align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED)
    add_text(doc, "本PDFの内容を無断で転載・配布することはご遠慮ください。",
             size=9, align=WD_ALIGN_PARAGRAPH.CENTER, color=MUTED)


# ====================================================
#  Build
# ====================================================

def main():
    doc = Document()
    setup_page(doc)

    # デフォルトスタイル
    style = doc.styles['Normal']
    style.font.name = JP_FONT
    style.font.size = Pt(11)
    rPr = style.element.rPr
    rFonts = rPr.find(qn('w:rFonts'))
    if rFonts is None:
        rFonts = OxmlElement('w:rFonts')
        rPr.append(rFonts)
    rFonts.set(qn('w:eastAsia'), JP_FONT)

    pages = [
        page_cover,
        page_intro_1,
        page_intro_2,
        page_how_to_use,
        page_work1_a,
        page_work1_b,
        page_work1_c,
        page_work1_d,
        page_work2_morning_a,
        page_work2_morning_b,
        page_work2_noon_a,
        page_work2_noon_b,
        page_work2_night_a,
        page_work2_night_b,
        page_work2_integration,
        page_work2_save,
        page_woop_intro,
        page_woop_practice,
        page_ai_prompts,
        page_letter_sample,
        page_next_step,
    ]

    for i, page_func in enumerate(pages):
        page_func(doc)
        if i < len(pages) - 1:
            add_pagebreak(doc)

    doc.save(OUT)
    print(f"完成: {OUT}")
    print(f"全{len(pages)}ページ")


if __name__ == "__main__":
    main()
