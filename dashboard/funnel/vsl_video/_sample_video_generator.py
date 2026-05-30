"""
YouTube/VSL動画 自動生成スクリプト サンプル版
- 既存の WAV 音声 + 動的背景(桜の花びらが舞う夜空風)+ 自動テロップ
- 完成形は MP4 ファイル
"""
import os
import sys
import random
import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from moviepy import (
    AudioFileClip, ImageClip, CompositeVideoClip, ColorClip,
    concatenate_videoclips, VideoClip,
)

HERE = Path(__file__).resolve().parent
AUDIO = HERE.parent / "vsl_audio" / "final_01_hook_Algieba_088.wav"
OUT = HERE / "sample_hook_video.mp4"

# 1920x1080 (Full HD)
WIDTH, HEIGHT = 1920, 1080
FPS = 24  # 軽量化のため24fps

# ========= 桜の花びらが舞う背景 =========

class Petal:
    """1枚の花びら(粒子)"""
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.reset(initial=True)

    def reset(self, initial=False):
        self.x = random.uniform(0, self.w)
        # 初回はランダム高さ、それ以降は画面上から
        self.y = random.uniform(-self.h, 0) if initial else random.uniform(-100, -20)
        self.size = random.uniform(8, 20)
        self.vy = random.uniform(20, 60)       # 落下速度 (px/sec)
        self.vx = random.uniform(-15, 15)      # 横揺れ速度
        self.alpha = random.randint(120, 220)
        self.color = (255, 200, 220)           # ピンク

    def update(self, dt):
        self.y += self.vy * dt
        self.x += self.vx * dt
        if self.y > self.h + 30:
            self.reset()


def make_background_frame_fn(num_petals=80):
    """毎フレーム呼ばれて NumPy 画像配列を返す関数を作る"""
    petals = [Petal(WIDTH, HEIGHT) for _ in range(num_petals)]
    last_t = [0.0]

    def make_frame(t):
        dt = max(0.0, t - last_t[0])
        last_t[0] = t

        # 夜空のグラデーション背景
        img = Image.new("RGB", (WIDTH, HEIGHT), (15, 10, 30))  # 深い藍
        draw = ImageDraw.Draw(img, "RGBA")
        # 上から下へグラデーション
        for y in range(0, HEIGHT, 8):
            ratio = y / HEIGHT
            r = int(15 + ratio * 35)
            g = int(10 + ratio * 20)
            b = int(30 + ratio * 60)
            draw.rectangle([(0, y), (WIDTH, y + 8)], fill=(r, g, b))

        # 花びら描画(更新も同時に)
        for p in petals:
            p.update(dt)
            # 楕円(花びら形)
            x0, y0 = p.x - p.size, p.y - p.size * 0.5
            x1, y1 = p.x + p.size, p.y + p.size * 0.5
            draw.ellipse([x0, y0, x1, y1], fill=(*p.color, p.alpha))

        return np.array(img)

    return make_frame


# ========= テロップ生成 =========

def find_japanese_font():
    """日本語フォントを探す"""
    candidates = [
        "C:/Windows/Fonts/YuGothB.ttc",       # 游ゴシック Bold
        "C:/Windows/Fonts/YuGothM.ttc",       # 游ゴシック Medium
        "C:/Windows/Fonts/msgothic.ttc",      # MS ゴシック
        "C:/Windows/Fonts/meiryob.ttc",       # メイリオ Bold
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return None


def make_telop_image(text, font_path, font_size=80, color=(255, 255, 255),
                     stroke_color=(0, 0, 0), stroke_width=4,
                     max_width=1700):
    """テロップ画像(透過PNG)を生成"""
    font = ImageFont.truetype(font_path, font_size)

    # 改行処理(日本語は1文字単位で測りながら折り返す)
    lines = []
    current = ""
    for ch in text:
        test = current + ch
        bbox = font.getbbox(test)
        w = bbox[2] - bbox[0]
        if w > max_width and current:
            lines.append(current)
            current = ch
        else:
            current = test
    if current:
        lines.append(current)

    # 全体サイズ計算
    line_h = font_size + 15
    total_h = line_h * len(lines) + 40
    max_w = 0
    for ln in lines:
        bb = font.getbbox(ln)
        lw = bb[2] - bb[0]
        max_w = max(max_w, lw)
    total_w = max_w + 80

    img = Image.new("RGBA", (total_w, total_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    y = 20
    for ln in lines:
        bb = font.getbbox(ln)
        lw = bb[2] - bb[0]
        x = (total_w - lw) // 2
        # 縁取り
        for dx in range(-stroke_width, stroke_width + 1):
            for dy in range(-stroke_width, stroke_width + 1):
                if dx * dx + dy * dy <= stroke_width * stroke_width:
                    draw.text((x + dx, y + dy), ln, font=font, fill=stroke_color)
        draw.text((x, y), ln, font=font, fill=color)
        y += line_h

    return img


def telop_clip(text, start, duration, font_path,
               font_size=80, color=(255, 255, 255), y_pos="center"):
    """テロップを動画クリップに"""
    img = make_telop_image(text, font_path, font_size=font_size, color=color)
    arr = np.array(img)
    clip = ImageClip(arr, duration=duration).with_start(start)
    if y_pos == "center":
        clip = clip.with_position(("center", "center"))
    elif y_pos == "lower":
        clip = clip.with_position(("center", HEIGHT - 300))
    elif y_pos == "upper":
        clip = clip.with_position(("center", 200))
    # フェードイン・アウト(短い)
    try:
        from moviepy.video.fx import FadeIn, FadeOut
        clip = clip.with_effects([FadeIn(0.3), FadeOut(0.3)])
    except Exception:
        pass
    return clip


# ========= テロップタイミング設計 =========
# 01_hook.txt の内容に基づき、桜木音声(rate 0.88・約1分30秒想定)に対して
# 主要キーフレーズを以下のタイミングで表示する

TELOPS = [
    # (秒数, 表示時間, テキスト, フォントサイズ, 色, 位置)
    (0.5,  3.0, "桜木式 AIマニフェスティング®", 70, (255, 255, 255), "upper"),
    (4.0,  3.5, "引き寄せの本、何冊読みましたか?", 75, (255, 255, 255), "center"),
    (9.0,  3.5, "5冊?  10冊?  20冊以上?", 75, (255, 255, 255), "center"),
    (14.0, 4.0, "本当に人生が変わった本は?", 80, (255, 200, 87), "center"),  # 金色強調
    (20.0, 4.0, "おそらく ― ゼロ", 100, (255, 100, 100), "center"),  # 赤強調
    (26.0, 4.0, "「願えば叶う」 ― 叶わなかった", 65, (255, 255, 255), "center"),
    (32.0, 4.0, "「感謝すれば」 ― 何も起きなかった", 65, (255, 255, 255), "center"),
    (38.0, 4.0, "あなたのせいでは、ありません", 85, (255, 200, 87), "center"),
    (44.0, 4.0, "メソッドの設計が、不完全だったのです", 70, (255, 255, 255), "center"),
    (50.0, 3.0, "日本マニフェスティング協会", 60, (200, 200, 200), "lower"),
    (54.0, 3.0, "桜木 賢治", 70, (255, 255, 255), "lower"),
    (60.0, 4.0, "2024年 ― 世界で起きていたこと", 70, (255, 200, 87), "center"),
    (66.0, 4.5, "TikTok × Instagram", 65, (255, 255, 255), "center"),
    (72.0, 5.0, "628億回再生", 130, (255, 200, 87), "center"),  # 巨大数字
    (78.5, 3.5, "#Manifesting  530億", 55, (255, 255, 255), "center"),
    (82.5, 3.5, "#Scripting     70億", 55, (255, 255, 255), "center"),
    (86.5, 3.5, "#Shifting      28億", 55, (255, 255, 255), "center"),
]


# ========= メイン処理 =========

def main():
    if not AUDIO.exists():
        print(f"ERROR: 音声ファイルがありません: {AUDIO}", file=sys.stderr)
        sys.exit(1)

    font_path = find_japanese_font()
    if not font_path:
        print("ERROR: 日本語フォントが見つかりません", file=sys.stderr)
        sys.exit(1)
    print(f"フォント: {font_path}")

    # 音声読込
    print(f"音声読込: {AUDIO.name}")
    audio = AudioFileClip(str(AUDIO))
    duration = audio.duration
    print(f"音声尺: {duration:.1f}秒")

    # 背景動画(花びらが舞う)
    print("背景動画 生成中...")
    bg_frame_fn = make_background_frame_fn(num_petals=80)
    background = VideoClip(bg_frame_fn, duration=duration).with_fps(FPS)

    # テロップを duration 内に絞り込み
    telops = []
    print("テロップ配置中...")
    for start, dur, text, fsize, color, ypos in TELOPS:
        if start >= duration:
            continue
        actual_dur = min(dur, duration - start)
        if actual_dur < 0.3:
            continue
        t = telop_clip(text, start, actual_dur, font_path,
                       font_size=fsize, color=color, y_pos=ypos)
        telops.append(t)
        print(f"  {start:5.1f}s ({actual_dur:.1f}s): {text}")

    # 合成
    print("動画合成中...")
    final = CompositeVideoClip([background] + telops, size=(WIDTH, HEIGHT))
    final = final.with_audio(audio).with_duration(duration)

    # 書き出し
    print(f"MP4書き出し中: {OUT.name}")
    final.write_videofile(
        str(OUT),
        fps=FPS,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        bitrate="3000k",
        threads=4,
    )
    print(f"完了: {OUT}")
    print(f"ファイルサイズ: {OUT.stat().st_size / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
