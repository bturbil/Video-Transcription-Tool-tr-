import os
from datetime import timedelta

import whisper
from moviepy import VideoFileClip
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# ---------- CONFIG ----------
video_path  = r"C:\Users\TBU9BU\Desktop\videolar\ALI.mp4"
output_pdf  = r"C:\Users\TBU9BU\Desktop\videolar\ALI_transcript_frames_tr.pdf"

PAGE_W, PAGE_H = A4         # points
MARGIN = 36                 # points
IMG_MAX_H = PAGE_H * 0.62
FONT_SIZE = 14

FONT_CANDIDATES = [
    r"C:\Windows\Fonts\segoeui.ttf",
    r"C:\Windows\Fonts\arial.ttf",
    r"C:\Windows\Fonts\calibri.ttf",
    r"C:\Windows\Fonts\tahoma.ttf",
]

# ---------- FONT ----------
FONT_NAME = "TurkishFont"
for fp in FONT_CANDIDATES:
    if os.path.exists(fp):
        try:
            pdfmetrics.registerFont(TTFont(FONT_NAME, fp))
            break
        except Exception:
            continue
else:
    FONT_NAME = "Helvetica"

def wrap_text(text, max_width_pts, font_name, font_size):
    sw = pdfmetrics.stringWidth
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if sw(t, font_name, font_size) <= max_width_pts:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

# ---------- TRANSCRIBE ----------
model = whisper.load_model("small")
result = model.transcribe(
    video_path,
    language="tr",
    task="transcribe",
    fp16=False,
    temperature=0.0,
    no_speech_threshold=0.2,
)
segments = result.get("segments", [])
if not segments:
    raise RuntimeError("No segments from Whisper.")

# ---------- PDF (streaming) ----------
c = canvas.Canvas(output_pdf, pagesize=A4)
c.setTitle("Transcript Frames (TR)")

# ---------- VIDEO ----------
clip = VideoFileClip(video_path)

avail_w = PAGE_W - 2 * MARGIN
avail_h = IMG_MAX_H - MARGIN
line_height = FONT_SIZE * 1.35

for seg in segments:
    t_mid = (seg["start"] + seg["end"]) / 2.0
    frame = clip.get_frame(t_mid)                 # RGB ndarray
    pil_img = Image.fromarray(frame)              # PIL Image

    w, h = pil_img.size
    scale = min(avail_w / w, max(1e-6, avail_h / h))
    img_w = max(1.0, w * scale)
    img_h = max(1.0, h * scale)

    img = ImageReader(pil_img)

    img_x = MARGIN + (avail_w - img_w) / 2.0
    img_y = PAGE_H - MARGIN - img_h
    c.drawImage(img, img_x, img_y, width=img_w, height=img_h, preserveAspectRatio=True, mask='auto')

    timestamp = str(timedelta(seconds=int(seg["start"])))
    caption = f"[{timestamp}] {seg['text'].strip()}"

    c.setFont(FONT_NAME, FONT_SIZE)
    lines = wrap_text(caption, avail_w, FONT_NAME, FONT_SIZE)

    text_y = img_y - 14
    for line in lines:
        text_y -= line_height
        if text_y < MARGIN:
            c.showPage()
            c.setFont(FONT_NAME, FONT_SIZE)
            text_y = PAGE_H - MARGIN - line_height
        c.drawString(MARGIN, text_y, line)

    c.showPage()

clip.close()
c.save()
