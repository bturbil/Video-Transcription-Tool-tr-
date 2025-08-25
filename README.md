# Video-to-Transcript-Frames PDF (TR/EN)
--EN--
# Overview
Converts a Turkish video into a paged PDF. Each page shows a video frame sampled at the middle of every transcription segment and the corresponding timestamped text. Uses OpenAI Whisper for speech-to-text, MoviePy for frame extraction, Pillow for image handling, and ReportLab for PDF generation. Turkish-capable fonts are auto-detected; falls back to Helvetica if none found.

# Features
- Offline Whisper transcription (`small` model by default)
- Timestamped captions
- Auto-scaling video frames to A4
- Turkish glyph-safe font selection on Windows
- Simple line-wrapping to page width

# Requirements
- Python 3.9+ recommended
- FFmpeg available on PATH (MoviePy/Whisper need it)
- Packages: `openai-whisper`, `moviepy`, `Pillow`, `reportlab`, `torch` (CPU or CUDA)

Install:
pip install -U openai-whisper moviepy Pillow reportlab
# CPU Torch:
pip install torch --index-url https://download.pytorch.org/whl/cpu
# If you have CUDA 12.1:
# pip install torch --index-url https://download.pytorch.org/whl/cu121

FFmpeg:
Windows: install ffmpeg and add its bin to PATH.

macOS: brew install ffmpeg.

Linux: sudo apt-get install ffmpeg.

# Configuration
Edit these at the top of the script:

video_path  = r"xxx"  # path to input video file
output_pdf  = r"xxx"  # path to output PDF file

Optional: change model size (tiny, base, small, medium, large) in:

model = whisper.load_model("small")
Larger models → better accuracy, more VRAM/RAM and time.

# Usage
Run from the project directory:

python video_transcript.py
The script will:

Load Whisper, transcribe Turkish (language="tr", task="transcribe").

For each segment, sample the mid-time frame and render to PDF with [hh:mm:ss] text.

Save the PDF at output_pdf.

#Output
A4 PDF

Each segment produces a page with an auto-scaled frame and wrapped caption lines.

# Notes
Fonts: the script tries Segoe UI, Arial, Calibri, Tahoma. If none found, uses Helvetica (may miss some Turkish glyph shaping).

Performance: GPU accelerates Whisper. CPU works but is slower.

Long videos: large PDFs. Consider changing IMG_MAX_H, FONT_SIZE, or concatenating multiple segments per page if needed.

# Troubleshooting
No segments from Whisper. → Audio not detected or ffmpeg missing. Verify ffmpeg -version.

MoviePy errors about readers/writers → confirm ffmpeg install and file path correctness.

CUDA not used → install CUDA-enabled Torch or run on CPU as above.

Missing fonts for Turkish accents → install a Unicode font and add its path to FONT_CANDIDATES.



--TR-- 
#Genel Bakış

Türkçe bir videoyu bölümlere ayrılmış PDF’e dönüştürür. Her sayfada, ilgili konuşma bölümünün orta anından alınmış bir video karesi ve zaman damgalı metin bulunur. Konuşma-metin için Whisper, kare almak için MoviePy, görüntü için Pillow, PDF için ReportLab kullanılır. Windows’ta Türkçe karakterleri destekleyen fontlar otomatik seçilir; yoksa Helvetica’ya düşer.

# Özellikler

Çevrimdışı Whisper transkripsiyonu (varsayılan small)

Zaman damgalı altyazılar

A4’e otomatik ölçekleme

Türkçe karakter güvenli yazı tipi seçimi

Basit satır kaydırma

# Gereksinimler

Önerilen Python 3.9+

PATH’te FFmpeg

Paketler: openai-whisper, moviepy, Pillow, reportlab, torch (CPU veya CUDA)

Kurulum:

pip install -U openai-whisper moviepy Pillow reportlab
# CPU Torch:
pip install torch --index-url https://download.pytorch.org/whl/cpu
# CUDA 12.1 varsa:
# pip install torch --index-url https://download.pytorch.org/whl/cu121


FFmpeg:

Windows: ffmpeg kur ve bin klasörünü PATH’e ekle.

macOS: brew install ffmpeg.

Linux: sudo apt-get install ffmpeg.

# Yapılandırma

Script başındaki değerleri düzenle:

video_path  = r"xxx"   # video dosya yolu
output_pdf  = r"xxx"   # çıktı PDF dosya yolu


Model boyutu değişimi:

model = whisper.load_model("small")


Büyük model → daha iyi doğruluk, daha fazla bellek ve süre.

# Kullanım

Proje klasöründen çalıştır:

python video_transcript.py


#İş akışı:

Whisper Türkçe transkripsiyon yapar (language="tr").

Her bölüm için orta zamandaki kare alınır, [ss:dd:sn] metin ile PDF’e yazılır.

PDF, output_pdf yoluna kaydedilir.

# Çıktı

A4 PDF

Her bölüm için bir sayfa: ölçeklenmiş kare + satır kaydırmalı açıklama.

# Notlar

Yazı tipleri: Segoe UI, Arial, Calibri, Tahoma denenir; yoksa Helvetica.

Performans: GPU hızlıdır; CPU çalışır ama yavaştır.

Uzun videolar: PDF büyür. IMG_MAX_H, FONT_SIZE düşürülebilir veya sayfa başına birden çok bölüm yazılabilir.

# Sorun Giderme

No segments from Whisper. → Ses algılanmadı veya ffmpeg yok. ffmpeg -version ile doğrula.

MoviePy okuyucu/yazıcı hataları → ffmpeg ve dosya yolu kontrol et.

CUDA kullanılmıyor → CUDA destekli Torch kur veya CPU’da çalıştır.

Türkçe karakter sorunları → Unicode font kur ve yolunu FONT_CANDIDATES listesine ekle.
